#!/usr/bin/env python
import sys
import warnings
import os
import yaml
from pathlib import Path
import glob
import json
from datetime import datetime

from .crew import SoylentRedDivision

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew with user-provided inputs.
    Usage: crewai run "content to write about" or provide content file path
    """
    if len(sys.argv) < 2:
        content_input = input("Enter content requirements or file path: ")
    else:
        content_input = " ".join(sys.argv[1:])
    
    # Check if input is a file path
    if content_input.endswith('.txt') or content_input.endswith('.md') or content_input.endswith('.yaml'):
        file_path = Path(content_input).resolve()
        if file_path.exists():
            inputs = process_content_file(str(file_path))
        else:
            # Treat as direct content requirements
            inputs = {
                'requirements': content_input,
                'title': 'Content Writing Task',
                'context': 'User-provided content requirements'
            }
    else:
        # Direct content requirements
        inputs = {
            'requirements': content_input,
            'title': 'Content Writing Task',
            'context': 'User-provided content requirements'
        }
    
    try:
        crew_instance = SoylentRedDivision()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Dynamic output path
        output_dir = crew_instance.project_root / "output"
        output_file = output_dir / "written_content.md"
        
        print(f"\n✅ Content completed successfully!")
        print(f"📄 Output saved to: {output_file}")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def process_content_file(file_path):
    """Process content file and extract requirements."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        raise Exception(f"Error reading content file: {e}")
    
    filename = Path(file_path).name
    
    # Check if it's a YAML file with structured inputs
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        try:
            config = yaml.safe_load(content)
            inputs = {
                'title': config.get('title', 'Writing Task'),
                'context': config.get('context', ''),
                'requirements': config.get('requirements', ''),
                'audience': config.get('audience', ''),
                'format': config.get('format', ''),
                'raw_content': config.get('raw_content', ''),
                'source_filename': filename
            }
        except yaml.YAMLError:
            # If YAML parsing fails, treat as text
            inputs = {
                'requirements': content,
                'title': 'Writing Task',
                'context': f'Content from {filename}',
                'raw_content': content,
                'source_filename': filename
            }
    else:
        # Text or markdown file
        inputs = {
            'requirements': content,
            'title': 'Writing Task', 
            'context': f'Content from {filename}',
            'raw_content': content,
            'source_filename': filename
        }
    
    return inputs

def train():
    """
    Train the crew for a given number of iterations.
    """
    if len(sys.argv) < 4:
        print("Usage: crewai train <iterations> <filename> \"<requirements>\"")
        return
        
    inputs = {
        "requirements": sys.argv[3] if len(sys.argv) > 3 else "Sample writing requirements"
    }
    try:
        SoylentRedDivision().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

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
        SoylentRedDivision().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    if len(sys.argv) < 4:
        print("Usage: crewai test <iterations> <eval_llm> \"<requirements>\"")
        return
        
    inputs = {
        "requirements": sys.argv[3] if len(sys.argv) > 3 else "Test writing requirements"
    }
    
    try:
        SoylentRedDivision().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def brand_author_draft():
    """
    Create initial draft using brand_author collaborative process.
    Usage: brand_author_draft "path/to/materials/folder"
    """
    if len(sys.argv) < 2:
        materials_folder = input("Enter path to materials folder: ")
    else:
        materials_folder = " ".join(sys.argv[1:])
    
    materials_path = Path(materials_folder).resolve()
    
    if not materials_path.exists() or not materials_path.is_dir():
        raise FileNotFoundError(f"Materials folder not found: {materials_path}")
    
    # Look for source materials in the folder
    source_files = []
    for ext in ['*.md', '*.txt', '*.yaml', '*.yml']:
        source_files.extend(glob.glob(str(materials_path / ext)))
    
    if not source_files:
        print(f"Warning: No source materials found in {materials_path}")
        raw_content = ""
    else:
        # Combine content from all source files
        combined_content = ""
        for source_file in source_files:
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    combined_content += f"\n\n## Content from {Path(source_file).name}\n\n{content}"
            except Exception as e:
                print(f"Warning: Could not read {source_file}: {e}")
        raw_content = combined_content
    
    # Build inputs for initial draft
    inputs = {
        'source_folder': str(materials_path),
        'raw_content': raw_content,
        'title': materials_path.name.replace('_', ' ').replace('-', ' ').title(),
        'context': f'Materials from {materials_path.name}',
        'format': 'markdown'
    }
    
    try:
        crew_instance = SoylentRedDivision()
        brand_author_crew = crew_instance.brand_author_crew()
        result = brand_author_crew.kickoff(inputs=inputs)
        
        print(f"\n✅ Initial draft created successfully!")
        print(f"📁 Materials folder: {materials_path}")
        print(f"📄 Draft saved in materials folder as DRAFT_*.md")
        print(f"🔄 Ready for feedback. Use 'crewai feedback' to provide feedback and iterate.")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while creating the initial draft: {e}")

