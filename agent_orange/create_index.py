#!/usr/bin/env python3
"""
Create an index of all the extracted Cloudscape materials
"""

import os
from pathlib import Path
import re

def create_index():
    base_dir = Path("refined_materials/cloudscape_complete")
    
    print("# Cloudscape Design System - Extracted Materials Index")
    print()
    
    # CSS Files
    css_dir = base_dir / "css"
    if css_dir.exists():
        css_files = list(css_dir.glob("*.css"))
        print(f"## CSS Files ({len(css_files)} files)")
        print("These are the compiled CSS files from the live site:")
        print()
        for i, css_file in enumerate(css_files[:10]):  # Show first 10
            size_kb = css_file.stat().st_size / 1024
            print(f"- `{css_file.name}` ({size_kb:.1f}KB)")
        if len(css_files) > 10:
            print(f"- ... and {len(css_files) - 10} more CSS files")
        print()
    
    # SCSS Source Files
    scss_dir = base_dir / "github_css/cloudscape-design_components/pages"
    if scss_dir.exists():
        scss_files = []
        for component_dir in scss_dir.iterdir():
            if component_dir.is_dir():
                for scss_file in component_dir.rglob("*.scss"):
                    scss_files.append((component_dir.name, scss_file))
        
        print(f"## SCSS Source Files ({len(scss_files)} files)")
        print("These are the source SCSS files from GitHub:")
        print()
        
        # Group by component
        components = {}
        for component, scss_file in scss_files:
            if component not in components:
                components[component] = []
            components[component].append(scss_file)
        
        for component, files in sorted(components.items())[:15]:  # Show first 15 components
            print(f"### {component}")
            for scss_file in files:
                rel_path = scss_file.relative_to(scss_dir)
                print(f"- `{rel_path}`")
            print()
        
        if len(components) > 15:
            print(f"... and {len(components) - 15} more components with SCSS files")
        print()
    
    # HTML Files
    html_files = list(base_dir.glob("*.html"))
    if html_files:
        print(f"## HTML Files ({len(html_files)} files)")
        print("Complete HTML pages with CSS references:")
        print()
        for html_file in html_files:
            size_mb = html_file.stat().st_size / (1024 * 1024)
            print(f"- `{html_file.name}` ({size_mb:.1f}MB)")
        print()
    
    # Key SCSS files to examine
    key_scss_files = [
        "app-layout/styles.scss",
        "button/styles.scss", 
        "autosuggest/styles.scss",
        "checkbox/styles.scss",
        "button-dropdown/styles.scss"
    ]
    
    print("## Key SCSS Files for Reskinning")
    print("These files contain the core component styling:")
    print()
    
    for key_file in key_scss_files:
        full_path = scss_dir / key_file
        if full_path.exists():
            size_kb = full_path.stat().st_size / 1024
            print(f"- **{key_file}** ({size_kb:.1f}KB)")
            
            # Show a few lines of the file
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]
                for line in lines[4:8]:  # Skip copyright, show some actual CSS
                    if line.strip() and not line.strip().startswith('/*'):
                        print(f"  ```scss")
                        print(f"  {line.strip()}")
                        print(f"  ```")
                        break
            print()
    
    print("## Next Steps")
    print()
    print("1. **Browse the SCSS files** in `github_css/cloudscape-design_components/pages/` to understand component structure")
    print("2. **Check the compiled CSS** in `css/` directory to see the final output")
    print("3. **Use the HTML files** as live examples of components in action")
    print("4. **Start with key components** like buttons, inputs, and layout for reskinning")
    print()
    print("**Note**: The extraction got real SCSS source files with design tokens, not TypeScript!")

if __name__ == "__main__":
    create_index()