#!/usr/bin/env python
import sys
import warnings
import os

from soylent_red.crew import SoylentRed

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew with user-provided content file path.
    Usage: crewai run "path/to/content/file.md"
    """
    if len(sys.argv) < 2:
        file_path = input("Enter the relative path to content file: ")
    else:
        file_path = " ".join(sys.argv[1:])
    
    # Validate file path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Content file not found: {file_path}")
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
    except Exception as e:
        raise Exception(f"Error reading content file: {e}")
    
    # Extract filename for reference
    filename = os.path.basename(file_path)
    
    inputs = {
        'content_file_path': file_path,
        'raw_content': raw_content,
        'source_filename': filename,
    }
    
    try:
        result = SoylentRed().crew().kickoff(inputs=inputs)
        print(f"\n✅ Article completed successfully!")
        print(f"📁 Source: {file_path}")
        print(f"📄 Output saved to: final_article.md")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


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