def feedback():
    """
    Provide feedback on a draft and create revised version.
    Usage: feedback "path/to/DRAFT_file.md" "Your feedback here"
    """
    if len(sys.argv) < 3:
        draft_path = input("Enter path to draft file: ")
        feedback_input = input("Enter your feedback: ")
    else:
        draft_path = sys.argv[1]
        feedback_input = " ".join(sys.argv[2:])
    
    draft_file = Path(draft_path).resolve()
    
    if not draft_file.exists():
        raise FileNotFoundError(f"Draft file not found: {draft_file}")
    
    # Read current draft to get context
    try:
        with open(draft_file, 'r', encoding='utf-8') as f:
            current_draft = f.read()
    except Exception as e:
        raise Exception(f"Error reading draft file: {e}")
    
    # Build revision history from draft headers
    revision_history = _extract_revision_history(current_draft)
    
    # Build inputs for feedback revision
    inputs = {
        'draft_path': str(draft_file),
        'author_feedback': feedback_input,
        'revision_history': revision_history,
        'current_draft': current_draft
    }
    
    try:
        crew_instance = SoylentRedDivision()
        feedback_crew = crew_instance.feedback_crew(
            feedback_input=feedback_input,
            draft_path=str(draft_file),
            revision_history=revision_history
        )
        result = feedback_crew.kickoff(inputs=inputs)
        
        print(f"\n✅ Draft revised based on feedback!")
        print(f"📄 Updated draft: {draft_file}")
        print(f"🔄 Provide more feedback with 'crewai feedback' or sign off with 'crewai signoff'")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while processing feedback: {e}")

def signoff():
    """
    Sign off on the final draft and prepare for personal editing.
    Usage: signoff "path/to/DRAFT_file.md" "approval message"
    """
    if len(sys.argv) < 3:
        draft_path = input("Enter path to final draft file: ")
        signoff_message = input("Enter sign-off confirmation: ")
    else:
        draft_path = sys.argv[1]
        signoff_message = " ".join(sys.argv[2:])
    
    draft_file = Path(draft_path).resolve()
    
    if not draft_file.exists():
        raise FileNotFoundError(f"Draft file not found: {draft_file}")
    
    # Build inputs for sign-off
    inputs = {
        'final_draft_path': str(draft_file),
        'signoff_confirmation': signoff_message
    }
    
    try:
        crew_instance = SoylentRedDivision()
        signoff_crew = crew_instance.signoff_crew(
            final_draft_path=str(draft_file),
            signoff_confirmation=signoff_message
        )
        result = signoff_crew.kickoff(inputs=inputs)
        
        print(f"\n✅ Draft approved and ready for personal editing!")
        print(f"📄 Final approved draft: {draft_file}")
        print(f"✏️ Ready for your personal editing phase")
        return result
    except Exception as e:
        raise Exception(f"An error occurred during sign-off: {e}")

def _extract_revision_history(draft_content: str) -> str:
    """Extract revision history from draft headers."""
    lines = draft_content.split('\n')
    history = []
    
    for line in lines[:10]:  # Check first 10 lines for headers
        if 'DRAFT' in line and ('REVISION' in line or 'INITIAL' in line):
            history.append(line.strip())
    
    return '\n'.join(history) if history else "No revision history found"

def memory_stats():
    """
    Display memory statistics for the current crew.
    Usage: memory_stats
    """
    try:
        crew_instance = SoylentRedDivision()
        
        # Get stats for brand_author (has admin access to all memory types)
        stats = crew_instance.memory_manager.get_memory_stats('brand_author')
        
        print("\n=== MEMORY STATISTICS ===")
        for memory_type, type_stats in stats.items():
            print(f"\n{memory_type.upper().replace('_', ' ')}:")
            print(f"  Total entries: {type_stats['total_entries']}")
            print(f"  Consolidation candidates: {type_stats['consolidation_candidates']}")
            print(f"  Average importance: {type_stats['average_importance']:.1f}/10")
            if type_stats['oldest_entry']:
                print(f"  Oldest entry: {type_stats['oldest_entry']}")
            if type_stats['newest_entry']:
                print(f"  Newest entry: {type_stats['newest_entry']}")
        
        return stats
    except Exception as e:
        raise Exception(f"An error occurred while getting memory stats: {e}")

def memory_consolidate():
    """
    Manually trigger memory consolidation.
    Usage: memory_consolidate [memory_type]
    """
    memory_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    if memory_type and memory_type not in ['crew_shared', 'agent_specific', 'external_consolidated']:
        print("Invalid memory type. Use: crew_shared, agent_specific, external_consolidated")
        return
    
    try:
        crew_instance = SoylentRedDivision()
        
        from .memory_manager import MemoryType
        mem_type = MemoryType(memory_type) if memory_type else None
        
        # Use brand_author role for admin access
        results = crew_instance.memory_manager.manual_consolidation('brand_author', mem_type)
        
        print(f"\n✅ Memory consolidation completed!")
        for memory_type, result in results.items():
            print(f"\n{memory_type.upper()}:")
            print(f"  Original entries: {result['original_count']}")
            print(f"  Consolidated entries: {result['consolidated_count']}")
            print(f"  Space saved: {result['space_saved']} entries")
        
        return results
    except Exception as e:
        raise Exception(f"An error occurred during memory consolidation: {e}")

