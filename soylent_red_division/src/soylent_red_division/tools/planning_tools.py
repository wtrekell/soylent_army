"""
Planning Tools - Agent-accessible tools for reasoning and planning
"""

from typing import Dict, List, Any, Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from ..reasoning_engine import ReasoningEngine, ReasoningContext, DecisionType, PlanStatus, StepStatus
import json

class CreatePlanInput(BaseModel):
    """Input for creating execution plans"""
    plan_type: str = Field(..., description="Type of plan: content_creation, revision_workflow, brand_validation, collaborative_drafting")
    task_type: str = Field(..., description="Type of task being planned")
    content_requirements: Dict[str, Any] = Field(..., description="Content requirements and specifications")
    target_personas: List[str] = Field(default=[], description="Target personas for the content")
    brand_constraints: Dict[str, Any] = Field(default={}, description="Brand constraints and requirements")
    success_criteria: Dict[str, Any] = Field(default={}, description="Success criteria for the plan")
    time_constraints: Optional[Dict[str, Any]] = Field(default=None, description="Time constraints if any")

class MakeDecisionInput(BaseModel):
    """Input for making decisions"""
    decision_type: str = Field(..., description="Type of decision: content_structure, persona_targeting, template_selection, revision_approach, brand_compliance, task_prioritization")
    task_type: str = Field(..., description="Type of task requiring decision")
    content_requirements: Dict[str, Any] = Field(..., description="Content requirements for decision context")
    target_personas: List[str] = Field(default=[], description="Target personas for the decision")
    brand_constraints: Dict[str, Any] = Field(default={}, description="Brand constraints affecting decision")
    additional_context: Dict[str, Any] = Field(default={}, description="Additional context for decision making")

class UpdatePlanInput(BaseModel):
    """Input for updating plan status"""
    plan_id: str = Field(..., description="ID of the plan to update")
    new_status: str = Field(..., description="New status: draft, active, paused, completed, failed, cancelled")

class UpdateStepInput(BaseModel):
    """Input for updating step status"""
    plan_id: str = Field(..., description="ID of the plan containing the step")
    step_id: str = Field(..., description="ID of the step to update")
    new_status: str = Field(..., description="New status: pending, in_progress, completed, failed, skipped, blocked")

class GetPlanInput(BaseModel):
    """Input for getting plan details"""
    plan_id: str = Field(..., description="ID of the plan to retrieve")

class AnalyzeTaskInput(BaseModel):
    """Input for task analysis"""
    task_description: str = Field(..., description="Description of the task to analyze")
    context: Dict[str, Any] = Field(default={}, description="Additional context for analysis")
    requirements: Dict[str, Any] = Field(default={}, description="Task requirements and constraints")

