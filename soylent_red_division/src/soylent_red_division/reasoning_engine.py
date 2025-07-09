"""
Reasoning Engine - Advanced reasoning and planning system for content creation
Handles multi-step planning, decision-making, and adaptive task execution
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import re
from collections import defaultdict

class ReasoningType(Enum):
    """Types of reasoning supported by the system"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    ITERATIVE = "iterative"
    ADAPTIVE = "adaptive"

class PlanStatus(Enum):
    """Status of plan execution"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StepStatus(Enum):
    """Status of individual plan steps"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"

class DecisionType(Enum):
    """Types of decisions the system can make"""
    CONTENT_STRUCTURE = "content_structure"
    PERSONA_TARGETING = "persona_targeting"
    TEMPLATE_SELECTION = "template_selection"
    REVISION_APPROACH = "revision_approach"
    BRAND_COMPLIANCE = "brand_compliance"
    TASK_PRIORITIZATION = "task_prioritization"

@dataclass
class ReasoningContext:
    """Context for reasoning operations"""
    task_type: str
    content_requirements: Dict[str, Any]
    brand_constraints: Dict[str, Any]
    target_personas: List[str]
    available_resources: Dict[str, Any]
    success_criteria: Dict[str, Any]
    time_constraints: Optional[Dict[str, Any]] = None
    quality_thresholds: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReasoningContext':
        """Create from dictionary"""
        return cls(**data)

@dataclass
class PlanStep:
    """Individual step in a plan"""
    id: str
    title: str
    description: str
    step_type: str
    dependencies: List[str]
    estimated_duration: int  # minutes
    priority: int  # 1-10
    status: StepStatus
    reasoning_type: ReasoningType
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    success_criteria: Dict[str, Any]
    failure_conditions: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'step_type': self.step_type,
            'dependencies': self.dependencies,
            'estimated_duration': self.estimated_duration,
            'priority': self.priority,
            'status': self.status.value,
            'reasoning_type': self.reasoning_type.value,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'success_criteria': self.success_criteria,
            'failure_conditions': self.failure_conditions,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlanStep':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            step_type=data['step_type'],
            dependencies=data['dependencies'],
            estimated_duration=data['estimated_duration'],
            priority=data['priority'],
            status=StepStatus(data['status']),
            reasoning_type=ReasoningType(data['reasoning_type']),
            inputs=data['inputs'],
            outputs=data['outputs'],
            success_criteria=data['success_criteria'],
            failure_conditions=data['failure_conditions'],
            metadata=data['metadata'],
            created_at=datetime.fromisoformat(data['created_at']),
            started_at=datetime.fromisoformat(data['started_at']) if data['started_at'] else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None
        )

@dataclass
class ExecutionPlan:
    """Complete execution plan with steps and metadata"""
    id: str
    title: str
    description: str
    plan_type: str
    status: PlanStatus
    steps: List[PlanStep]
    reasoning_context: ReasoningContext
    created_by: str
    created_at: datetime
    updated_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_duration: int = 0  # minutes
    actual_duration: int = 0  # minutes
    success_rate: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'plan_type': self.plan_type,
            'status': self.status.value,
            'steps': [step.to_dict() for step in self.steps],
            'reasoning_context': self.reasoning_context.to_dict(),
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'estimated_duration': self.estimated_duration,
            'actual_duration': self.actual_duration,
            'success_rate': self.success_rate,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExecutionPlan':
        """Create from dictionary"""
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            plan_type=data['plan_type'],
            status=PlanStatus(data['status']),
            steps=[PlanStep.from_dict(step_data) for step_data in data['steps']],
            reasoning_context=ReasoningContext.from_dict(data['reasoning_context']),
            created_by=data['created_by'],
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            started_at=datetime.fromisoformat(data['started_at']) if data['started_at'] else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None,
            estimated_duration=data.get('estimated_duration', 0),
            actual_duration=data.get('actual_duration', 0),
            success_rate=data.get('success_rate', 0.0),
            metadata=data.get('metadata', {})
        )