def memory_search():
    """
    Search memory for specific content.
    Usage: memory_search "search query" [memory_type]
    """
    if len(sys.argv) < 3:
        query = input("Enter search query: ")
    else:
        query = sys.argv[2]
    
    memory_type = sys.argv[3] if len(sys.argv) > 3 else "all"
    
    try:
        crew_instance = SoylentRedDivision()
        
        if memory_type == "all":
            results = crew_instance.memory_manager.search_across_memories(
                agent_role='brand_author',
                query=query,
                limit=20
            )
            
            if not results:
                print("No memories found matching your query.")
                return
            
            print(f"\n=== SEARCH RESULTS FOR: '{query}' ===")
            for mem_type, memories in results.items():
                print(f"\n{mem_type.value.upper()} MEMORIES:")
                for memory in memories:
                    print(f"- [{memory.timestamp.strftime('%Y-%m-%d %H:%M')}] {memory.content}")
                    if memory.tags:
                        print(f"  Tags: {', '.join(memory.tags)}")
                    print(f"  Importance: {memory.importance}/10")
        else:
            from .memory_manager import MemoryType
            mem_type = MemoryType(memory_type)
            memories = crew_instance.memory_manager.retrieve_memory(
                agent_role='brand_author',
                memory_type=mem_type,
                query=query,
                limit=20
            )
            
            if not memories:
                print(f"No memories found in {memory_type} for your query.")
                return
            
            print(f"\n=== {memory_type.upper()} SEARCH RESULTS ===")
            for memory in memories:
                print(f"- [{memory.timestamp.strftime('%Y-%m-%d %H:%M')}] {memory.content}")
                if memory.tags:
                    print(f"  Tags: {', '.join(memory.tags)}")
                print(f"  Importance: {memory.importance}/10")
        
        return results if memory_type == "all" else memories
    except Exception as e:
        raise Exception(f"An error occurred during memory search: {e}")

def memory_export():
    """
    Export memory to a file.
    Usage: memory_export <memory_type> <output_file>
    """
    if len(sys.argv) < 4:
        print("Usage: memory_export <memory_type> <output_file>")
        print("Memory types: crew_shared, agent_specific, external_consolidated, session_temporary")
        return
    
    memory_type = sys.argv[2]
    output_file = sys.argv[3]
    
    try:
        crew_instance = SoylentRedDivision()
        
        from .memory_manager import MemoryType
        mem_type = MemoryType(memory_type)
        output_path = Path(output_file).resolve()
        
        success = crew_instance.memory_manager.export_memory(
            agent_role='brand_author',
            memory_type=mem_type,
            output_path=output_path
        )
        
        if success:
            print(f"\n✅ Memory exported successfully!")
            print(f"📄 Output file: {output_path}")
        else:
            print(f"❌ Export failed. Check the logs for details.")
        
        return success
    except Exception as e:
        raise Exception(f"An error occurred during memory export: {e}")

def memory_clear_session():
    """
    Clear temporary session memory.
    Usage: memory_clear_session
    """
    try:
        crew_instance = SoylentRedDivision()
        crew_instance.memory_manager.clear_session_memory()
        
        print(f"\n✅ Session memory cleared successfully!")
        return True
    except Exception as e:
        raise Exception(f"An error occurred while clearing session memory: {e}")

def knowledge_stats():
    """
    Display knowledge statistics for the current crew.
    Usage: knowledge_stats
    """
    try:
        crew_instance = SoylentRedDivision()
        
        # Get stats for brand_author (has access to all knowledge types)
        stats = crew_instance.knowledge_manager.get_knowledge_stats('brand_author')
        
        print("\n=== KNOWLEDGE STATISTICS ===")
        print(f"Total items in system: {stats['total_items']}")
        print(f"Accessible items: {stats['accessible_items']}")
        
        if stats['last_updated']:
            print(f"Last updated: {stats['last_updated']}")
        
        print("\n**By Knowledge Type:**")
        for kt, count in stats['by_type'].items():
            print(f"  {kt.replace('_', ' ').title()}: {count}")
        
        print("\n**By Status:**")
        for status, count in stats['by_status'].items():
            print(f"  {status.title()}: {count}")
        
        return stats
    except Exception as e:
        raise Exception(f"An error occurred while getting knowledge stats: {e}")

def knowledge_search():
    """
    Search knowledge for specific content.
    Usage: knowledge_search "search query" [knowledge_type]
    """
    if len(sys.argv) < 3:
        query = input("Enter search query: ")
    else:
        query = sys.argv[2]
    
    knowledge_type = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        crew_instance = SoylentRedDivision()
        
        from .knowledge_manager import KnowledgeType
        kt_enums = None
        if knowledge_type:
            try:
                kt_enums = [KnowledgeType(knowledge_type)]
            except ValueError:
                print(f"Invalid knowledge type: {knowledge_type}")
                print("Valid types: brand_foundation, personas, writing_examples, templates, user_preferences, contextual")
                return
        
        results = crew_instance.knowledge_manager.search_knowledge(
            agent_role='brand_author',
            query=query,
            knowledge_types=kt_enums,
            limit=20
        )
        
        if not results:
            print("No knowledge items found matching your query.")
            return
        
        print(f"\n=== KNOWLEDGE SEARCH RESULTS FOR: '{query}' ===")
        for item in results:
            print(f"\n**{item.title}** ({item.knowledge_type.value})")
            print(f"Version: {item.version} | Updated: {item.last_modified.strftime('%Y-%m-%d')}")
            if item.tags:
                print(f"Tags: {', '.join(item.tags)}")
            
            # Show content preview
            content_preview = item.content[:200]
            if len(item.content) > 200:
                content_preview += "..."
            print(f"Preview: {content_preview}")
            print(f"ID: {item.id}")
            print("---")
        
        return results
    except Exception as e:
        raise Exception(f"An error occurred during knowledge search: {e}")