class CreatePlanTool(BaseTool):
    """Tool for creating execution plans"""
    name: str = "create_plan"
    description: str = "Create a structured execution plan for content creation tasks. Use this to break down complex tasks into manageable steps with dependencies and timelines."
    args_schema: type[BaseModel] = CreatePlanInput
    
    def __init__(self, reasoning_engine: ReasoningEngine, agent_role: str):
        super().__init__()
        self.reasoning_engine = reasoning_engine
        self.agent_role = agent_role
    
    def _run(self, plan_type: str, task_type: str, content_requirements: Dict[str, Any],
             target_personas: List[str] = None, brand_constraints: Dict[str, Any] = None,
             success_criteria: Dict[str, Any] = None, time_constraints: Dict[str, Any] = None) -> str:
        """Create an execution plan"""
        try:
            # Create reasoning context
            context = ReasoningContext(
                task_type=task_type,
                content_requirements=content_requirements,
                brand_constraints=brand_constraints or {},
                target_personas=target_personas or [],
                available_resources={},
                success_criteria=success_criteria or {},
                time_constraints=time_constraints,
                quality_thresholds={}
            )
            
            # Create plan
            plan = self.reasoning_engine.create_plan(plan_type, context, self.agent_role)
            
            # Format response
            formatted_plan = [f"=== EXECUTION PLAN CREATED ==="]
            formatted_plan.append(f"Plan ID: {plan.id}")
            formatted_plan.append(f"Title: {plan.title}")
            formatted_plan.append(f"Type: {plan.plan_type}")
            formatted_plan.append(f"Status: {plan.status.value}")
            formatted_plan.append(f"Estimated Duration: {plan.estimated_duration} minutes")
            formatted_plan.append(f"Created: {plan.created_at.strftime('%Y-%m-%d %H:%M')}")
            
            formatted_plan.append(f"\n**Steps ({len(plan.steps)}):**")
            for i, step in enumerate(plan.steps, 1):
                formatted_plan.append(f"{i}. {step.title}")
                formatted_plan.append(f"   Type: {step.step_type}")
                formatted_plan.append(f"   Duration: {step.estimated_duration}min")
                formatted_plan.append(f"   Priority: {step.priority}/10")
                formatted_plan.append(f"   Status: {step.status.value}")
                if step.dependencies:
                    formatted_plan.append(f"   Dependencies: {len(step.dependencies)}")
                formatted_plan.append("")
            
            return "\n".join(formatted_plan)
        
        except Exception as e:
            return f"Error creating plan: {e}"

class MakeDecisionTool(BaseTool):
    """Tool for making structured decisions"""
    name: str = "make_decision"
    description: str = "Make context-aware decisions for content creation tasks. Use this to get structured recommendations for content structure, persona targeting, templates, and more."
    args_schema: type[BaseModel] = MakeDecisionInput
    
    def __init__(self, reasoning_engine: ReasoningEngine, agent_role: str):
        super().__init__()
        self.reasoning_engine = reasoning_engine
        self.agent_role = agent_role
    
    def _run(self, decision_type: str, task_type: str, content_requirements: Dict[str, Any],
             target_personas: List[str] = None, brand_constraints: Dict[str, Any] = None,
             additional_context: Dict[str, Any] = None) -> str:
        """Make a decision using the reasoning framework"""
        try:
            # Convert string to enum
            try:
                dt_enum = DecisionType(decision_type)
            except ValueError:
                return f"Invalid decision type: {decision_type}. Valid types: content_structure, persona_targeting, template_selection, revision_approach, brand_compliance, task_prioritization"
            
            # Merge additional context
            merged_requirements = {**content_requirements, **(additional_context or {})}
            
            # Create reasoning context
            context = ReasoningContext(
                task_type=task_type,
                content_requirements=merged_requirements,
                brand_constraints=brand_constraints or {},
                target_personas=target_personas or [],
                available_resources={},
                success_criteria={}
            )
            
            # Make decision
            decision = self.reasoning_engine.make_decision(dt_enum, context)
            
            # Format response
            formatted_decision = [f"=== DECISION MADE ==="]
            formatted_decision.append(f"Decision Type: {decision_type}")
            formatted_decision.append(f"Confidence: {decision.get('confidence', 0):.2f}")
            formatted_decision.append(f"Timestamp: {decision.get('timestamp', 'N/A')}")
            
            formatted_decision.append(f"\n**Decision Details:**")
            for key, value in decision.items():
                if key not in ['decision', 'confidence', 'timestamp']:
                    if isinstance(value, list):
                        formatted_decision.append(f"{key}: {', '.join(map(str, value))}")
                    else:
                        formatted_decision.append(f"{key}: {value}")
            
            return "\n".join(formatted_decision)
        
        except Exception as e:
            return f"Error making decision: {e}"

