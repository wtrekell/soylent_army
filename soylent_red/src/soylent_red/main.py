#!/usr/bin/env python
import sys
import warnings

from soylent_red.crew import SoylentRed

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew with user-provided topic.
    Usage: crewai run "Your Article Topic"
    """
    if len(sys.argv) < 2:
        topic = input("Enter the article topic: ")
    else:
        topic = " ".join(sys.argv[1:])
    
    inputs = {
        'topic': topic,
    }
    
    try:
        result = SoylentRed().crew().kickoff(inputs=inputs)
        print(f"\n✅ Article completed successfully!")
        print(f"📝 Topic: {topic}")
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