def knowledge_get():
    """
    Get a specific knowledge item by ID.
    Usage: knowledge_get <item_id>
    """
    if len(sys.argv) < 3:
        item_id = input("Enter knowledge item ID: ")
    else:
        item_id = sys.argv[2]
    
    try:
        crew_instance = SoylentRedDivision()
        
        item = crew_instance.knowledge_manager.get_knowledge_item('brand_author', item_id)
        
        if not item:
            print(f"Knowledge item '{item_id}' not found.")
            return
        
        print(f"\n=== KNOWLEDGE ITEM: {item.title} ===")
        print(f"Type: {item.knowledge_type.value}")
        print(f"Version: {item.version}")
        print(f"Status: {item.status.value}")
        print(f"Last Modified: {item.last_modified.strftime('%Y-%m-%d %H:%M')}")
        if item.tags:
            print(f"Tags: {', '.join(item.tags)}")
        if item.dependencies:
            print(f"Dependencies: {', '.join(item.dependencies)}")
        print(f"\n**Content:**\n{item.content}")
        
        return item
    except Exception as e:
        raise Exception(f"An error occurred getting knowledge item: {e}")

def knowledge_validate():
    """
    Validate knowledge consistency.
    Usage: knowledge_validate
    """
    try:
        crew_instance = SoylentRedDivision()
        
        issues = crew_instance.knowledge_manager.validate_knowledge_consistency()
        
        if not any(issues.values()):
            print("✅ Knowledge validation passed - no issues found.")
            return True
        
        print("⚠️ KNOWLEDGE VALIDATION ISSUES FOUND:")
        
        for issue_type, issue_list in issues.items():
            if issue_list:
                print(f"\n**{issue_type.replace('_', ' ').title()}:**")
                for issue in issue_list:
                    print(f"  - {issue}")
        
        return issues
    except Exception as e:
        raise Exception(f"An error occurred during knowledge validation: {e}")

def knowledge_refresh():
    """
    Refresh knowledge from filesystem.
    Usage: knowledge_refresh
    """
    try:
        crew_instance = SoylentRedDivision()
        
        results = crew_instance.knowledge_manager.refresh_knowledge()
        
        print(f"\n✅ Knowledge refresh completed!")
        print(f"Items before: {results['items_before']}")
        print(f"Items after: {results['items_after']}")
        print(f"Items added/updated: {results['items_added']}")
        print(f"Refreshed at: {results['timestamp']}")
        
        # Also refresh brand knowledge in crew
        crew_instance.refresh_brand_knowledge()
        print("✅ Brand knowledge cache refreshed!")
        
        return results
    except Exception as e:
        raise Exception(f"An error occurred during knowledge refresh: {e}")

def knowledge_by_type():
    """
    Get all knowledge items of a specific type.
    Usage: knowledge_by_type <knowledge_type>
    """
    if len(sys.argv) < 3:
        print("Usage: knowledge_by_type <knowledge_type>")
        print("Knowledge types: brand_foundation, personas, writing_examples, templates, user_preferences, contextual")
        return
    
    knowledge_type = sys.argv[2]
    
    try:
        crew_instance = SoylentRedDivision()
        
        from .knowledge_manager import KnowledgeType
        try:
            kt_enum = KnowledgeType(knowledge_type)
        except ValueError:
            print(f"Invalid knowledge type: {knowledge_type}")
            print("Valid types: brand_foundation, personas, writing_examples, templates, user_preferences, contextual")
            return
        
        items = crew_instance.knowledge_manager.get_knowledge_by_type('brand_author', kt_enum)
        
        if not items:
            print(f"No {knowledge_type} items found.")
            return
        
        print(f"\n=== {knowledge_type.upper().replace('_', ' ')} ITEMS ===")
        for item in items:
            print(f"\n**{item.title}**")
            print(f"ID: {item.id} | Version: {item.version}")
            if item.tags:
                print(f"Tags: {', '.join(item.tags)}")
            
            # Show content preview for lists
            content_preview = item.content[:150]
            if len(item.content) > 150:
                content_preview += "..."
            print(f"Preview: {content_preview}")
            print("---")
        
        return items
    except Exception as e:
        raise Exception(f"An error occurred getting knowledge by type: {e}")

