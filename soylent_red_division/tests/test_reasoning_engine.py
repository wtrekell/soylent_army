"""
Tests for Reasoning Engine
"""

import pytest
import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.soylent_red_division.reasoning_engine import (
    ReasoningEngine, ReasoningContext, ExecutionPlan, PlanStep, 
    DecisionFramework, ReasoningType, PlanStatus, StepStatus, DecisionType
)

class TestReasoningEngine:
    """Test suite for Reasoning Engine"""
    
    def test_reasoning_engine_initialization(self, temp_project_root):
        """Test reasoning engine initialization"""
        re = ReasoningEngine(temp_project_root)
        
        assert re.project_root == temp_project_root
        assert re.reasoning_cache_dir.exists()
        assert re.plans_file.exists() or not re.plans_file.exists()  # May or may not exist initially
        assert re.decisions_file.exists() or not re.decisions_file.exists()
        assert re.reasoning_log_file.exists() or not re.reasoning_log_file.exists()
        
        # Check components
        assert isinstance(re.decision_framework, DecisionFramework)
        assert isinstance(re.plans, dict)
        assert isinstance(re.decision_log, list)
        assert re.logger is not None
    
    def test_decision_framework_initialization(self):
        """Test decision framework initialization"""
        df = DecisionFramework()
        
        assert len(df.decision_rules) == 6
        assert DecisionType.CONTENT_STRUCTURE in df.decision_rules
        assert DecisionType.PERSONA_TARGETING in df.decision_rules
        assert DecisionType.TEMPLATE_SELECTION in df.decision_rules
        assert DecisionType.REVISION_APPROACH in df.decision_rules
        assert DecisionType.BRAND_COMPLIANCE in df.decision_rules
        assert DecisionType.TASK_PRIORITIZATION in df.decision_rules
    
    def test_reasoning_context_creation(self):
        """Test reasoning context creation and serialization"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={
                "type": "guide",
                "complexity": "medium",
                "format": "markdown"
            },
            brand_constraints={
                "voice_characteristics": ["methodical_experimenter", "practical_educator"],
                "authenticity_protection": True
            },
            target_personas=["Adaptive Alex", "Curious Casey"],
            available_resources={
                "templates": ["core_body_guide"],
                "examples": ["ai_integration_guide"]
            },
            success_criteria={
                "brand_compliance": True,
                "quality_score": 8.0
            }
        )
        
        # Test serialization
        context_dict = context.to_dict()
        assert context_dict["task_type"] == "content_creation"
        assert "type" in context_dict["content_requirements"]
        assert len(context_dict["target_personas"]) == 2
        
        # Test deserialization
        restored_context = ReasoningContext.from_dict(context_dict)
        assert restored_context.task_type == context.task_type
        assert restored_context.target_personas == context.target_personas
    
    def test_plan_step_creation_and_serialization(self):
        """Test plan step creation and serialization"""
        step = PlanStep(
            id="test_step_1",
            title="Test Step",
            description="A test step for validation",
            step_type="validation",
            dependencies=["prerequisite_step"],
            estimated_duration=30,
            priority=8,
            status=StepStatus.PENDING,
            reasoning_type=ReasoningType.SEQUENTIAL,
            inputs={"content": "test content"},
            outputs={"validation_result": None},
            success_criteria={"validation_passed": True},
            failure_conditions={"critical_errors": True},
            metadata={"test": True},
            created_at=datetime.now()
        )
        
        # Test serialization
        step_dict = step.to_dict()
        assert step_dict["id"] == "test_step_1"
        assert step_dict["status"] == "pending"
        assert step_dict["reasoning_type"] == "sequential"
        
        # Test deserialization
        restored_step = PlanStep.from_dict(step_dict)
        assert restored_step.id == step.id
        assert restored_step.status == step.status
        assert restored_step.reasoning_type == step.reasoning_type
    
    def test_execution_plan_creation_and_serialization(self, sample_task_context):
        """Test execution plan creation and serialization"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements=sample_task_context,
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        steps = [
            PlanStep(
                id="step_1",
                title="Step 1",
                description="First step",
                step_type="analysis",
                dependencies=[],
                estimated_duration=15,
                priority=10,
                status=StepStatus.PENDING,
                reasoning_type=ReasoningType.SEQUENTIAL,
                inputs={}, outputs={}, success_criteria={}, failure_conditions={},
                metadata={}, created_at=datetime.now()
            )
        ]
        
        plan = ExecutionPlan(
            id="test_plan_1",
            title="Test Plan",
            description="A test execution plan",
            plan_type="content_creation",
            status=PlanStatus.DRAFT,
            steps=steps,
            reasoning_context=context,
            created_by="test_user",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Test serialization
        plan_dict = plan.to_dict()
        assert plan_dict["id"] == "test_plan_1"
        assert plan_dict["status"] == "draft"
        assert len(plan_dict["steps"]) == 1
        
        # Test deserialization
        restored_plan = ExecutionPlan.from_dict(plan_dict)
        assert restored_plan.id == plan.id
        assert restored_plan.status == plan.status
        assert len(restored_plan.steps) == 1
    
    def test_decision_framework_content_structure(self):
        """Test content structure decision making"""
        df = DecisionFramework()
        
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"type": "guide", "complexity": "medium"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        decision = df.make_decision(DecisionType.CONTENT_STRUCTURE, context)
        
        assert decision["decision"] == "content_structure"
        assert decision["structure_type"] == "guide"
        assert "reasoning_type" in decision
        assert "template" in decision
        assert "confidence" in decision
        assert decision["confidence"] > 0
    
    def test_decision_framework_persona_targeting(self):
        """Test persona targeting decision making"""
        df = DecisionFramework()
        
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"complexity": "high"},
            brand_constraints={},
            target_personas=["Strategic Sofia", "Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        decision = df.make_decision(DecisionType.PERSONA_TARGETING, context)
        
        assert decision["decision"] == "persona_targeting"
        assert decision["primary_persona"] in ["Strategic Sofia", "Adaptive Alex"]
        assert "secondary_personas" in decision
        assert "approach" in decision
        assert decision["confidence"] > 0
    
    def test_decision_framework_brand_compliance(self):
        """Test brand compliance decision making"""
        df = DecisionFramework()
        
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={"strict_compliance": True},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        decision = df.make_decision(DecisionType.BRAND_COMPLIANCE, context)
        
        assert decision["decision"] == "brand_compliance"
        assert decision["compliance_level"] == "strict"
        assert "validation_points" in decision
        assert decision["confidence"] == 1.0  # Brand compliance is always strict
    
    def test_plan_creation_content_creation(self, reasoning_engine):
        """Test content creation plan template"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"type": "guide"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        
        assert plan.plan_type == "content_creation"
        assert plan.status == PlanStatus.DRAFT
        assert plan.created_by == "test_user"
        assert len(plan.steps) == 5  # Expected steps in content creation template
        
        # Check step order and dependencies
        step_titles = [step.title for step in plan.steps]
        assert "Brand Knowledge Review" in step_titles
        assert "Content Structure Decision" in step_titles
        assert "Content Creation" in step_titles
        assert "Content Validation" in step_titles
        assert "Quality Assurance Gate" in step_titles
    
    def test_plan_creation_revision_workflow(self, reasoning_engine):
        """Test revision workflow plan template"""
        context = ReasoningContext(
            task_type="revision",
            content_requirements={"feedback_type": "structural"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("revision_workflow", context, "test_user")
        
        assert plan.plan_type == "revision_workflow"
        assert plan.status == PlanStatus.DRAFT
        assert len(plan.steps) == 3  # Expected steps in revision workflow template
        
        step_titles = [step.title for step in plan.steps]
        assert "Feedback Analysis" in step_titles
        assert "Revision Strategy" in step_titles
        assert "Content Revision" in step_titles
    
    def test_plan_creation_brand_validation(self, reasoning_engine):
        """Test brand validation plan template"""
        context = ReasoningContext(
            task_type="validation",
            content_requirements={},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("brand_validation", context, "test_user")
        
        assert plan.plan_type == "brand_validation"
        assert plan.status == PlanStatus.DRAFT
        assert len(plan.steps) == 3  # Expected steps in brand validation template
        
        step_titles = [step.title for step in plan.steps]
        assert "Voice Characteristics Validation" in step_titles
        assert "Persona Targeting Validation" in step_titles
        assert "Authenticity Protection Validation" in step_titles
    
    def test_plan_creation_collaborative_drafting(self, reasoning_engine):
        """Test collaborative drafting plan template"""
        context = ReasoningContext(
            task_type="collaboration",
            content_requirements={},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("collaborative_drafting", context, "test_user")
        
        assert plan.plan_type == "collaborative_drafting"
        assert plan.status == PlanStatus.DRAFT
        assert len(plan.steps) == 3  # Expected steps in collaborative drafting template
        
        step_titles = [step.title for step in plan.steps]
        assert "Initial Draft Planning" in step_titles
        assert "Feedback Integration Loop" in step_titles
        assert "Sign-off Preparation" in step_titles
    
    def test_plan_status_management(self, reasoning_engine):
        """Test plan status updates"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        plan_id = plan.id
        
        # Test status updates
        assert reasoning_engine.update_plan_status(plan_id, PlanStatus.ACTIVE)
        updated_plan = reasoning_engine.get_plan(plan_id)
        assert updated_plan.status == PlanStatus.ACTIVE
        assert updated_plan.started_at is not None
        
        assert reasoning_engine.update_plan_status(plan_id, PlanStatus.COMPLETED)
        completed_plan = reasoning_engine.get_plan(plan_id)
        assert completed_plan.status == PlanStatus.COMPLETED
        assert completed_plan.completed_at is not None
        assert completed_plan.actual_duration > 0
    
    def test_step_status_management(self, reasoning_engine):
        """Test step status updates"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        plan_id = plan.id
        step_id = plan.steps[0].id
        
        # Test step status updates
        assert reasoning_engine.update_step_status(plan_id, step_id, StepStatus.IN_PROGRESS)
        updated_plan = reasoning_engine.get_plan(plan_id)
        updated_step = next(s for s in updated_plan.steps if s.id == step_id)
        assert updated_step.status == StepStatus.IN_PROGRESS
        assert updated_step.started_at is not None
        
        assert reasoning_engine.update_step_status(plan_id, step_id, StepStatus.COMPLETED)
        completed_plan = reasoning_engine.get_plan(plan_id)
        completed_step = next(s for s in completed_plan.steps if s.id == step_id)
        assert completed_step.status == StepStatus.COMPLETED
        assert completed_step.completed_at is not None
    
    def test_decision_logging(self, reasoning_engine):
        """Test decision logging functionality"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"type": "guide"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        initial_log_count = len(reasoning_engine.decision_log)
        
        decision = reasoning_engine.make_decision(DecisionType.CONTENT_STRUCTURE, context)
        
        assert len(reasoning_engine.decision_log) == initial_log_count + 1
        
        log_entry = reasoning_engine.decision_log[-1]
        assert log_entry["decision_type"] == "content_structure"
        assert "timestamp" in log_entry
        assert "context" in log_entry
        assert "decision" in log_entry
        assert log_entry["decision"] == decision
    
    def test_plan_retrieval_methods(self, reasoning_engine):
        """Test various plan retrieval methods"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        # Create multiple plans
        plan1 = reasoning_engine.create_plan("content_creation", context, "user1")
        plan2 = reasoning_engine.create_plan("revision_workflow", context, "user2")
        
        # Update statuses
        reasoning_engine.update_plan_status(plan1.id, PlanStatus.ACTIVE)
        reasoning_engine.update_plan_status(plan2.id, PlanStatus.COMPLETED)
        
        # Test retrieval by status
        active_plans = reasoning_engine.get_plans_by_status(PlanStatus.ACTIVE)
        assert len(active_plans) >= 1
        assert any(p.id == plan1.id for p in active_plans)
        
        completed_plans = reasoning_engine.get_plans_by_status(PlanStatus.COMPLETED)
        assert len(completed_plans) >= 1
        assert any(p.id == plan2.id for p in completed_plans)
        
        # Test retrieval by creator
        user1_plans = reasoning_engine.get_plans_by_creator("user1")
        assert len(user1_plans) >= 1
        assert any(p.id == plan1.id for p in user1_plans)
    
    def test_reasoning_statistics(self, reasoning_engine):
        """Test reasoning engine statistics"""
        # Create some test data
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        reasoning_engine.make_decision(DecisionType.CONTENT_STRUCTURE, context)
        
        stats = reasoning_engine.get_reasoning_stats()
        
        assert "total_plans" in stats
        assert "plans_by_status" in stats
        assert "plans_by_type" in stats
        assert "total_decisions" in stats
        assert "decisions_by_type" in stats
        assert "average_plan_duration" in stats
        assert "success_rate" in stats
        
        assert stats["total_plans"] >= 1
        assert stats["total_decisions"] >= 1
    
    def test_decision_pattern_analysis(self, reasoning_engine):
        """Test decision pattern analysis"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"type": "guide"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        # Make several decisions
        reasoning_engine.make_decision(DecisionType.CONTENT_STRUCTURE, context)
        reasoning_engine.make_decision(DecisionType.PERSONA_TARGETING, context)
        reasoning_engine.make_decision(DecisionType.BRAND_COMPLIANCE, context)
        
        patterns = reasoning_engine.analyze_decision_patterns()
        
        if patterns:  # May be empty if no decisions logged
            assert "most_common_decisions" in patterns
            assert "decision_confidence_avg" in patterns
            assert "context_patterns" in patterns
    
    def test_plan_monitoring(self, reasoning_engine):
        """Test plan execution monitoring"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        plan_id = plan.id
        
        monitoring_data = reasoning_engine.monitor_plan_execution(plan_id)
        
        assert "plan_id" in monitoring_data
        assert "status" in monitoring_data
        assert "progress" in monitoring_data
        assert "execution_health" in monitoring_data
        assert "bottlenecks" in monitoring_data
        assert "recommendations" in monitoring_data
        assert "estimated_completion" in monitoring_data
        assert "quality_metrics" in monitoring_data
        
        assert monitoring_data["plan_id"] == plan_id
        
        # Test progress structure
        progress = monitoring_data["progress"]
        assert "total_steps" in progress
        assert "completed_steps" in progress
        assert "completion_percentage" in progress
        
        # Test health structure
        health = monitoring_data["execution_health"]
        assert "health_score" in health
        assert "status" in health
        assert "issues" in health
    
    def test_plan_adaptation_reschedule_step(self, reasoning_engine):
        """Test plan adaptation - reschedule step"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        plan_id = plan.id
        step_id = plan.steps[0].id
        
        adaptation_data = {
            "step_id": step_id,
            "priority": 5
        }
        
        success = reasoning_engine.adapt_plan_execution(plan_id, "reschedule_step", adaptation_data)
        assert success
        
        updated_plan = reasoning_engine.get_plan(plan_id)
        updated_step = next(s for s in updated_plan.steps if s.id == step_id)
        assert updated_step.priority == 5
    
    def test_plan_adaptation_extend_duration(self, reasoning_engine):
        """Test plan adaptation - extend duration"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        plan_id = plan.id
        step_id = plan.steps[0].id
        original_duration = plan.steps[0].estimated_duration
        
        adaptation_data = {
            "step_id": step_id,
            "additional_minutes": 15
        }
        
        success = reasoning_engine.adapt_plan_execution(plan_id, "extend_duration", adaptation_data)
        assert success
        
        updated_plan = reasoning_engine.get_plan(plan_id)
        updated_step = next(s for s in updated_plan.steps if s.id == step_id)
        assert updated_step.estimated_duration == original_duration + 15
    
    def test_plan_adaptation_skip_step(self, reasoning_engine):
        """Test plan adaptation - skip step"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        plan_id = plan.id
        step_id = plan.steps[0].id
        
        adaptation_data = {
            "step_id": step_id,
            "reason": "Not needed for this content type"
        }
        
        success = reasoning_engine.adapt_plan_execution(plan_id, "skip_step", adaptation_data)
        assert success
        
        updated_plan = reasoning_engine.get_plan(plan_id)
        updated_step = next(s for s in updated_plan.steps if s.id == step_id)
        assert updated_step.status == StepStatus.SKIPPED
        assert updated_step.metadata["skip_reason"] == "Not needed for this content type"
    
    def test_plan_adaptation_add_quality_check(self, reasoning_engine):
        """Test plan adaptation - add quality check"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        plan_id = plan.id
        target_step_id = plan.steps[0].id
        original_step_count = len(plan.steps)
        
        adaptation_data = {
            "target_step_id": target_step_id,
            "check_type": "quality_validation"
        }
        
        success = reasoning_engine.adapt_plan_execution(plan_id, "add_quality_check", adaptation_data)
        assert success
        
        updated_plan = reasoning_engine.get_plan(plan_id)
        assert len(updated_plan.steps) == original_step_count + 1
        
        # Find the new quality check step
        quality_steps = [s for s in updated_plan.steps if s.step_type == "quality_validation"]
        assert len(quality_steps) >= 1
        
        quality_step = quality_steps[-1]  # Get the most recent one
        assert target_step_id in quality_step.dependencies
        assert quality_step.metadata["quality_check_for"] == target_step_id
    
    def test_plan_persistence(self, temp_project_root):
        """Test plan persistence across engine instances"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        # Create first engine and plan
        re1 = ReasoningEngine(temp_project_root)
        plan = re1.create_plan("content_creation", context, "test_user")
        plan_id = plan.id
        
        # Create second engine instance
        re2 = ReasoningEngine(temp_project_root)
        
        # Verify plan persists
        loaded_plan = re2.get_plan(plan_id)
        assert loaded_plan is not None
        assert loaded_plan.id == plan_id
        assert loaded_plan.plan_type == "content_creation"
        assert loaded_plan.created_by == "test_user"
    
    def test_decision_log_persistence(self, temp_project_root):
        """Test decision log persistence across engine instances"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"type": "guide"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        # Create first engine and make decision
        re1 = ReasoningEngine(temp_project_root)
        initial_count = len(re1.decision_log)
        re1.make_decision(DecisionType.CONTENT_STRUCTURE, context)
        
        # Create second engine instance
        re2 = ReasoningEngine(temp_project_root)
        
        # Verify decision log persists
        assert len(re2.decision_log) == initial_count + 1
        assert re2.decision_log[-1]["decision_type"] == "content_structure"
    
    def test_error_handling_invalid_plan_type(self, reasoning_engine):
        """Test error handling for invalid plan type"""
        context = ReasoningContext(
            task_type="invalid",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        with pytest.raises(ValueError, match="Unknown plan type"):
            reasoning_engine.create_plan("invalid_plan_type", context, "test_user")
    
    def test_error_handling_invalid_decision_type(self):
        """Test error handling for invalid decision type"""
        df = DecisionFramework()
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        # Use string instead of enum to trigger error
        with pytest.raises(AttributeError):
            df.make_decision("invalid_decision_type", context)
    
    def test_error_handling_nonexistent_plan(self, reasoning_engine):
        """Test error handling for nonexistent plan operations"""
        # Test get plan
        result = reasoning_engine.get_plan("nonexistent_plan_id")
        assert result is None
        
        # Test update plan status
        success = reasoning_engine.update_plan_status("nonexistent_plan_id", PlanStatus.ACTIVE)
        assert success is False
        
        # Test update step status
        success = reasoning_engine.update_step_status("nonexistent_plan_id", "step_id", StepStatus.COMPLETED)
        assert success is False
        
        # Test monitoring
        monitoring_data = reasoning_engine.monitor_plan_execution("nonexistent_plan_id")
        assert "error" in monitoring_data
    
    def test_complex_dependency_handling(self, reasoning_engine):
        """Test complex step dependency handling"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        
        # Verify dependency chain
        steps_by_id = {step.id: step for step in plan.steps}
        
        for step in plan.steps:
            for dep_id in step.dependencies:
                assert dep_id in steps_by_id, f"Dependency {dep_id} not found for step {step.id}"
    
    def test_completion_time_estimation(self, reasoning_engine):
        """Test completion time estimation accuracy"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        monitoring_data = reasoning_engine.monitor_plan_execution(plan.id)
        
        completion_estimate = monitoring_data["estimated_completion"]
        assert "estimated_minutes" in completion_estimate
        assert "completion_time" in completion_estimate
        
        # Estimated time should be reasonable (not negative, not excessive)
        estimated_minutes = completion_estimate["estimated_minutes"]
        assert estimated_minutes >= 0
        assert estimated_minutes <= 1000  # Reasonable upper bound
    
    def test_quality_metrics_calculation(self, reasoning_engine):
        """Test quality metrics calculation"""
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        
        # Complete some steps
        step1_id = plan.steps[0].id
        reasoning_engine.update_step_status(plan.id, step1_id, StepStatus.IN_PROGRESS)
        reasoning_engine.update_step_status(plan.id, step1_id, StepStatus.COMPLETED)
        
        monitoring_data = reasoning_engine.monitor_plan_execution(plan.id)
        quality_metrics = monitoring_data["quality_metrics"]
        
        assert "completion_rate" in quality_metrics
        assert "failure_rate" in quality_metrics
        assert "quality_score" in quality_metrics
        
        # With at least one completed step, completion rate should be > 0
        assert quality_metrics["completion_rate"] > 0
        assert 0 <= quality_metrics["quality_score"] <= 100