class GetPlanTool(BaseTool):
    """Tool for retrieving plan details"""
    name: str = "get_plan"
    description: str = "Get details of an execution plan including steps, status, and progress. Use this to check on existing plans."
    args_schema: type[BaseModel] = GetPlanInput
    
    def __init__(self, reasoning_engine: ReasoningEngine, agent_role: str):
        super().__init__()
        self.reasoning_engine = reasoning_engine
        self.agent_role = agent_role
    
    def _run(self, plan_id: str) -> str:
        """Get plan details"""
        try:
            plan = self.reasoning_engine.get_plan(plan_id)
            
            if not plan:
                return f"Plan '{plan_id}' not found."
            
            # Format response
            formatted_plan = [f"=== PLAN DETAILS ==="]
            formatted_plan.append(f"ID: {plan.id}")
            formatted_plan.append(f"Title: {plan.title}")
            formatted_plan.append(f"Type: {plan.plan_type}")
            formatted_plan.append(f"Status: {plan.status.value}")
            formatted_plan.append(f"Created by: {plan.created_by}")
            formatted_plan.append(f"Created: {plan.created_at.strftime('%Y-%m-%d %H:%M')}")
            formatted_plan.append(f"Updated: {plan.updated_at.strftime('%Y-%m-%d %H:%M')}")
            
            # Duration info
            formatted_plan.append(f"\n**Duration:**")
            formatted_plan.append(f"Estimated: {plan.estimated_duration} minutes")
            formatted_plan.append(f"Actual: {plan.actual_duration} minutes")
            if plan.success_rate > 0:
                formatted_plan.append(f"Success Rate: {plan.success_rate:.2%}")
            
            # Steps
            formatted_plan.append(f"\n**Steps ({len(plan.steps)}):**")
            for i, step in enumerate(plan.steps, 1):
                status_icon = "✓" if step.status == StepStatus.COMPLETED else "⏳" if step.status == StepStatus.IN_PROGRESS else "○"
                formatted_plan.append(f"{status_icon} {i}. {step.title}")
                formatted_plan.append(f"    Status: {step.status.value}")
                formatted_plan.append(f"    Type: {step.step_type}")
                formatted_plan.append(f"    Priority: {step.priority}/10")
                formatted_plan.append(f"    Duration: {step.estimated_duration}min")
                
                if step.dependencies:
                    formatted_plan.append(f"    Dependencies: {len(step.dependencies)}")
                
                if step.started_at:
                    formatted_plan.append(f"    Started: {step.started_at.strftime('%Y-%m-%d %H:%M')}")
                if step.completed_at:
                    formatted_plan.append(f"    Completed: {step.completed_at.strftime('%Y-%m-%d %H:%M')}")
                
                formatted_plan.append("")
            
            return "\n".join(formatted_plan)
        
        except Exception as e:
            return f"Error getting plan: {e}"

class UpdatePlanTool(BaseTool):
    """Tool for updating plan status"""
    name: str = "update_plan"
    description: str = "Update the status of an execution plan. Use this to mark plans as active, completed, or failed."
    args_schema: type[BaseModel] = UpdatePlanInput
    
    def __init__(self, reasoning_engine: ReasoningEngine, agent_role: str):
        super().__init__()
        self.reasoning_engine = reasoning_engine
        self.agent_role = agent_role
    
    def _run(self, plan_id: str, new_status: str) -> str:
        """Update plan status"""
        try:
            # Convert string to enum
            try:
                status_enum = PlanStatus(new_status)
            except ValueError:
                return f"Invalid status: {new_status}. Valid statuses: draft, active, paused, completed, failed, cancelled"
            
            success = self.reasoning_engine.update_plan_status(plan_id, status_enum)
            
            if success:
                return f"✅ Plan {plan_id} status updated to: {new_status}"
            else:
                return f"❌ Failed to update plan {plan_id} - plan not found"
        
        except Exception as e:
            return f"Error updating plan: {e}"