def reasoning_stats():
    """
    Display reasoning and planning statistics.
    Usage: reasoning_stats
    """
    try:
        crew_instance = SoylentRedDivision()
        
        stats = crew_instance.reasoning_engine.get_reasoning_stats()
        
        print("\n=== REASONING & PLANNING STATISTICS ===")
        print(f"Total Plans: {stats['total_plans']}")
        print(f"Total Decisions: {stats['total_decisions']}")
        print(f"Average Plan Duration: {stats['average_plan_duration']:.1f} minutes")
        print(f"Success Rate: {stats['success_rate']:.2%}")
        
        print("\n**Plans by Status:**")
        for status, count in stats['plans_by_status'].items():
            print(f"  {status.title()}: {count}")
        
        print("\n**Plans by Type:**")
        for plan_type, count in stats['plans_by_type'].items():
            print(f"  {plan_type.replace('_', ' ').title()}: {count}")
        
        print("\n**Decisions by Type:**")
        for decision_type, count in stats['decisions_by_type'].items():
            print(f"  {decision_type.replace('_', ' ').title()}: {count}")
        
        return stats
    except Exception as e:
        raise Exception(f"An error occurred getting reasoning stats: {e}")

def reasoning_plans():
    """
    List all execution plans.
    Usage: reasoning_plans [status]
    """
    status_filter = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        crew_instance = SoylentRedDivision()
        
        if status_filter:
            from .reasoning_engine import PlanStatus
            try:
                status_enum = PlanStatus(status_filter)
                plans = crew_instance.reasoning_engine.get_plans_by_status(status_enum)
            except ValueError:
                print(f"Invalid status: {status_filter}")
                print("Valid statuses: draft, active, paused, completed, failed, cancelled")
                return
        else:
            plans = list(crew_instance.reasoning_engine.plans.values())
        
        if not plans:
            print("No plans found.")
            return
        
        print(f"\n=== EXECUTION PLANS {'(' + status_filter.upper() + ')' if status_filter else ''} ===")
        for plan in plans:
            print(f"\n**{plan.title}** ({plan.plan_type})")
            print(f"ID: {plan.id} | Status: {plan.status.value}")
            print(f"Created: {plan.created_at.strftime('%Y-%m-%d %H:%M')} by {plan.created_by}")
            print(f"Duration: {plan.estimated_duration}min (est) | {plan.actual_duration}min (actual)")
            print(f"Steps: {len(plan.steps)} | Success Rate: {plan.success_rate:.2%}")
            print("---")
        
        return plans
    except Exception as e:
        raise Exception(f"An error occurred getting plans: {e}")

def reasoning_plan():
    """
    Get details of a specific execution plan.
    Usage: reasoning_plan <plan_id>
    """
    if len(sys.argv) < 3:
        plan_id = input("Enter plan ID: ")
    else:
        plan_id = sys.argv[2]
    
    try:
        crew_instance = SoylentRedDivision()
        
        plan = crew_instance.reasoning_engine.get_plan(plan_id)
        
        if not plan:
            print(f"Plan '{plan_id}' not found.")
            return
        
        print(f"\n=== EXECUTION PLAN DETAILS ===")
        print(f"ID: {plan.id}")
        print(f"Title: {plan.title}")
        print(f"Type: {plan.plan_type}")
        print(f"Status: {plan.status.value}")
        print(f"Created by: {plan.created_by}")
        print(f"Created: {plan.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Updated: {plan.updated_at.strftime('%Y-%m-%d %H:%M')}")
        
        print(f"\n**Duration:**")
        print(f"Estimated: {plan.estimated_duration} minutes")
        print(f"Actual: {plan.actual_duration} minutes")
        if plan.success_rate > 0:
            print(f"Success Rate: {plan.success_rate:.2%}")
        
        print(f"\n**Steps ({len(plan.steps)}):**")
        for i, step in enumerate(plan.steps, 1):
            from .reasoning_engine import StepStatus
            status_icon = "✓" if step.status == StepStatus.COMPLETED else "⏳" if step.status == StepStatus.IN_PROGRESS else "○"
            print(f"{status_icon} {i}. {step.title}")
            print(f"    Status: {step.status.value}")
            print(f"    Type: {step.step_type}")
            print(f"    Priority: {step.priority}/10")
            print(f"    Duration: {step.estimated_duration}min")
            
            if step.dependencies:
                print(f"    Dependencies: {len(step.dependencies)}")
            
            if step.started_at:
                print(f"    Started: {step.started_at.strftime('%Y-%m-%d %H:%M')}")
            if step.completed_at:
                print(f"    Completed: {step.completed_at.strftime('%Y-%m-%d %H:%M')}")
            
            print("")
        
        return plan
    except Exception as e:
        raise Exception(f"An error occurred getting plan details: {e}")

def reasoning_decisions():
    """
    Analyze decision patterns.
    Usage: reasoning_decisions
    """
    try:
        crew_instance = SoylentRedDivision()
        
        patterns = crew_instance.reasoning_engine.analyze_decision_patterns()
        
        if not patterns:
            print("No decision patterns found.")
            return
        
        print("\n=== DECISION PATTERNS ANALYSIS ===")
        
        print("\n**Most Common Decisions:**")
        for decision_type, count in patterns['most_common_decisions'].items():
            print(f"  {decision_type.replace('_', ' ').title()}: {count}")
        
        print("\n**Average Confidence by Decision Type:**")
        for decision_type, avg_confidence in patterns['decision_confidence_avg'].items():
            print(f"  {decision_type.replace('_', ' ').title()}: {avg_confidence:.2f}")
        
        print("\n**Context Patterns:**")
        for context_type, count in patterns['context_patterns'].items():
            print(f"  {context_type.replace('_', ' ').title()}: {count}")
        
        return patterns
    except Exception as e:
        raise Exception(f"An error occurred analyzing decision patterns: {e}")

