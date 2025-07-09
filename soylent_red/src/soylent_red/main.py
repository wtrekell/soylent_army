#!/usr/bin/env python
import sys
import warnings
import os
import yaml
from pathlib import Path

from .crew import SoylentRed

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew with user-provided content file path or manifest.
    Usage: crewai run "path/to/content/file.md" or "path/to/manifest.yaml"
    """
    if len(sys.argv) < 2:
        file_path = input("Enter the relative path to content file or manifest: ")
    else:
        file_path = " ".join(sys.argv[1:])
    
    # Convert to Path object and resolve relative to current working directory
    file_path = Path(file_path).resolve()
    
    # Validate file path
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Convert back to string for compatibility
    file_path = str(file_path)
    
    # Check if it's a YAML manifest or content file
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        inputs = process_manifest(file_path)
    else:
        inputs = process_content_file(file_path)
    
    try:
        crew_instance = SoylentRed()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Dynamic output path
        output_dir = crew_instance.project_root / "supplies"
        output_file = output_dir / "final_article.md"
        
        print(f"\n✅ Article completed successfully!")
        print(f"📁 Source: {file_path}")
        print(f"📄 Output saved to: {output_file}")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def process_manifest(manifest_path):
    """Process YAML manifest file and extract content from source files."""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = yaml.safe_load(f)
    except Exception as e:
        raise Exception(f"Error reading manifest file: {e}")
    
    # Get directory of manifest for relative paths
    manifest_dir = Path(manifest_path).parent
    
    # Combine content from source files
    combined_content = ""
    source_files = manifest.get('source_files', [])
    
    for source_file in source_files:
        source_path = manifest_dir / source_file
        if source_path.exists():
            try:
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    combined_content += f"\n\n## Content from {source_file}\n\n{content}"
            except Exception as e:
                print(f"Warning: Could not read {source_file}: {e}")
        else:
            print(f"Warning: Source file not found: {source_path}")
            print(f"  Looking in directory: {manifest_dir}")
            print(f"  Available files: {list(manifest_dir.glob('*'))}")
    
    # Build comprehensive inputs
    inputs = {
        'content_file_path': str(manifest_path),
        'raw_content': combined_content,
        'source_filename': Path(manifest_path).name,
        'title': manifest.get('title', 'Untitled Article'),
        'context': manifest.get('context', ''),
        'summary': manifest.get('summary', ''),
        'brand': manifest.get('brand', 'Syntax & Empathy'),
        'personas': manifest.get('personas', []),
        'required_sections': manifest.get('required_sections', []),
        'notes': manifest.get('notes', ''),
        'manifest_instructions': yaml.dump(manifest, default_flow_style=False)
    }
    
    return inputs


def process_content_file(file_path):
    """Process regular content file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        raise Exception(f"Error reading content file: {e}")
    
    filename = Path(file_path).name
    
    inputs = {
        'content_file_path': file_path,
        'raw_content': raw_content,
        'source_filename': filename,
    }
    
    return inputs
    


def train():
    """
    Train the crew for a given number of iterations.
    """
    if len(sys.argv) < 4:
        print("Usage: crewai train <iterations> <filename> \"<topic>\"")
        return
        
    inputs = {
        "topic": sys.argv[3] if len(sys.argv) > 3 else "Sample Article Topic"
    }
    try:
        SoylentRed().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    if len(sys.argv) < 2:
        print("Usage: crewai replay <task_id>")
        return
        
    try:
        SoylentRed().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    if len(sys.argv) < 4:
        print("Usage: crewai test <iterations> <eval_llm> \"<topic>\"")
        return
        
    inputs = {
        "topic": sys.argv[3] if len(sys.argv) > 3 else "Test Article Topic"
    }
    
    try:
        SoylentRed().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == '__main__':
    run()