class UpdateStepTool(BaseTool):
    """Tool for updating step status"""
    name: str = "update_step"
    description: str = "Update the status of a specific step in an execution plan. Use this to track progress through plan steps."
    args_schema: type[BaseModel] = UpdateStepInput
    
    def __init__(self, reasoning_engine: ReasoningEngine, agent_role: str):
        super().__init__()
        self.reasoning_engine = reasoning_engine
        self.agent_role = agent_role
    
    def _run(self, plan_id: str, step_id: str, new_status: str) -> str:
        """Update step status"""
        try:
            # Convert string to enum
            try:
                status_enum = StepStatus(new_status)
            except ValueError:
                return f"Invalid status: {new_status}. Valid statuses: pending, in_progress, completed, failed, skipped, blocked"
            
            success = self.reasoning_engine.update_step_status(plan_id, step_id, status_enum)
            
            if success:
                return f"✅ Step {step_id} status updated to: {new_status}"
            else:
                return f"❌ Failed to update step - plan or step not found"
        
        except Exception as e:
            return f"Error updating step: {e}"

class AnalyzeTaskTool(BaseTool):
    """Tool for analyzing task complexity and requirements"""
    name: str = "analyze_task"
    description: str = "Analyze a task to understand its complexity, requirements, and recommended approach. Use this before creating plans."
    args_schema: type[BaseModel] = AnalyzeTaskInput
    
    def __init__(self, reasoning_engine: ReasoningEngine, agent_role: str):
        super().__init__()
        self.reasoning_engine = reasoning_engine
        self.agent_role = agent_role
    
    def _run(self, task_description: str, context: Dict[str, Any] = None, 
             requirements: Dict[str, Any] = None) -> str:
        """Analyze task and provide recommendations"""
        try:
            # Simple task analysis based on description
            analysis = {
                'complexity': 'medium',
                'recommended_plan_type': 'content_creation',
                'estimated_duration': 60,
                'key_considerations': [],
                'recommended_personas': [],
                'potential_challenges': []
            }
            
            description_lower = task_description.lower()
            
            # Analyze complexity
            if any(keyword in description_lower for keyword in ['complex', 'comprehensive', 'detailed', 'extensive']):
                analysis['complexity'] = 'high'
                analysis['estimated_duration'] = 120
            elif any(keyword in description_lower for keyword in ['simple', 'basic', 'quick', 'brief']):
                analysis['complexity'] = 'low'
                analysis['estimated_duration'] = 30
            
            # Determine plan type
            if any(keyword in description_lower for keyword in ['revise', 'update', 'modify', 'change']):
                analysis['recommended_plan_type'] = 'revision_workflow'
            elif any(keyword in description_lower for keyword in ['collaborate', 'feedback', 'iterative']):
                analysis['recommended_plan_type'] = 'collaborative_drafting'
            elif any(keyword in description_lower for keyword in ['validate', 'check', 'verify']):
                analysis['recommended_plan_type'] = 'brand_validation'
            
            # Identify target personas
            if any(keyword in description_lower for keyword in ['strategic', 'senior', 'leadership']):
                analysis['recommended_personas'].append('Strategic Sofia')
            if any(keyword in description_lower for keyword in ['practical', 'implementation', 'hands-on']):
                analysis['recommended_personas'].append('Adaptive Alex')
            if any(keyword in description_lower for keyword in ['beginner', 'introduction', 'basics']):
                analysis['recommended_personas'].append('Curious Casey')
            
            # Identify considerations
            if 'brand' in description_lower:
                analysis['key_considerations'].append('Brand compliance critical')
            if any(keyword in description_lower for keyword in ['technical', 'code', 'implementation']):
                analysis['key_considerations'].append('Technical accuracy required')
            if any(keyword in description_lower for keyword in ['creative', 'innovative', 'experimental']):
                analysis['key_considerations'].append('Creative freedom needed')
            
            # Identify challenges
            if analysis['complexity'] == 'high':
                analysis['potential_challenges'].append('Complex task decomposition needed')
            if len(analysis['recommended_personas']) > 2:
                analysis['potential_challenges'].append('Multiple persona targeting required')
            
            # Format response
            formatted_analysis = [f"=== TASK ANALYSIS ==="]
            formatted_analysis.append(f"Task: {task_description}")
            formatted_analysis.append(f"Complexity: {analysis['complexity']}")
            formatted_analysis.append(f"Estimated Duration: {analysis['estimated_duration']} minutes")
            formatted_analysis.append(f"Recommended Plan Type: {analysis['recommended_plan_type']}")
            
            if analysis['recommended_personas']:
                formatted_analysis.append(f"\n**Recommended Personas:**")
                for persona in analysis['recommended_personas']:
                    formatted_analysis.append(f"- {persona}")
            
            if analysis['key_considerations']:
                formatted_analysis.append(f"\n**Key Considerations:**")
                for consideration in analysis['key_considerations']:
                    formatted_analysis.append(f"- {consideration}")
            
            if analysis['potential_challenges']:
                formatted_analysis.append(f"\n**Potential Challenges:**")
                for challenge in analysis['potential_challenges']:
                    formatted_analysis.append(f"- {challenge}")
            
            formatted_analysis.append(f"\n**Next Steps:**")
            formatted_analysis.append(f"1. Use 'create_plan' tool with type '{analysis['recommended_plan_type']}'")
            formatted_analysis.append(f"2. Include identified personas in target_personas")
            formatted_analysis.append(f"3. Set appropriate time constraints based on complexity")
            
            return "\n".join(formatted_analysis)
        
        except Exception as e:
            return f"Error analyzing task: {e}"