def reasoning_integration_stats():
    """
    Display reasoning integration statistics.
    Usage: reasoning_integration_stats
    """
    try:
        crew_instance = SoylentRedDivision()
        
        stats = crew_instance.reasoning_integration.get_integration_stats('brand_author')
        
        print("\n=== REASONING INTEGRATION STATISTICS ===")
        print(f"Plans Created: {stats['plans_created']}")
        print(f"Decisions Made: {stats['decisions_made']}")
        print(f"Feedback Processed: {stats['feedback_processed']}")
        print(f"Adaptations Applied: {stats['adaptations_applied']}")
        print(f"Knowledge Utilization: {stats['knowledge_utilization']:.1f}%")
        print(f"Memory Utilization: {stats['memory_utilization']:.1f}%")
        
        return stats
    except Exception as e:
        raise Exception(f"An error occurred getting integration stats: {e}")

def reasoning_monitor():
    """
    Monitor execution of a specific plan.
    Usage: reasoning_monitor <plan_id>
    """
    if len(sys.argv) < 3:
        plan_id = input("Enter plan ID to monitor: ")
    else:
        plan_id = sys.argv[2]
    
    try:
        crew_instance = SoylentRedDivision()
        
        monitoring_data = crew_instance.reasoning_engine.monitor_plan_execution(plan_id)
        
        if 'error' in monitoring_data:
            print(f"Error: {monitoring_data['error']}")
            return
        
        print(f"\n=== PLAN EXECUTION MONITORING ===")
        print(f"Plan ID: {monitoring_data['plan_id']}")
        print(f"Status: {monitoring_data['status']}")
        
        # Progress information
        progress = monitoring_data['progress']
        print(f"\n**Progress:**")
        print(f"  Completion: {progress['completion_percentage']:.1f}%")
        print(f"  Completed Steps: {progress['completed_steps']}/{progress['total_steps']}")
        print(f"  In Progress: {progress['in_progress_steps']}")
        print(f"  Failed: {progress['failed_steps']}")
        print(f"  Remaining: {progress['steps_remaining']}")
        
        # Execution health
        health = monitoring_data['execution_health']
        print(f"\n**Execution Health:**")
        print(f"  Health Score: {health['health_score']}/100 ({health['status']})")
        if health['issues']:
            print(f"  Issues: {', '.join(health['issues'])}")
        
        # Bottlenecks
        bottlenecks = monitoring_data['bottlenecks']
        if bottlenecks:
            print(f"\n**Bottlenecks:**")
            for bottleneck in bottlenecks:
                print(f"  - {bottleneck['type']}: {bottleneck['step_title']}")
                if bottleneck['type'] == 'dependency_bottleneck':
                    print(f"    Blocked by: {len(bottleneck['blocking_dependencies'])} dependencies")
                elif bottleneck['type'] == 'duration_bottleneck':
                    print(f"    Runtime: {bottleneck['runtime']:.1f}min (est: {bottleneck['estimated_duration']}min)")
        
        # Recommendations
        recommendations = monitoring_data['recommendations']
        if recommendations:
            print(f"\n**Recommendations:**")
            for rec in recommendations:
                print(f"  - {rec['description']}")
        
        # Completion estimate
        completion = monitoring_data['estimated_completion']
        print(f"\n**Completion Estimate:**")
        print(f"  Estimated Time: {completion['completion_time']}")
        if 'estimated_completion' in completion:
            print(f"  Expected Completion: {completion['estimated_completion']}")
        
        # Quality metrics
        quality = monitoring_data['quality_metrics']
        print(f"\n**Quality Metrics:**")
        print(f"  Completion Rate: {quality['completion_rate']:.2%}")
        print(f"  Failure Rate: {quality['failure_rate']:.2%}")
        print(f"  Quality Score: {quality['quality_score']:.1f}/100")
        if quality['average_step_duration'] > 0:
            print(f"  Avg Step Duration: {quality['average_step_duration']:.1f}min")
        
        return monitoring_data
    except Exception as e:
        raise Exception(f"An error occurred monitoring plan: {e}")

