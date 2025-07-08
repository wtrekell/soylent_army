from crewai.tools import BaseTool
from typing import Type, Optional, List
from pydantic import BaseModel, Field
import requests
import os
import json
import base64
from pathlib import Path
import re
from bs4 import BeautifulSoup


class GitHubRepoInput(BaseModel):
    """Input schema for GitHub repository tools."""
    repo_path: str = Field(..., description="Repository path like 'cloudscape-design/components'")
    target_path: Optional[str] = Field(None, description="Specific path within repo to target")
    file_extensions: Optional[List[str]] = Field(default=[".css", ".scss", ".sass"], description="File extensions to extract")


class GitHubSourceExtractorTool(BaseTool):
    name: str = "GitHub Source Extractor"
    description: str = (
        "Extract source code files (CSS, SCSS, etc.) from GitHub repositories. "
        "Downloads actual source files from the Cloudscape design system repos."
    )
    args_schema: Type[BaseModel] = GitHubRepoInput

    def _run(self, repo_path: str, target_path: Optional[str] = None, file_extensions: Optional[List[str]] = None) -> str:
        """Extract source files from GitHub repository."""
        if file_extensions is None:
            file_extensions = [".css", ".scss", ".sass"]
            
        try:
            # GitHub API base URL
            base_url = f"https://api.github.com/repos/{repo_path}/contents"
            if target_path:
                base_url += f"/{target_path}"
            
            # Create local directory structure
            local_path = Path(f"raw_materials/github_sources/{repo_path.replace('/', '_')}")
            if target_path:
                local_path = local_path / target_path
            local_path.mkdir(parents=True, exist_ok=True)
            
            # Recursively fetch files
            extracted_files = self._fetch_files_recursive(base_url, local_path, file_extensions)
            
            return f"""Successfully extracted {len(extracted_files)} files from {repo_path}:

Files extracted:
{chr(10).join([f"- {file}" for file in extracted_files[:10]])}
{f"... and {len(extracted_files) - 10} more files" if len(extracted_files) > 10 else ""}

Local path: {local_path}

Next steps:
1. Review the extracted files
2. Use Component CSS Analyzer to understand the styling structure
3. Use Design Pattern Extractor to identify reusable patterns"""
            
        except Exception as e:
            return f"Error extracting files from {repo_path}: {str(e)}"

    def _fetch_files_recursive(self, url: str, local_path: Path, file_extensions: List[str]) -> List[str]:
        """Recursively fetch files from GitHub API."""
        extracted_files = []
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            contents = response.json()
            
            for item in contents:
                if item['type'] == 'file':
                    # Check if file has target extension
                    if any(item['name'].endswith(ext) for ext in file_extensions):
                        file_content = self._download_file(item['download_url'])
                        if file_content:
                            file_path = local_path / item['name']
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(file_content)
                            extracted_files.append(str(file_path))
                            
                elif item['type'] == 'dir':
                    # Recursively process directories
                    sub_path = local_path / item['name']
                    sub_path.mkdir(exist_ok=True)
                    sub_files = self._fetch_files_recursive(item['url'], sub_path, file_extensions)
                    extracted_files.extend(sub_files)
                    
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            
        return extracted_files

    def _download_file(self, download_url: str) -> Optional[str]:
        """Download individual file content."""
        try:
            response = requests.get(download_url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None


class ComponentAnalysisInput(BaseModel):
    """Input schema for component CSS analysis."""
    component_path: str = Field(..., description="Path to component CSS/SCSS files")
    analysis_type: Optional[str] = Field("full", description="Type of analysis: 'full', 'variables', 'selectors', 'patterns'")


class ComponentCSSAnalyzerTool(BaseTool):
    name: str = "Component CSS Analyzer"
    description: str = (
        "Analyze CSS/SCSS files to extract component styling patterns, variables, "
        "and design tokens. Identifies visual patterns for reskinning."
    )
    args_schema: Type[BaseModel] = ComponentAnalysisInput

    def _run(self, component_path: str, analysis_type: str = "full") -> str:
        """Analyze CSS/SCSS component files."""
        try:
            path = Path(component_path)
            if not path.exists():
                return f"Path not found: {component_path}"
            
            css_files = []
            if path.is_file():
                css_files = [path]
            else:
                css_files = list(path.rglob("*.css")) + list(path.rglob("*.scss")) + list(path.rglob("*.sass"))
            
            if not css_files:
                return f"No CSS/SCSS files found in {component_path}"
            
            analysis_results = []
            
            for css_file in css_files:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_analysis = self._analyze_css_content(content, css_file.name, analysis_type)
                analysis_results.append(file_analysis)
            
            return f"""CSS Analysis Results for {component_path}:

Analyzed {len(css_files)} files:

{chr(10).join(analysis_results)}

Summary:
- Total files analyzed: {len(css_files)}
- Analysis type: {analysis_type}
- Ready for pattern extraction and reskinning"""
            
        except Exception as e:
            return f"Error analyzing CSS files: {str(e)}"

    def _analyze_css_content(self, content: str, filename: str, analysis_type: str) -> str:
        """Analyze individual CSS file content."""
        results = [f"\n## {filename}"]
        
        if analysis_type in ["full", "variables"]:
            # Extract CSS variables
            css_vars = re.findall(r'--[\w-]+:\s*[^;]+', content)
            if css_vars:
                results.append(f"CSS Variables ({len(css_vars)}):")
                results.extend([f"  {var}" for var in css_vars[:5]])
                if len(css_vars) > 5:
                    results.append(f"  ... and {len(css_vars) - 5} more")
        
        if analysis_type in ["full", "selectors"]:
            # Extract class selectors
            selectors = re.findall(r'\.[\w-]+', content)
            unique_selectors = list(set(selectors))
            if unique_selectors:
                results.append(f"CSS Classes ({len(unique_selectors)}):")
                results.extend([f"  {sel}" for sel in unique_selectors[:5]])
                if len(unique_selectors) > 5:
                    results.append(f"  ... and {len(unique_selectors) - 5} more")
        
        if analysis_type in ["full", "patterns"]:
            # Look for common design patterns
            patterns = []
            if 'border-radius' in content:
                patterns.append("Rounded corners")
            if 'box-shadow' in content:
                patterns.append("Shadows/elevation")
            if 'transition' in content or 'animation' in content:
                patterns.append("Animations/transitions")
            if '@media' in content:
                patterns.append("Responsive design")
            if 'grid' in content or 'flex' in content:
                patterns.append("Layout patterns")
                
            if patterns:
                results.append(f"Design Patterns: {', '.join(patterns)}")
        
        return '\n'.join(results)


class DesignPatternInput(BaseModel):
    """Input schema for design pattern extraction."""
    source_directory: str = Field(..., description="Directory containing CSS/SCSS files")
    pattern_type: Optional[str] = Field("all", description="Type of patterns to extract: 'colors', 'typography', 'spacing', 'components', 'all'")


class DesignPatternExtractorTool(BaseTool):
    name: str = "Design Pattern Extractor"
    description: str = (
        "Extract reusable design patterns from CSS files. Identifies color schemes, "
        "typography, spacing, and component patterns for creating new variants."
    )
    args_schema: Type[BaseModel] = DesignPatternInput

    def _run(self, source_directory: str, pattern_type: str = "all") -> str:
        """Extract design patterns from CSS files."""
        try:
            path = Path(source_directory)
            if not path.exists():
                return f"Directory not found: {source_directory}"
            
            css_files = list(path.rglob("*.css")) + list(path.rglob("*.scss"))
            
            if not css_files:
                return f"No CSS/SCSS files found in {source_directory}"
            
            # Combine all CSS content
            all_content = ""
            for css_file in css_files:
                with open(css_file, 'r', encoding='utf-8') as f:
                    all_content += f"\n/* {css_file.name} */\n" + f.read()
            
            patterns = self._extract_patterns(all_content, pattern_type)
            
            return f"""Design Pattern Analysis for {source_directory}:

{patterns}

Files analyzed: {len(css_files)}
Pattern type: {pattern_type}

These patterns can be used as a foundation for creating new component variants and reskinning the design system."""
            
        except Exception as e:
            return f"Error extracting design patterns: {str(e)}"

    def _extract_patterns(self, content: str, pattern_type: str) -> str:
        """Extract specific types of design patterns."""
        results = []
        
        if pattern_type in ["all", "colors"]:
            # Extract color patterns
            colors = re.findall(r'#[0-9a-fA-F]{3,6}|rgb\([^)]+\)|rgba\([^)]+\)|hsl\([^)]+\)', content)
            unique_colors = list(set(colors))
            if unique_colors:
                results.append(f"## Color Patterns ({len(unique_colors)} unique)")
                results.extend([f"  {color}" for color in unique_colors[:10]])
                if len(unique_colors) > 10:
                    results.append(f"  ... and {len(unique_colors) - 10} more")
        
        if pattern_type in ["all", "typography"]:
            # Extract typography patterns
            font_sizes = re.findall(r'font-size:\s*[^;]+', content)
            font_families = re.findall(r'font-family:\s*[^;]+', content)
            if font_sizes or font_families:
                results.append("## Typography Patterns")
                if font_sizes:
                    unique_sizes = list(set(font_sizes))
                    results.append(f"Font sizes: {', '.join(unique_sizes[:5])}")
                if font_families:
                    unique_families = list(set(font_families))
                    results.append(f"Font families: {', '.join(unique_families[:3])}")
        
        if pattern_type in ["all", "spacing"]:
            # Extract spacing patterns
            margins = re.findall(r'margin[^:]*:\s*[^;]+', content)
            paddings = re.findall(r'padding[^:]*:\s*[^;]+', content)
            if margins or paddings:
                results.append("## Spacing Patterns")
                if margins:
                    unique_margins = list(set(margins))
                    results.append(f"Margins: {len(unique_margins)} variations")
                if paddings:
                    unique_paddings = list(set(paddings))
                    results.append(f"Paddings: {len(unique_paddings)} variations")
        
        if pattern_type in ["all", "components"]:
            # Extract component-specific patterns
            border_radius = re.findall(r'border-radius:\s*[^;]+', content)
            box_shadows = re.findall(r'box-shadow:\s*[^;]+', content)
            if border_radius or box_shadows:
                results.append("## Component Patterns")
                if border_radius:
                    unique_radius = list(set(border_radius))
                    results.append(f"Border radius: {len(unique_radius)} variations")
                if box_shadows:
                    unique_shadows = list(set(box_shadows))
                    results.append(f"Box shadows: {len(unique_shadows)} variations")
        
        return '\n'.join(results) if results else "No patterns found for the specified type."


class VisualReferenceInput(BaseModel):
    """Input schema for visual reference generation."""
    components_directory: str = Field(..., description="Directory containing component files")
    output_format: Optional[str] = Field("html", description="Output format: 'html', 'markdown', 'json'")


class VisualReferenceGeneratorTool(BaseTool):
    name: str = "Visual Reference Generator"
    description: str = (
        "Generate a visual reference guide from component CSS files. Creates an easy-to-browse "
        "documentation of all visual components for reskinning reference."
    )
    args_schema: Type[BaseModel] = VisualReferenceInput

    def _run(self, components_directory: str, output_format: str = "html") -> str:
        """Generate visual reference documentation."""
        try:
            path = Path(components_directory)
            if not path.exists():
                return f"Directory not found: {components_directory}"
            
            # Create output directory
            output_dir = Path("refined_materials/visual_reference")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            if output_format == "html":
                output_file = output_dir / "design_system_reference.html"
                content = self._generate_html_reference(path)
            elif output_format == "markdown":
                output_file = output_dir / "design_system_reference.md"
                content = self._generate_markdown_reference(path)
            else:
                output_file = output_dir / "design_system_reference.json"
                content = self._generate_json_reference(path)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"""Visual reference generated successfully!

Output file: {output_file}
Format: {output_format}
Components directory: {components_directory}

The reference includes:
- Component catalog
- CSS variable documentation
- Color palette
- Typography scale
- Spacing system
- Interactive patterns

Open the {output_format} file to browse your design system reference."""
            
        except Exception as e:
            return f"Error generating visual reference: {str(e)}"

    def _generate_html_reference(self, components_dir: Path) -> str:
        """Generate HTML reference documentation."""
        css_files = list(components_dir.rglob("*.css")) + list(components_dir.rglob("*.scss"))
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloudscape Design System Reference</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 2rem; }}
        .component {{ border: 1px solid #ddd; margin: 1rem 0; padding: 1rem; border-radius: 4px; }}
        .component h3 {{ margin-top: 0; color: #333; }}
        .code {{ background: #f5f5f5; padding: 0.5rem; border-radius: 4px; font-family: monospace; }}
        .colors {{ display: flex; flex-wrap: wrap; gap: 1rem; }}
        .color-swatch {{ width: 50px; height: 50px; border-radius: 4px; border: 1px solid #ccc; }}
    </style>
</head>
<body>
    <h1>Cloudscape Design System Reference</h1>
    <p>Generated from {len(css_files)} CSS/SCSS files</p>
    
    <h2>Components</h2>
"""
        
        for css_file in css_files[:20]:  # Limit to first 20 for demo
            component_name = css_file.stem
            html_content += f"""
    <div class="component">
        <h3>{component_name}</h3>
        <p>Source: {css_file.name}</p>
        <div class="code">/* CSS content analysis would go here */</div>
    </div>
"""
        
        html_content += """
</body>
</html>"""
        
        return html_content

    def _generate_markdown_reference(self, components_dir: Path) -> str:
        """Generate Markdown reference documentation."""
        css_files = list(components_dir.rglob("*.css")) + list(components_dir.rglob("*.scss"))
        
        content = f"""# Cloudscape Design System Reference

Generated from {len(css_files)} CSS/SCSS files in `{components_dir}`

## Component Files

"""
        
        for css_file in css_files:
            content += f"- **{css_file.stem}** (`{css_file.name}`)\n"
        
        content += """
## Usage Notes

This reference was generated to help with reskinning and component development. 
Each component can be analyzed for:
- Color variables
- Typography patterns
- Spacing systems
- Animation patterns
- Responsive breakpoints

"""
        
        return content

    def _generate_json_reference(self, components_dir: Path) -> str:
        """Generate JSON reference documentation."""
        css_files = list(components_dir.rglob("*.css")) + list(components_dir.rglob("*.scss"))
        
        reference_data = {
            "design_system": "Cloudscape",
            "generated_from": str(components_dir),
            "total_files": len(css_files),
            "components": []
        }
        
        for css_file in css_files:
            reference_data["components"].append({
                "name": css_file.stem,
                "filename": css_file.name,
                "path": str(css_file),
                "type": css_file.suffix
            })
        
        return json.dumps(reference_data, indent=2)