class DecisionFramework:
    """Framework for making context-aware decisions"""
    
    def __init__(self):
        self.decision_rules = {
            DecisionType.CONTENT_STRUCTURE: self._decide_content_structure,
            DecisionType.PERSONA_TARGETING: self._decide_persona_targeting,
            DecisionType.TEMPLATE_SELECTION: self._decide_template_selection,
            DecisionType.REVISION_APPROACH: self._decide_revision_approach,
            DecisionType.BRAND_COMPLIANCE: self._decide_brand_compliance,
            DecisionType.TASK_PRIORITIZATION: self._decide_task_prioritization
        }
        
        # Content structure decision matrix
        self.content_structure_matrix = {
            'guide': {'reasoning_type': ReasoningType.SEQUENTIAL, 'template': 'step_by_step'},
            'analysis': {'reasoning_type': ReasoningType.PARALLEL, 'template': 'comparative'},
            'narrative': {'reasoning_type': ReasoningType.ITERATIVE, 'template': 'storytelling'},
            'reference': {'reasoning_type': ReasoningType.CONDITIONAL, 'template': 'reference'},
            'tutorial': {'reasoning_type': ReasoningType.SEQUENTIAL, 'template': 'instructional'}
        }
    
    def make_decision(self, decision_type: DecisionType, context: ReasoningContext) -> Dict[str, Any]:
        """Make a decision based on type and context"""
        decision_func = self.decision_rules.get(decision_type)
        if not decision_func:
            raise ValueError(f"Unknown decision type: {decision_type}")
        
        return decision_func(context)
    
    def _decide_content_structure(self, context: ReasoningContext) -> Dict[str, Any]:
        """Decide on content structure based on context"""
        content_type = context.content_requirements.get('type', 'guide')
        
        # Use content structure matrix
        structure_info = self.content_structure_matrix.get(content_type, 
                                                          self.content_structure_matrix['guide'])
        
        # Consider target personas
        personas = context.target_personas
        if 'Strategic Sofia' in personas:
            structure_info['depth'] = 'strategic'
        elif 'Adaptive Alex' in personas:
            structure_info['depth'] = 'practical'
        elif 'Curious Casey' in personas:
            structure_info['depth'] = 'foundational'
        
        return {
            'decision': 'content_structure',
            'structure_type': content_type,
            'reasoning_type': structure_info['reasoning_type'],
            'template': structure_info['template'],
            'depth': structure_info.get('depth', 'balanced'),
            'confidence': 0.85
        }
    
    def _decide_persona_targeting(self, context: ReasoningContext) -> Dict[str, Any]:
        """Decide on persona targeting strategy"""
        personas = context.target_personas
        content_complexity = context.content_requirements.get('complexity', 'medium')
        
        # Primary persona selection
        primary_persona = None
        if content_complexity == 'high' and 'Strategic Sofia' in personas:
            primary_persona = 'Strategic Sofia'
        elif content_complexity == 'medium' and 'Adaptive Alex' in personas:
            primary_persona = 'Adaptive Alex'
        elif content_complexity == 'low' and 'Curious Casey' in personas:
            primary_persona = 'Curious Casey'
        else:
            primary_persona = personas[0] if personas else 'Adaptive Alex'
        
        return {
            'decision': 'persona_targeting',
            'primary_persona': primary_persona,
            'secondary_personas': [p for p in personas if p != primary_persona],
            'approach': 'layered_complexity',
            'confidence': 0.90
        }
    
    def _decide_template_selection(self, context: ReasoningContext) -> Dict[str, Any]:
        """Decide on template selection"""
        content_type = context.content_requirements.get('type', 'guide')
        format_req = context.content_requirements.get('format', 'markdown')
        
        template_mapping = {
            'guide': 'core_body_guide',
            'analysis': 'core_body_comparison',
            'narrative': 'core_body_narrative',
            'tutorial': 'core_body_guide',
            'reference': 'core_body_comparison'
        }
        
        selected_template = template_mapping.get(content_type, 'core_body_guide')
        
        return {
            'decision': 'template_selection',
            'template': selected_template,
            'format': format_req,
            'customizations': [],
            'confidence': 0.80
        }
    
    def _decide_revision_approach(self, context: ReasoningContext) -> Dict[str, Any]:
        """Decide on revision approach based on feedback"""
        feedback_type = context.content_requirements.get('feedback_type', 'general')
        revision_count = context.content_requirements.get('revision_count', 0)
        
        if revision_count == 0:
            approach = 'comprehensive'
        elif revision_count < 3:
            approach = 'targeted'
        else:
            approach = 'minimal'
        
        return {
            'decision': 'revision_approach',
            'approach': approach,
            'focus_areas': self._identify_focus_areas(feedback_type),
            'iteration_strategy': 'incremental',
            'confidence': 0.75
        }
    
    def _decide_brand_compliance(self, context: ReasoningContext) -> Dict[str, Any]:
        """Decide on brand compliance strategy"""
        brand_constraints = context.brand_constraints
        
        compliance_level = 'strict'  # Always strict for brand compliance
        validation_points = [
            'voice_characteristics',
            'persona_alignment',
            'value_integration',
            'authenticity_protection',
            'ethical_considerations'
        ]
        
        return {
            'decision': 'brand_compliance',
            'compliance_level': compliance_level,
            'validation_points': validation_points,
            'enforcement_strategy': 'mandatory',
            'confidence': 1.0
        }
    
    def _decide_task_prioritization(self, context: ReasoningContext) -> Dict[str, Any]:
        """Decide on task prioritization"""
        time_constraints = context.time_constraints or {}
        quality_thresholds = context.quality_thresholds or {}
        
        priority_factors = {
            'brand_compliance': 10,
            'content_quality': 8,
            'persona_targeting': 7,
            'template_adherence': 6,
            'time_efficiency': 5
        }
        
        return {
            'decision': 'task_prioritization',
            'priority_factors': priority_factors,
            'optimization_strategy': 'quality_first',
            'trade_offs': [],
            'confidence': 0.85
        }
    
    def _identify_focus_areas(self, feedback_type: str) -> List[str]:
        """Identify focus areas based on feedback type"""
        focus_mapping = {
            'general': ['content_quality', 'brand_alignment'],
            'structural': ['content_structure', 'template_adherence'],
            'voice': ['brand_voice', 'persona_targeting'],
            'technical': ['accuracy', 'detail_level'],
            'creative': ['engagement', 'creativity']
        }
        
        return focus_mapping.get(feedback_type, focus_mapping['general'])