def reasoning_adapt():
    """
    Adapt plan execution based on monitoring data.
    Usage: reasoning_adapt <plan_id> <adaptation_type> [options]
    """
    if len(sys.argv) < 4:
        print("Usage: reasoning_adapt <plan_id> <adaptation_type> [options]")
        print("Adaptation types: reschedule_step, add_parallel_step, modify_dependencies, adjust_priorities")
        print("                  extend_duration, skip_step, add_quality_check")
        return
    
    plan_id = sys.argv[2]
    adaptation_type = sys.argv[3]
    
    try:
        crew_instance = SoylentRedDivision()
        
        # Get adaptation data based on type
        if adaptation_type == 'reschedule_step':
            step_id = input("Enter step ID to reschedule: ")
            priority = input("Enter new priority (1-10): ")
            adaptation_data = {
                'step_id': step_id,
                'priority': int(priority) if priority else None
            }
        elif adaptation_type == 'extend_duration':
            step_id = input("Enter step ID to extend: ")
            additional_minutes = input("Enter additional minutes: ")
            adaptation_data = {
                'step_id': step_id,
                'additional_minutes': int(additional_minutes)
            }
        elif adaptation_type == 'skip_step':
            step_id = input("Enter step ID to skip: ")
            reason = input("Enter reason for skipping: ")
            adaptation_data = {
                'step_id': step_id,
                'reason': reason
            }
        elif adaptation_type == 'add_quality_check':
            target_step_id = input("Enter target step ID for quality check: ")
            adaptation_data = {
                'target_step_id': target_step_id,
                'check_type': 'quality_validation'
            }
        else:
            print(f"Adaptation type '{adaptation_type}' not supported in interactive mode.")
            print("Use the reasoning engine API directly for complex adaptations.")
            return
        
        success = crew_instance.reasoning_engine.adapt_plan_execution(
            plan_id, adaptation_type, adaptation_data
        )
        
        if success:
            print(f"\n✅ Plan adaptation successful!")
            print(f"Applied {adaptation_type} to plan {plan_id}")
        else:
            print(f"❌ Plan adaptation failed.")
            print(f"Could not apply {adaptation_type} to plan {plan_id}")
        
        return success
    except Exception as e:
        raise Exception(f"An error occurred adapting plan: {e}")