class PlanningStatsTool(BaseTool):
    """Tool for getting planning statistics"""
    name: str = "planning_stats"
    description: str = "Get statistics about planning and reasoning activities. Use this to understand planning patterns and effectiveness."
    args_schema: type[BaseModel] = BaseModel
    
    def __init__(self, reasoning_engine: ReasoningEngine, agent_role: str):
        super().__init__()
        self.reasoning_engine = reasoning_engine
        self.agent_role = agent_role
    
    def _run(self) -> str:
        """Get planning statistics"""
        try:
            stats = self.reasoning_engine.get_reasoning_stats()
            
            formatted_stats = ["=== PLANNING STATISTICS ==="]
            formatted_stats.append(f"Total Plans: {stats['total_plans']}")
            formatted_stats.append(f"Total Decisions: {stats['total_decisions']}")
            formatted_stats.append(f"Average Plan Duration: {stats['average_plan_duration']:.1f} minutes")
            formatted_stats.append(f"Success Rate: {stats['success_rate']:.2%}")
            
            formatted_stats.append("\n**Plans by Status:**")
            for status, count in stats['plans_by_status'].items():
                formatted_stats.append(f"  {status}: {count}")
            
            formatted_stats.append("\n**Plans by Type:**")
            for plan_type, count in stats['plans_by_type'].items():
                formatted_stats.append(f"  {plan_type}: {count}")
            
            formatted_stats.append("\n**Decisions by Type:**")
            for decision_type, count in stats['decisions_by_type'].items():
                formatted_stats.append(f"  {decision_type}: {count}")
            
            return "\n".join(formatted_stats)
        
        except Exception as e:
            return f"Error getting planning stats: {e}"

def create_planning_tools(reasoning_engine: ReasoningEngine, agent_role: str) -> List[BaseTool]:
    """Create planning tools for an agent"""
    return [
        CreatePlanTool(reasoning_engine, agent_role),
        MakeDecisionTool(reasoning_engine, agent_role),
        GetPlanTool(reasoning_engine, agent_role),
        UpdatePlanTool(reasoning_engine, agent_role),
        UpdateStepTool(reasoning_engine, agent_role),
        AnalyzeTaskTool(reasoning_engine, agent_role),
        PlanningStatsTool(reasoning_engine, agent_role)
    ]