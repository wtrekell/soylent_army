#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from pathlib import Path

from agent_orange.crew import AgentOrange

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the Cloudscape Design System analysis and reskinning crew.
    This will extract, analyze, and create reference materials for the Cloudscape Design System.
    """
    
    # Ensure output directories exist
    Path("raw_materials/github_sources").mkdir(parents=True, exist_ok=True)
    Path("refined_materials").mkdir(parents=True, exist_ok=True)
    
    inputs = {
        'design_system': 'Cloudscape Design System',
        'analysis_date': datetime.now().strftime("%Y-%m-%d"),
        'target_repos': [
            'cloudscape-design/components',
            'cloudscape-design/global-styles', 
            'cloudscape-design/board-components',
            'cloudscape-design/chart-components'
        ]
    }
    
    print("🔶 Starting Agent Orange - Cloudscape Design System Analysis")
    print("📋 This crew will:")
    print("   1. Extract CSS/SCSS source files from GitHub repositories")
    print("   2. Analyze design patterns and styling architecture") 
    print("   3. Create visual reference documentation")
    print("   4. Develop reskinning and customization strategies")
    print("")
    
    try:
        result = AgentOrange().crew().kickoff(inputs=inputs)
        
        print("\n✅ Agent Orange analysis complete!")
        print("📁 Check these locations for results:")
        print("   • raw_materials/github_sources/ - Extracted source files")
        print("   • refined_materials/visual_reference/ - Visual documentation")
        print("   • refined_materials/cloudscape_reskinning_strategy.md - Strategy guide")
        
        return result
        
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        AgentOrange().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgentOrange().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        AgentOrange().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