def validation_check():
    """
    Validate content for brand compliance and quality.
    Usage: validation_check <content_file> [personas]
    """
    if len(sys.argv) < 3:
        content_file = input("Enter path to content file: ")
    else:
        content_file = sys.argv[2]
    
    personas = sys.argv[3:] if len(sys.argv) > 3 else []
    
    content_path = Path(content_file).resolve()
    
    if not content_path.exists():
        print(f"Content file not found: {content_path}")
        return
    
    try:
        # Read content
        with open(content_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        crew_instance = SoylentRedDivision()
        
        # Run validation
        result = crew_instance.validation_engine.validate_content(
            content=content,
            target_personas=personas,
            content_id=content_path.stem
        )
        
        print(f"\n=== VALIDATION RESULTS ===")
        print(f"File: {content_path}")
        print(f"Status: {result.overall_status.value.upper()}")
        print(f"Score: {result.overall_score:.1f}/100")
        print(f"Issues: {len(result.issues)}")
        
        if result.overall_status.value == 'passed':
            print("\n✅ Content passed all validation checks!")
        else:
            print(f"\n⚠️ Validation {result.overall_status.value}")
            
            # Show critical and high issues
            from .validation_engine import ValidationSeverity
            critical_issues = [i for i in result.issues if i.severity == ValidationSeverity.CRITICAL]
            high_issues = [i for i in result.issues if i.severity == ValidationSeverity.HIGH]
            
            if critical_issues:
                print(f"\n🚨 Critical Issues ({len(critical_issues)}):")
                for issue in critical_issues:
                    print(f"  • {issue.message}")
                    if issue.suggestions:
                        print(f"    💡 {issue.suggestions[0]}")
            
            if high_issues:
                print(f"\n⚠️ High Priority Issues ({len(high_issues)}):")
                for issue in high_issues:
                    print(f"  • {issue.message}")
                    if issue.suggestions:
                        print(f"    💡 {issue.suggestions[0]}")
        
        if result.suggestions:
            print(f"\n**Recommendations:**")
            for suggestion in result.suggestions:
                print(f"  • {suggestion}")
        
        print(f"\nValidation ID: {result.id}")
        
        return result
    except Exception as e:
        raise Exception(f"An error occurred during validation: {e}")

def validation_stats():
    """
    Display validation system statistics.
    Usage: validation_stats
    """
    try:
        crew_instance = SoylentRedDivision()
        
        stats = crew_instance.validation_engine.get_validation_stats()
        
        print("\n=== VALIDATION SYSTEM STATISTICS ===")
        print(f"Total Validations: {stats['total_validations']}")
        print(f"Average Score: {stats['average_score']:.1f}/100")
        print(f"Pass Rate: {stats['pass_rate']:.1f}%")
        
        if stats['issues_by_type']:
            print(f"\n**Issues by Type:**")
            for issue_type, count in stats['issues_by_type'].items():
                print(f"  {issue_type.replace('_', ' ').title()}: {count}")
        
        if stats['issues_by_severity']:
            print(f"\n**Issues by Severity:**")
            for severity, count in stats['issues_by_severity'].items():
                print(f"  {severity.title()}: {count}")
        
        print(f"\n**System Health:**")
        if stats['pass_rate'] >= 80:
            print("  ✅ System performing well")
        elif stats['pass_rate'] >= 60:
            print("  ⚠️ System needs attention")
        else:
            print("  🚨 System requires immediate attention")
        
        return stats
    except Exception as e:
        raise Exception(f"An error occurred getting validation stats: {e}")

def validation_result():
    """
    Get detailed validation result by ID.
    Usage: validation_result <result_id>
    """
    if len(sys.argv) < 3:
        result_id = input("Enter validation result ID: ")
    else:
        result_id = sys.argv[2]
    
    try:
        crew_instance = SoylentRedDivision()
        
        result = crew_instance.validation_engine.get_validation_result(result_id)
        
        if not result:
            print(f"Validation result '{result_id}' not found.")
            return
        
        print(f"\n=== VALIDATION RESULT DETAILS ===")
        print(f"ID: {result.id}")
        print(f"Content ID: {result.content_id}")
        print(f"Status: {result.overall_status.value}")
        print(f"Score: {result.overall_score:.1f}/100")
        print(f"Validated: {result.validated_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Issues: {len(result.issues)}")
        
        if result.issues:
            print(f"\n**Issues by Type:**")
            
            from .validation_engine import ValidationType
            issues_by_type = {}
            for issue in result.issues:
                vt = issue.validation_type
                if vt not in issues_by_type:
                    issues_by_type[vt] = []
                issues_by_type[vt].append(issue)
            
            for validation_type, issues in issues_by_type.items():
                print(f"\n**{validation_type.value.replace('_', ' ').title()}:**")
                for issue in issues:
                    print(f"  • {issue.severity.value.upper()}: {issue.message}")
                    if issue.suggestions:
                        print(f"    💡 {issue.suggestions[0]}")
        
        if result.suggestions:
            print(f"\n**Overall Recommendations:**")
            for suggestion in result.suggestions:
                print(f"  • {suggestion}")
        
        return result
    except Exception as e:
        raise Exception(f"An error occurred getting validation result: {e}")

def validation_history():
    """
    Get validation history for content.
    Usage: validation_history <content_id>
    """
    if len(sys.argv) < 3:
        content_id = input("Enter content ID: ")
    else:
        content_id = sys.argv[2]
    
    try:
        crew_instance = SoylentRedDivision()
        
        history = crew_instance.validation_engine.get_content_validation_history(content_id)
        
        if not history:
            print(f"No validation history found for content '{content_id}'")
            return
        
        # Sort by date
        history.sort(key=lambda x: x.validated_at, reverse=True)
        
        print(f"\n=== VALIDATION HISTORY FOR {content_id} ===")
        print(f"Total validations: {len(history)}")
        
        for i, result in enumerate(history, 1):
            print(f"\n**Validation {i}:**")
            print(f"  ID: {result.id}")
            print(f"  Date: {result.validated_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"  Status: {result.overall_status.value}")
            print(f"  Score: {result.overall_score:.1f}/100")
            print(f"  Issues: {len(result.issues)}")
            
            if result.issues:
                from .validation_engine import ValidationSeverity
                critical = sum(1 for issue in result.issues if issue.severity == ValidationSeverity.CRITICAL)
                high = sum(1 for issue in result.issues if issue.severity == ValidationSeverity.HIGH)
                medium = sum(1 for issue in result.issues if issue.severity == ValidationSeverity.MEDIUM)
                low = sum(1 for issue in result.issues if issue.severity == ValidationSeverity.LOW)
                
                issue_summary = []
                if critical: issue_summary.append(f"{critical} critical")
                if high: issue_summary.append(f"{high} high")
                if medium: issue_summary.append(f"{medium} medium")
                if low: issue_summary.append(f"{low} low")
                
                print(f"    ({', '.join(issue_summary)})")
        
        # Show improvement trend
        if len(history) > 1:
            recent_score = history[0].overall_score
            oldest_score = history[-1].overall_score
            trend = recent_score - oldest_score
            
            print(f"\n**Improvement Trend:**")
            if trend > 0:
                print(f"  📈 Improved by {trend:.1f} points")
            elif trend < 0:
                print(f"  📉 Decreased by {abs(trend):.1f} points")
            else:
                print(f"  📊 No change in score")
        
        return history
    except Exception as e:
        raise Exception(f"An error occurred getting validation history: {e}")

if __name__ == '__main__':
    # Check for special commands
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        if command == 'brand_author_draft':
            brand_author_draft()
        elif command == 'feedback':
            feedback()
        elif command == 'signoff':
            signoff()
        elif command == 'memory_stats':
            memory_stats()
        elif command == 'memory_consolidate':
            memory_consolidate()
        elif command == 'memory_search':
            memory_search()
        elif command == 'memory_export':
            memory_export()
        elif command == 'memory_clear_session':
            memory_clear_session()
        elif command == 'knowledge_stats':
            knowledge_stats()
        elif command == 'knowledge_search':
            knowledge_search()
        elif command == 'knowledge_get':
            knowledge_get()
        elif command == 'knowledge_validate':
            knowledge_validate()
        elif command == 'knowledge_refresh':
            knowledge_refresh()
        elif command == 'knowledge_by_type':
            knowledge_by_type()
        elif command == 'reasoning_stats':
            reasoning_stats()
        elif command == 'reasoning_plans':
            reasoning_plans()
        elif command == 'reasoning_plan':
            reasoning_plan()
        elif command == 'reasoning_decisions':
            reasoning_decisions()
        elif command == 'reasoning_integration_stats':
            reasoning_integration_stats()
        elif command == 'reasoning_monitor':
            reasoning_monitor()
        elif command == 'reasoning_adapt':
            reasoning_adapt()
        elif command == 'validation_check':
            validation_check()
        elif command == 'validation_stats':
            validation_stats()
        elif command == 'validation_result':
            validation_result()
        elif command == 'validation_history':
            validation_history()
        else:
            # Default run behavior
            run()
    else:
        run()