class ReasoningEngine:
    """
    Advanced reasoning engine for content creation planning and execution
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.reasoning_cache_dir = project_root / "reasoning_cache"
        self.reasoning_cache_dir.mkdir(exist_ok=True)
        
        # Storage files
        self.plans_file = self.reasoning_cache_dir / "execution_plans.json"
        self.decisions_file = self.reasoning_cache_dir / "decisions_log.json"
        self.reasoning_log_file = self.reasoning_cache_dir / "reasoning_operations.log"
        
        # Initialize components
        self.decision_framework = DecisionFramework()
        self.plans: Dict[str, ExecutionPlan] = {}
        self.decision_log: List[Dict[str, Any]] = []
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Load existing data
        self._load_plans()
        self._load_decision_log()
        
        # Plan templates
        self.plan_templates = {
            'content_creation': self._create_content_creation_template,
            'revision_workflow': self._create_revision_workflow_template,
            'brand_validation': self._create_brand_validation_template,
            'collaborative_drafting': self._create_collaborative_drafting_template
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for reasoning operations"""
        logger = logging.getLogger("ReasoningEngine")
        if not logger.handlers:
            handler = logging.FileHandler(self.reasoning_log_file)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _load_plans(self):
        """Load execution plans from storage"""
        if not self.plans_file.exists():
            return
        
        try:
            with open(self.plans_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for plan_data in data:
                    plan = ExecutionPlan.from_dict(plan_data)
                    self.plans[plan.id] = plan
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.logger.error(f"Error loading plans: {e}")
    
    def _save_plans(self):
        """Save execution plans to storage"""
        try:
            with open(self.plans_file, 'w', encoding='utf-8') as f:
                json.dump([plan.to_dict() for plan in self.plans.values()], f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving plans: {e}")
    
    def _load_decision_log(self):
        """Load decision log from storage"""
        if not self.decisions_file.exists():
            return
        
        try:
            with open(self.decisions_file, 'r', encoding='utf-8') as f:
                self.decision_log = json.load(f)
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Error loading decision log: {e}")
    
    def _save_decision_log(self):
        """Save decision log to storage"""
        try:
            with open(self.decisions_file, 'w', encoding='utf-8') as f:
                json.dump(self.decision_log, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving decision log: {e}")
    
    def create_plan(self, plan_type: str, context: ReasoningContext, 
                   created_by: str) -> ExecutionPlan:
        """Create a new execution plan"""
        if plan_type not in self.plan_templates:
            raise ValueError(f"Unknown plan type: {plan_type}")
        
        plan_id = str(uuid.uuid4())
        template_func = self.plan_templates[plan_type]
        
        # Create plan from template
        plan = template_func(plan_id, context, created_by)
        
        # Store plan
        self.plans[plan_id] = plan
        self._save_plans()
        
        self.logger.info(f"Created plan {plan_id} of type {plan_type}")
        return plan
    
    def _create_content_creation_template(self, plan_id: str, context: ReasoningContext, 
                                        created_by: str) -> ExecutionPlan:
        """Create content creation plan template"""
        steps = []
        
        # Step 1: Brand Knowledge Review
        steps.append(PlanStep(
            id=f"{plan_id}_step_1",
            title="Brand Knowledge Review",
            description="Review brand foundation, personas, and writing examples",
            step_type="brand_review",
            dependencies=[],
            estimated_duration=10,
            priority=10,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.SEQUENTIAL,
            inputs={'context': context.to_dict()},
            outputs={'brand_context': None},
            success_criteria={'brand_knowledge_loaded': True},
            failure_conditions={'brand_access_denied': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        # Step 2: Content Structure Decision
        steps.append(PlanStep(
            id=f"{plan_id}_step_2",
            title="Content Structure Decision",
            description="Determine optimal content structure based on requirements",
            step_type="structure_decision",
            dependencies=[f"{plan_id}_step_1"],
            estimated_duration=5,
            priority=9,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.CONDITIONAL,
            inputs={'context': context.to_dict()},
            outputs={'structure_decision': None},
            success_criteria={'structure_selected': True},
            failure_conditions={'decision_conflicts': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        # Step 3: Content Creation
        steps.append(PlanStep(
            id=f"{plan_id}_step_3",
            title="Content Creation",
            description="Create content following brand guidelines and structure",
            step_type="content_creation",
            dependencies=[f"{plan_id}_step_2"],
            estimated_duration=45,
            priority=8,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.ITERATIVE,
            inputs={'structure_decision': None, 'brand_context': None},
            outputs={'content_draft': None},
            success_criteria={'content_created': True, 'brand_compliant': True},
            failure_conditions={'quality_threshold_missed': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        # Step 4: Content Validation
        steps.append(PlanStep(
            id=f"{plan_id}_step_4",
            title="Content Validation",
            description="Comprehensive validation including brand compliance and quality checks",
            step_type="content_validation",
            dependencies=[f"{plan_id}_step_3"],
            estimated_duration=15,
            priority=10,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.CONDITIONAL,
            inputs={'content_draft': None},
            outputs={'validation_results': None, 'validation_passed': None},
            success_criteria={'validation_passed': True, 'critical_issues_resolved': True},
            failure_conditions={'critical_validation_failures': True},
            metadata={'validation_types': ['brand_voice', 'authenticity', 'persona_alignment', 'ethical_integration']},
            created_at=datetime.now()
        ))
        
        # Step 5: Quality Assurance Gate
        steps.append(PlanStep(
            id=f"{plan_id}_step_5",
            title="Quality Assurance Gate",
            description="Final quality gate before publication",
            step_type="quality_gate",
            dependencies=[f"{plan_id}_step_4"],
            estimated_duration=5,
            priority=10,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.CONDITIONAL,
            inputs={'validation_results': None},
            outputs={'quality_approved': None},
            success_criteria={'quality_approved': True},
            failure_conditions={'quality_rejected': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        return ExecutionPlan(
            id=plan_id,
            title="Content Creation Plan",
            description="Complete content creation with brand compliance",
            plan_type="content_creation",
            status=PlanStatus.DRAFT,
            steps=steps,
            reasoning_context=context,
            created_by=created_by,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            estimated_duration=85,
            metadata={'template_version': '1.0'}
        )
    
    def _create_revision_workflow_template(self, plan_id: str, context: ReasoningContext, 
                                         created_by: str) -> ExecutionPlan:
        """Create revision workflow plan template"""
        steps = []
        
        # Step 1: Feedback Analysis
        steps.append(PlanStep(
            id=f"{plan_id}_step_1",
            title="Feedback Analysis",
            description="Analyze author feedback and identify revision requirements",
            step_type="feedback_analysis",
            dependencies=[],
            estimated_duration=15,
            priority=10,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.CONDITIONAL,
            inputs={'feedback': None, 'current_draft': None},
            outputs={'revision_plan': None},
            success_criteria={'feedback_understood': True},
            failure_conditions={'feedback_unclear': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        # Step 2: Revision Strategy
        steps.append(PlanStep(
            id=f"{plan_id}_step_2",
            title="Revision Strategy",
            description="Determine revision approach and priorities",
            step_type="revision_strategy",
            dependencies=[f"{plan_id}_step_1"],
            estimated_duration=10,
            priority=9,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.ADAPTIVE,
            inputs={'revision_plan': None},
            outputs={'strategy_decision': None},
            success_criteria={'strategy_defined': True},
            failure_conditions={'strategy_conflicts': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        # Step 3: Content Revision
        steps.append(PlanStep(
            id=f"{plan_id}_step_3",
            title="Content Revision",
            description="Implement revisions while maintaining brand compliance",
            step_type="content_revision",
            dependencies=[f"{plan_id}_step_2"],
            estimated_duration=30,
            priority=8,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.ITERATIVE,
            inputs={'strategy_decision': None, 'current_draft': None},
            outputs={'revised_content': None},
            success_criteria={'revisions_implemented': True, 'brand_maintained': True},
            failure_conditions={'revision_quality_issues': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        return ExecutionPlan(
            id=plan_id,
            title="Revision Workflow Plan",
            description="Systematic content revision with feedback integration",
            plan_type="revision_workflow",
            status=PlanStatus.DRAFT,
            steps=steps,
            reasoning_context=context,
            created_by=created_by,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            estimated_duration=55,
            metadata={'template_version': '1.0'}
        )
    
    def _create_brand_validation_template(self, plan_id: str, context: ReasoningContext, 
                                        created_by: str) -> ExecutionPlan:
        """Create brand validation plan template"""
        steps = []
        
        # Step 1: Voice Characteristics Check
        steps.append(PlanStep(
            id=f"{plan_id}_step_1",
            title="Voice Characteristics Validation",
            description="Validate content against brand voice characteristics",
            step_type="voice_validation",
            dependencies=[],
            estimated_duration=8,
            priority=10,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.SEQUENTIAL,
            inputs={'content': None},
            outputs={'voice_validation': None},
            success_criteria={'voice_aligned': True},
            failure_conditions={'voice_misaligned': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        # Step 2: Persona Targeting Check
        steps.append(PlanStep(
            id=f"{plan_id}_step_2",
            title="Persona Targeting Validation",
            description="Ensure content serves target personas effectively",
            step_type="persona_validation",
            dependencies=[],
            estimated_duration=5,
            priority=9,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.PARALLEL,
            inputs={'content': None, 'target_personas': None},
            outputs={'persona_validation': None},
            success_criteria={'persona_targeted': True},
            failure_conditions={'persona_mismatch': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        # Step 3: Authenticity Protection Check
        steps.append(PlanStep(
            id=f"{plan_id}_step_3",
            title="Authenticity Protection Validation",
            description="Ensure no fabricated personal experiences",
            step_type="authenticity_validation",
            dependencies=[],
            estimated_duration=3,
            priority=10,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.CONDITIONAL,
            inputs={'content': None},
            outputs={'authenticity_validation': None},
            success_criteria={'authenticity_protected': True},
            failure_conditions={'fabricated_experiences_found': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        return ExecutionPlan(
            id=plan_id,
            title="Brand Validation Plan",
            description="Comprehensive brand compliance validation",
            plan_type="brand_validation",
            status=PlanStatus.DRAFT,
            steps=steps,
            reasoning_context=context,
            created_by=created_by,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            estimated_duration=16,
            metadata={'template_version': '1.0'}
        )
    
    def _create_collaborative_drafting_template(self, plan_id: str, context: ReasoningContext, 
                                              created_by: str) -> ExecutionPlan:
        """Create collaborative drafting plan template"""
        steps = []
        
        # Step 1: Initial Draft Planning
        steps.append(PlanStep(
            id=f"{plan_id}_step_1",
            title="Initial Draft Planning",
            description="Plan initial draft approach and structure",
            step_type="draft_planning",
            dependencies=[],
            estimated_duration=15,
            priority=9,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.SEQUENTIAL,
            inputs={'source_materials': None, 'requirements': None},
            outputs={'draft_plan': None},
            success_criteria={'plan_created': True},
            failure_conditions={'insufficient_materials': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        # Step 2: Feedback Integration Loop
        steps.append(PlanStep(
            id=f"{plan_id}_step_2",
            title="Feedback Integration Loop",
            description="Iterative feedback integration and revision",
            step_type="feedback_loop",
            dependencies=[f"{plan_id}_step_1"],
            estimated_duration=60,
            priority=8,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.ITERATIVE,
            inputs={'draft_plan': None, 'feedback': None},
            outputs={'revised_draft': None},
            success_criteria={'feedback_integrated': True, 'author_satisfied': True},
            failure_conditions={'feedback_conflicts': True},
            metadata={'max_iterations': 5},
            created_at=datetime.now()
        ))
        
        # Step 3: Sign-off Preparation
        steps.append(PlanStep(
            id=f"{plan_id}_step_3",
            title="Sign-off Preparation",
            description="Prepare final draft for author sign-off",
            step_type="signoff_preparation",
            dependencies=[f"{plan_id}_step_2"],
            estimated_duration=10,
            priority=7,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.SEQUENTIAL,
            inputs={'revised_draft': None},
            outputs={'final_draft': None},
            success_criteria={'ready_for_signoff': True},
            failure_conditions={'quality_issues': True},
            metadata={},
            created_at=datetime.now()
        ))
        
        return ExecutionPlan(
            id=plan_id,
            title="Collaborative Drafting Plan",
            description="Complete collaborative drafting workflow",
            plan_type="collaborative_drafting",
            status=PlanStatus.DRAFT,
            steps=steps,
            reasoning_context=context,
            created_by=created_by,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            estimated_duration=85,
            metadata={'template_version': '1.0'}
        )
    
    def make_decision(self, decision_type: DecisionType, context: ReasoningContext) -> Dict[str, Any]:
        """Make a decision using the decision framework"""
        decision = self.decision_framework.make_decision(decision_type, context)
        
        # Log the decision
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'decision_type': decision_type.value,
            'context': context.to_dict(),
            'decision': decision,
            'reasoning_engine_version': '1.0'
        }
        
        self.decision_log.append(log_entry)
        self._save_decision_log()
        
        self.logger.info(f"Made decision: {decision_type.value}")
        return decision
    
    def get_plan(self, plan_id: str) -> Optional[ExecutionPlan]:
        """Get execution plan by ID"""
        return self.plans.get(plan_id)
    
    def get_plans_by_status(self, status: PlanStatus) -> List[ExecutionPlan]:
        """Get all plans with specified status"""
        return [plan for plan in self.plans.values() if plan.status == status]
    
    def get_plans_by_creator(self, creator: str) -> List[ExecutionPlan]:
        """Get all plans created by specified user"""
        return [plan for plan in self.plans.values() if plan.created_by == creator]
    
    def update_plan_status(self, plan_id: str, new_status: PlanStatus) -> bool:
        """Update plan status"""
        plan = self.plans.get(plan_id)
        if not plan:
            return False
        
        plan.status = new_status
        plan.updated_at = datetime.now()
        
        if new_status == PlanStatus.ACTIVE:
            plan.started_at = datetime.now()
        elif new_status == PlanStatus.COMPLETED:
            plan.completed_at = datetime.now()
            if plan.started_at:
                plan.actual_duration = int((plan.completed_at - plan.started_at).total_seconds() / 60)
        
        self._save_plans()
        return True
    
    def update_step_status(self, plan_id: str, step_id: str, new_status: StepStatus) -> bool:
        """Update step status"""
        plan = self.plans.get(plan_id)
        if not plan:
            return False
        
        step = next((s for s in plan.steps if s.id == step_id), None)
        if not step:
            return False
        
        step.status = new_status
        
        if new_status == StepStatus.IN_PROGRESS:
            step.started_at = datetime.now()
        elif new_status == StepStatus.COMPLETED:
            step.completed_at = datetime.now()
        
        plan.updated_at = datetime.now()
        self._save_plans()
        return True
    
    def get_reasoning_stats(self) -> Dict[str, Any]:
        """Get reasoning engine statistics"""
        stats = {
            'total_plans': len(self.plans),
            'plans_by_status': defaultdict(int),
            'plans_by_type': defaultdict(int),
            'total_decisions': len(self.decision_log),
            'decisions_by_type': defaultdict(int),
            'average_plan_duration': 0,
            'success_rate': 0
        }
        
        total_duration = 0
        completed_plans = 0
        successful_plans = 0
        
        for plan in self.plans.values():
            stats['plans_by_status'][plan.status.value] += 1
            stats['plans_by_type'][plan.plan_type] += 1
            
            if plan.status == PlanStatus.COMPLETED:
                completed_plans += 1
                total_duration += plan.actual_duration
                if plan.success_rate > 0.8:
                    successful_plans += 1
        
        if completed_plans > 0:
            stats['average_plan_duration'] = total_duration / completed_plans
            stats['success_rate'] = successful_plans / completed_plans
        
        for decision in self.decision_log:
            decision_type = decision.get('decision_type', 'unknown')
            stats['decisions_by_type'][decision_type] += 1
        
        return dict(stats)
    
    def get_plan_monitoring_data(self, plan_id: str) -> Dict[str, Any]:
        """Get comprehensive monitoring data for a plan"""
        return self.monitor_plan_execution(plan_id)
    
    def analyze_decision_patterns(self) -> Dict[str, Any]:
        """Analyze decision-making patterns"""
        if not self.decision_log:
            return {}
        
        patterns = {
            'most_common_decisions': defaultdict(int),
            'decision_confidence_avg': defaultdict(list),
            'decision_trends': [],
            'context_patterns': defaultdict(int)
        }
        
        for decision in self.decision_log:
            decision_type = decision.get('decision_type', 'unknown')
            patterns['most_common_decisions'][decision_type] += 1
            
            decision_result = decision.get('decision', {})
            confidence = decision_result.get('confidence', 0)
            patterns['decision_confidence_avg'][decision_type].append(confidence)
            
            # Analyze context patterns
            context = decision.get('context', {})
            task_type = context.get('task_type', 'unknown')
            patterns['context_patterns'][task_type] += 1
        
        # Calculate average confidence
        for decision_type, confidences in patterns['decision_confidence_avg'].items():
            patterns['decision_confidence_avg'][decision_type] = sum(confidences) / len(confidences)
        
        return dict(patterns)
    
    def monitor_plan_execution(self, plan_id: str) -> Dict[str, Any]:
        """Monitor plan execution and provide status updates"""
        plan = self.plans.get(plan_id)
        if not plan:
            return {'error': f'Plan {plan_id} not found'}
        
        monitoring_data = {
            'plan_id': plan_id,
            'status': plan.status.value,
            'progress': self._calculate_progress(plan),
            'execution_health': self._assess_execution_health(plan),
            'bottlenecks': self._identify_bottlenecks(plan),
            'recommendations': self._generate_recommendations(plan),
            'estimated_completion': self._estimate_completion(plan),
            'quality_metrics': self._assess_quality_metrics(plan)
        }
        
        return monitoring_data
    
    def adapt_plan_execution(self, plan_id: str, adaptation_type: str, 
                           adaptation_data: Dict[str, Any]) -> bool:
        """Adapt plan execution based on monitoring data"""
        plan = self.plans.get(plan_id)
        if not plan:
            return False
        
        adaptation_handlers = {
            'reschedule_step': self._reschedule_step,
            'add_parallel_step': self._add_parallel_step,
            'modify_dependencies': self._modify_dependencies,
            'adjust_priorities': self._adjust_priorities,
            'extend_duration': self._extend_duration,
            'skip_step': self._skip_step,
            'add_quality_check': self._add_quality_check
        }
        
        handler = adaptation_handlers.get(adaptation_type)
        if not handler:
            return False
        
        try:
            success = handler(plan, adaptation_data)
            if success:
                plan.updated_at = datetime.now()
                plan.metadata['adaptations'] = plan.metadata.get('adaptations', [])
                plan.metadata['adaptations'].append({
                    'type': adaptation_type,
                    'data': adaptation_data,
                    'timestamp': datetime.now().isoformat()
                })
                self._save_plans()
                self.logger.info(f"Adapted plan {plan_id} with {adaptation_type}")
            return success
        except Exception as e:
            self.logger.error(f"Error adapting plan {plan_id}: {e}")
            return False
    
    def _calculate_progress(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Calculate plan execution progress"""
        total_steps = len(plan.steps)
        completed_steps = sum(1 for step in plan.steps if step.status == StepStatus.COMPLETED)
        in_progress_steps = sum(1 for step in plan.steps if step.status == StepStatus.IN_PROGRESS)
        failed_steps = sum(1 for step in plan.steps if step.status == StepStatus.FAILED)
        
        return {
            'total_steps': total_steps,
            'completed_steps': completed_steps,
            'in_progress_steps': in_progress_steps,
            'failed_steps': failed_steps,
            'completion_percentage': (completed_steps / total_steps) * 100 if total_steps > 0 else 0,
            'steps_remaining': total_steps - completed_steps
        }
    
    def _assess_execution_health(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Assess the health of plan execution"""
        health_score = 100
        issues = []
        
        # Check for failed steps
        failed_steps = [step for step in plan.steps if step.status == StepStatus.FAILED]
        if failed_steps:
            health_score -= len(failed_steps) * 20
            issues.append(f"{len(failed_steps)} failed steps")
        
        # Check for blocked steps
        blocked_steps = [step for step in plan.steps if step.status == StepStatus.BLOCKED]
        if blocked_steps:
            health_score -= len(blocked_steps) * 15
            issues.append(f"{len(blocked_steps)} blocked steps")
        
        # Check for overdue steps
        overdue_steps = self._identify_overdue_steps(plan)
        if overdue_steps:
            health_score -= len(overdue_steps) * 10
            issues.append(f"{len(overdue_steps)} overdue steps")
        
        # Check for dependency violations
        dependency_issues = self._check_dependency_violations(plan)
        if dependency_issues:
            health_score -= len(dependency_issues) * 10
            issues.extend(dependency_issues)
        
        health_score = max(0, health_score)
        
        return {
            'health_score': health_score,
            'status': 'healthy' if health_score >= 80 else 'warning' if health_score >= 60 else 'critical',
            'issues': issues
        }
    
    def _identify_bottlenecks(self, plan: ExecutionPlan) -> List[Dict[str, Any]]:
        """Identify bottlenecks in plan execution"""
        bottlenecks = []
        
        # Look for steps with many dependencies waiting
        for step in plan.steps:
            if step.status == StepStatus.PENDING:
                blocking_deps = [dep for dep in step.dependencies 
                               if not self._is_step_completed(plan, dep)]
                if len(blocking_deps) > 2:
                    bottlenecks.append({
                        'type': 'dependency_bottleneck',
                        'step_id': step.id,
                        'step_title': step.title,
                        'blocking_dependencies': blocking_deps
                    })
        
        # Look for long-running steps
        for step in plan.steps:
            if step.status == StepStatus.IN_PROGRESS and step.started_at:
                runtime = (datetime.now() - step.started_at).total_seconds() / 60
                if runtime > step.estimated_duration * 1.5:
                    bottlenecks.append({
                        'type': 'duration_bottleneck',
                        'step_id': step.id,
                        'step_title': step.title,
                        'runtime': runtime,
                        'estimated_duration': step.estimated_duration
                    })
        
        return bottlenecks
    
    def _generate_recommendations(self, plan: ExecutionPlan) -> List[Dict[str, Any]]:
        """Generate recommendations for plan optimization"""
        recommendations = []
        
        # Check for parallelizable steps
        for step in plan.steps:
            if step.status == StepStatus.PENDING and not step.dependencies:
                similar_steps = [s for s in plan.steps 
                               if s.step_type == step.step_type and s.status == StepStatus.PENDING]
                if len(similar_steps) > 1:
                    recommendations.append({
                        'type': 'parallelize_steps',
                        'description': f'Consider parallelizing {len(similar_steps)} {step.step_type} steps',
                        'steps': [s.id for s in similar_steps]
                    })
        
        # Check for priority rebalancing
        high_priority_pending = [s for s in plan.steps 
                               if s.priority >= 8 and s.status == StepStatus.PENDING]
        if high_priority_pending:
            recommendations.append({
                'type': 'priority_focus',
                'description': f'Focus on {len(high_priority_pending)} high-priority pending steps',
                'steps': [s.id for s in high_priority_pending]
            })
        
        # Check for quality gates
        content_steps = [s for s in plan.steps if s.step_type == 'content_creation']
        quality_steps = [s for s in plan.steps if 'validation' in s.step_type]
        if len(content_steps) > len(quality_steps):
            recommendations.append({
                'type': 'add_quality_checks',
                'description': 'Consider adding more quality validation steps',
                'affected_steps': [s.id for s in content_steps]
            })
        
        return recommendations
    
    def _estimate_completion(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Estimate plan completion time"""
        remaining_steps = [step for step in plan.steps 
                         if step.status in [StepStatus.PENDING, StepStatus.IN_PROGRESS]]
        
        if not remaining_steps:
            return {'completion_time': 'Already completed', 'estimated_minutes': 0}
        
        # Calculate remaining time based on dependencies
        remaining_time = 0
        processed_steps = set()
        
        # Process steps in dependency order
        while remaining_steps:
            ready_steps = [step for step in remaining_steps 
                         if all(dep in processed_steps for dep in step.dependencies)]
            
            if not ready_steps:
                # Break circular dependencies
                ready_steps = [remaining_steps[0]]
            
            # Process ready steps (assuming some can run in parallel)
            batch_duration = max(step.estimated_duration for step in ready_steps)
            remaining_time += batch_duration
            
            for step in ready_steps:
                processed_steps.add(step.id)
                remaining_steps.remove(step)
        
        estimated_completion = datetime.now() + timedelta(minutes=remaining_time)
        
        return {
            'estimated_minutes': remaining_time,
            'estimated_completion': estimated_completion.strftime('%Y-%m-%d %H:%M'),
            'completion_time': f"{remaining_time} minutes"
        }
    
    def _assess_quality_metrics(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Assess quality metrics for the plan"""
        completed_steps = [step for step in plan.steps if step.status == StepStatus.COMPLETED]
        total_steps = len(plan.steps)
        
        quality_metrics = {
            'completion_rate': len(completed_steps) / total_steps if total_steps > 0 else 0,
            'failure_rate': len([s for s in plan.steps if s.status == StepStatus.FAILED]) / total_steps if total_steps > 0 else 0,
            'average_step_duration': 0,
            'duration_variance': 0,
            'quality_score': 0
        }
        
        if completed_steps:
            durations = []
            for step in completed_steps:
                if step.started_at and step.completed_at:
                    duration = (step.completed_at - step.started_at).total_seconds() / 60
                    durations.append(duration)
            
            if durations:
                quality_metrics['average_step_duration'] = sum(durations) / len(durations)
                mean_duration = quality_metrics['average_step_duration']
                quality_metrics['duration_variance'] = sum((d - mean_duration) ** 2 for d in durations) / len(durations)
        
        # Calculate overall quality score
        quality_score = 100
        quality_score -= quality_metrics['failure_rate'] * 50
        quality_score -= min(quality_metrics['duration_variance'], 20)
        quality_metrics['quality_score'] = max(0, quality_score)
        
        return quality_metrics
    
    def _identify_overdue_steps(self, plan: ExecutionPlan) -> List[PlanStep]:
        """Identify steps that are overdue"""
        overdue_steps = []
        current_time = datetime.now()
        
        for step in plan.steps:
            if step.status == StepStatus.IN_PROGRESS and step.started_at:
                runtime = (current_time - step.started_at).total_seconds() / 60
                if runtime > step.estimated_duration * 1.2:  # 20% buffer
                    overdue_steps.append(step)
        
        return overdue_steps
    
    def _check_dependency_violations(self, plan: ExecutionPlan) -> List[str]:
        """Check for dependency violations"""
        violations = []
        
        for step in plan.steps:
            if step.status == StepStatus.IN_PROGRESS:
                for dep_id in step.dependencies:
                    dep_step = next((s for s in plan.steps if s.id == dep_id), None)
                    if dep_step and dep_step.status != StepStatus.COMPLETED:
                        violations.append(f"Step {step.title} started but dependency {dep_step.title} not completed")
        
        return violations
    
    def _is_step_completed(self, plan: ExecutionPlan, step_id: str) -> bool:
        """Check if a step is completed"""
        step = next((s for s in plan.steps if s.id == step_id), None)
        return step and step.status == StepStatus.COMPLETED
    
    def _reschedule_step(self, plan: ExecutionPlan, data: Dict[str, Any]) -> bool:
        """Reschedule a step to a different time"""
        step_id = data.get('step_id')
        new_priority = data.get('priority')
        
        step = next((s for s in plan.steps if s.id == step_id), None)
        if not step:
            return False
        
        if new_priority is not None:
            step.priority = new_priority
        
        # Reset timing if step is rescheduled
        if step.status == StepStatus.IN_PROGRESS:
            step.status = StepStatus.PENDING
            step.started_at = None
        
        return True
    
    def _add_parallel_step(self, plan: ExecutionPlan, data: Dict[str, Any]) -> bool:
        """Add a parallel step to the plan"""
        step_config = data.get('step_config', {})
        
        new_step = PlanStep(
            id=f"{plan.id}_parallel_{len(plan.steps) + 1}",
            title=step_config.get('title', 'Parallel Step'),
            description=step_config.get('description', ''),
            step_type=step_config.get('step_type', 'parallel_task'),
            dependencies=step_config.get('dependencies', []),
            estimated_duration=step_config.get('estimated_duration', 30),
            priority=step_config.get('priority', 5),
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.PARALLEL,
            inputs=step_config.get('inputs', {}),
            outputs=step_config.get('outputs', {}),
            success_criteria=step_config.get('success_criteria', {}),
            failure_conditions=step_config.get('failure_conditions', {}),
            metadata={'added_dynamically': True},
            created_at=datetime.now()
        )
        
        plan.steps.append(new_step)
        plan.estimated_duration += new_step.estimated_duration
        
        return True
    
    def _modify_dependencies(self, plan: ExecutionPlan, data: Dict[str, Any]) -> bool:
        """Modify step dependencies"""
        step_id = data.get('step_id')
        new_dependencies = data.get('dependencies', [])
        
        step = next((s for s in plan.steps if s.id == step_id), None)
        if not step:
            return False
        
        step.dependencies = new_dependencies
        
        return True
    
    def _adjust_priorities(self, plan: ExecutionPlan, data: Dict[str, Any]) -> bool:
        """Adjust step priorities"""
        priority_adjustments = data.get('adjustments', {})
        
        for step_id, new_priority in priority_adjustments.items():
            step = next((s for s in plan.steps if s.id == step_id), None)
            if step:
                step.priority = new_priority
        
        # Resort steps by priority
        plan.steps.sort(key=lambda s: s.priority, reverse=True)
        
        return True
    
    def _extend_duration(self, plan: ExecutionPlan, data: Dict[str, Any]) -> bool:
        """Extend step duration estimates"""
        step_id = data.get('step_id')
        additional_time = data.get('additional_minutes', 0)
        
        step = next((s for s in plan.steps if s.id == step_id), None)
        if not step:
            return False
        
        step.estimated_duration += additional_time
        plan.estimated_duration += additional_time
        
        return True
    
    def _skip_step(self, plan: ExecutionPlan, data: Dict[str, Any]) -> bool:
        """Skip a step in the plan"""
        step_id = data.get('step_id')
        reason = data.get('reason', 'Skipped by adaptation')
        
        step = next((s for s in plan.steps if s.id == step_id), None)
        if not step:
            return False
        
        step.status = StepStatus.SKIPPED
        step.metadata['skip_reason'] = reason
        step.completed_at = datetime.now()
        
        return True
    
    def _add_quality_check(self, plan: ExecutionPlan, data: Dict[str, Any]) -> bool:
        """Add a quality check step"""
        target_step_id = data.get('target_step_id')
        check_type = data.get('check_type', 'quality_validation')
        
        target_step = next((s for s in plan.steps if s.id == target_step_id), None)
        if not target_step:
            return False
        
        quality_step = PlanStep(
            id=f"{plan.id}_quality_{len(plan.steps) + 1}",
            title=f"Quality Check: {target_step.title}",
            description=f"Quality validation for {target_step.title}",
            step_type=check_type,
            dependencies=[target_step_id],
            estimated_duration=10,
            priority=9,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.CONDITIONAL,
            inputs={'target_output': None},
            outputs={'validation_result': None},
            success_criteria={'quality_passed': True},
            failure_conditions={'quality_failed': True},
            metadata={'added_dynamically': True, 'quality_check_for': target_step_id},
            created_at=datetime.now()
        )
        
        plan.steps.append(quality_step)
        plan.estimated_duration += quality_step.estimated_duration
        
        return True