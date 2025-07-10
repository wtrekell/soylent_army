"""
Integration Tests for Soylent Red Division
Tests the integration between memory, knowledge, reasoning, and validation systems
"""

import pytest
import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.soylent_red_division.memory_manager import MemoryManager, MemoryType
from src.soylent_red_division.knowledge_manager import KnowledgeManager, KnowledgeType
from src.soylent_red_division.reasoning_engine import ReasoningEngine, ReasoningContext, DecisionType
from src.soylent_red_division.validation_engine import ValidationEngine, ValidationType
from src.soylent_red_division.knowledge_memory_integration import KnowledgeMemoryIntegration
from src.soylent_red_division.reasoning_integration import ReasoningIntegration

class TestSystemIntegration:
    """Test suite for system integration"""
    
    def test_memory_knowledge_integration_basic(self, temp_project_root, sample_brand_foundation):
        """Test basic memory-knowledge integration"""
        # Initialize systems
        memory_manager = MemoryManager(temp_project_root)
        knowledge_manager = KnowledgeManager(temp_project_root)
        knowledge_manager.refresh_knowledge()
        
        integration = KnowledgeMemoryIntegration(knowledge_manager, memory_manager)
        
        # Store memory about knowledge usage
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Brand foundation used successfully for voice guidance',
            tags=['knowledge_usage', 'brand_foundation', 'success'],
            importance=8,
            metadata={'knowledge_type': 'brand_foundation', 'usage_context': 'content_creation'}
        )
        
        # Get knowledge with memory insights
        enhanced_knowledge = integration.get_knowledge_with_memory_insights(
            agent_role='brand_author',
            knowledge_type=KnowledgeType.BRAND_FOUNDATION
        )
        
        assert len(enhanced_knowledge) > 0
        # Should enhance knowledge items with usage insights
        for item in enhanced_knowledge:
            assert hasattr(item, 'usage_insights')
    
    def test_reasoning_memory_integration(self, temp_project_root):
        """Test reasoning-memory integration"""
        # Initialize systems
        memory_manager = MemoryManager(temp_project_root)
        knowledge_manager = KnowledgeManager(temp_project_root)
        reasoning_engine = ReasoningEngine(temp_project_root)
        
        integration = ReasoningIntegration(reasoning_engine, memory_manager, knowledge_manager)
        
        # Store memory about successful decision patterns
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Persona targeting for Adaptive Alex worked well with practical examples',
            tags=['decision_success', 'persona_targeting', 'adaptive_alex'],
            importance=9,
            metadata={'decision_type': 'persona_targeting', 'outcome': 'successful'}
        )
        
        # Create context-aware plan
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"type": "guide", "target_persona": "Adaptive Alex"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        plan = integration.create_context_aware_plan(
            agent_role='brand_author',
            plan_type='content_creation',
            base_requirements={"type": "guide", "target_persona": "Adaptive Alex"}
        )
        
        assert plan is not None
        assert plan.plan_type == 'content_creation'
        assert 'Adaptive Alex' in plan.reasoning_context.target_personas
    
    def test_reasoning_validation_integration(self, temp_project_root):
        """Test reasoning-validation integration"""
        # Initialize systems
        reasoning_engine = ReasoningEngine(temp_project_root)
        validation_engine = ValidationEngine(temp_project_root)
        
        # Create a content creation plan
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"type": "guide"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        
        # Check that validation steps are included in the plan
        validation_steps = [
            step for step in plan.steps 
            if 'validation' in step.step_type.lower()
        ]
        
        assert len(validation_steps) >= 1
        
        # Simulate validation in plan execution
        test_content = "Test content for validation integration"
        
        validation_result = validation_engine.validate_content(
            content=test_content,
            content_id="test_integration_content"
        )
        
        # Validation should integrate with reasoning for continuous improvement
        assert validation_result is not None
        assert validation_result.content_id == "test_integration_content"
    
    def test_memory_validation_learning(self, temp_project_root):
        """Test memory learning from validation results"""
        # Initialize systems
        memory_manager = MemoryManager(temp_project_root)
        validation_engine = ValidationEngine(temp_project_root)
        
        # Validate content and store results in memory
        good_content = """
        # Practical AI Integration Guide
        
        After testing 15 AI tools over 6 months, I've learned that successful integration 
        requires methodical experimentation and transparent documentation.
        
        [AUTHOR: add personal testing examples]
        
        The data shows that 73% of initial implementations require revision.
        """
        
        validation_result = validation_engine.validate_content(
            content=good_content,
            content_id="learning_test_good"
        )
        
        # Store validation insights in memory
        if validation_result.overall_score >= 80:
            memory_manager.store_memory(
                agent_role='brand_author',
                memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
                content=f'High-quality content pattern: methodical approach with data and transparency',
                tags=['validation_success', 'content_pattern', 'quality'],
                importance=9,
                metadata={
                    'validation_score': validation_result.overall_score,
                    'content_type': 'guide',
                    'success_factors': ['methodical_approach', 'data_inclusion', 'transparency']
                }
            )
        
        # Validate problematic content
        bad_content = """
        This revolutionary AI will transform everything and disrupt the industry!
        Magic algorithms will optimize synergies for maximum ROI.
        """
        
        bad_validation = validation_engine.validate_content(
            content=bad_content,
            content_id="learning_test_bad"
        )
        
        # Store failure patterns in memory
        if bad_validation.overall_score < 60:
            memory_manager.store_memory(
                agent_role='brand_author',
                memory_type=MemoryType.CREW_SHARED,
                content=f'Avoid hype language and buzzwords - leads to validation failures',
                tags=['validation_failure', 'prohibited_language', 'pattern'],
                importance=8,
                metadata={
                    'validation_score': bad_validation.overall_score,
                    'failure_reasons': ['prohibited_language', 'hype_terms']
                }
            )
        
        # Verify learning is captured in memory
        pattern_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            tags=['validation_failure', 'pattern']
        )
        
        assert len(pattern_memories) >= 1
    
    def test_knowledge_validation_feedback_loop(self, temp_project_root, sample_brand_foundation):
        """Test knowledge-validation feedback loop"""
        # Initialize systems
        knowledge_manager = KnowledgeManager(temp_project_root)
        validation_engine = ValidationEngine(temp_project_root)
        knowledge_manager.refresh_knowledge()
        
        # Get brand knowledge
        brand_items = knowledge_manager.get_knowledge_by_type(KnowledgeType.BRAND_FOUNDATION)
        assert len(brand_items) > 0
        
        # Create content that should align with brand knowledge
        brand_aligned_content = """
        # Testing AI Tools: A Methodical Approach
        
        After 6 months of systematic testing, here's what the data shows:
        
        ## The Methodical Experimenter Approach
        - 127 documented tests across 8 tools
        - Failure rate: 27% on first attempt
        - Iteration count: Average 2.3 revisions per tool
        
        ## Practical Education & Translation
        Here's how to apply these findings to your UX workflow:
        1. Start with one tool for research tasks
        2. Document what works and what doesn't
        3. Scale gradually based on evidence
        
        ## Transparent Practitioner Documentation
        [AUTHOR: add personal testing methodology]
        The complete testing log is available for review.
        
        ## Ethical Realist Considerations
        Bias detection was integrated from day one.
        User agency and control were primary considerations.
        """
        
        validation_result = validation_engine.validate_content(
            content=brand_aligned_content,
            content_id="brand_alignment_test"
        )
        
        # Should score highly for brand alignment
        assert validation_result.overall_score >= 70
        
        # Check that brand voice validation passes
        brand_voice_issues = [
            issue for issue in validation_result.issues
            if issue.validation_type == ValidationType.BRAND_VOICE
        ]
        
        # Should have minimal brand voice issues
        critical_brand_issues = [
            issue for issue in brand_voice_issues
            if issue.severity.value in ['critical', 'high']
        ]
        assert len(critical_brand_issues) <= 1
    
    def test_end_to_end_content_creation_workflow(self, temp_project_root, sample_brand_foundation, sample_writing_example):
        """Test complete end-to-end content creation workflow"""
        # Initialize all systems
        memory_manager = MemoryManager(temp_project_root)
        knowledge_manager = KnowledgeManager(temp_project_root)
        reasoning_engine = ReasoningEngine(temp_project_root)
        validation_engine = ValidationEngine(temp_project_root)
        
        knowledge_manager.refresh_knowledge()
        
        # Initialize integrations
        km_integration = KnowledgeMemoryIntegration(knowledge_manager, memory_manager)
        reasoning_integration = ReasoningIntegration(reasoning_engine, memory_manager, knowledge_manager)
        
        # Step 1: Create content creation plan
        plan = reasoning_integration.create_context_aware_plan(
            agent_role='brand_author',
            plan_type='content_creation',
            base_requirements={
                "type": "guide",
                "target_persona": "Adaptive Alex",
                "topic": "AI tool integration"
            }
        )
        
        assert plan is not None
        plan_id = plan.id
        
        # Step 2: Execute brand knowledge review step
        reasoning_engine.update_step_status(plan_id, plan.steps[0].id, reasoning_engine.StepStatus.IN_PROGRESS)
        
        # Get brand context (simulating agent knowledge review)
        brand_knowledge = knowledge_manager.get_knowledge_by_type(KnowledgeType.BRAND_FOUNDATION)
        assert len(brand_knowledge) > 0
        
        reasoning_engine.update_step_status(plan_id, plan.steps[0].id, reasoning_engine.StepStatus.COMPLETED)
        
        # Step 3: Make content structure decision
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"type": "guide", "target_persona": "Adaptive Alex"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        structure_decision = reasoning_engine.make_decision(DecisionType.CONTENT_STRUCTURE, context)
        assert structure_decision['decision'] == 'content_structure'
        
        # Step 4: Simulate content creation
        created_content = """
        # AI Tool Integration for UX Teams: A Practical Guide
        
        After testing 12 AI tools over 4 months in real UX workflows, here's a systematic approach that actually works.
        
        ## The Methodical Testing Approach
        - Tested each tool with identical design briefs
        - Documented response quality and time savings
        - Tracked integration success rates: 67% on first attempt
        
        ## Practical Implementation Strategy
        For mid-level UX designers ready to integrate AI:
        
        1. **Start Small**: Begin with research and ideation tools
        2. **Document Everything**: Track what works and what doesn't
        3. **Build Gradually**: Add tools only after proving value
        
        [AUTHOR: add specific tool testing examples]
        
        ## What Actually Worked
        - Tool A: 34% faster initial research (documented over 23 projects)
        - Tool B: 28% improvement in ideation quality scores
        - Tool C: Failed integration - removed after 2 weeks
        
        ## Ethical Integration Requirements
        Each tool was evaluated for bias implications before adoption.
        User control and transparency were non-negotiable requirements.
        All AI suggestions required human review and approval.
        
        ## Transparent Process Documentation
        Complete testing methodology and results are documented.
        Failure cases included for learning and improvement.
        """
        
        # Step 5: Validate content
        validation_result = validation_engine.validate_content(
            content=created_content,
            content_id="end_to_end_test",
            target_personas=["Adaptive Alex"]
        )
        
        # Should pass validation with good score
        assert validation_result.overall_score >= 75
        
        # Step 6: Store successful patterns in memory
        if validation_result.overall_score >= 80:
            memory_manager.store_memory(
                agent_role='brand_author',
                memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
                content='Successful content pattern: methodical testing + practical implementation + ethical integration',
                tags=['success_pattern', 'content_creation', 'brand_compliant'],
                importance=9,
                metadata={
                    'plan_id': plan_id,
                    'validation_score': validation_result.overall_score,
                    'target_persona': 'Adaptive Alex'
                }
            )
        
        # Step 7: Complete plan
        reasoning_engine.update_plan_status(plan_id, reasoning_engine.PlanStatus.COMPLETED)
        
        # Verify complete workflow
        completed_plan = reasoning_engine.get_plan(plan_id)
        assert completed_plan.status == reasoning_engine.PlanStatus.COMPLETED
        
        # Verify memory learning
        success_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
            tags=['success_pattern']
        )
        assert len(success_memories) >= 1
    
    def test_cross_system_error_handling(self, temp_project_root):
        """Test error handling across integrated systems"""
        # Initialize systems
        memory_manager = MemoryManager(temp_project_root)
        knowledge_manager = KnowledgeManager(temp_project_root)
        reasoning_engine = ReasoningEngine(temp_project_root)
        validation_engine = ValidationEngine(temp_project_root)
        
        # Test with invalid/empty inputs
        try:
            # Invalid memory storage
            result = memory_manager.store_memory(
                agent_role='invalid_role',
                memory_type=MemoryType.CREW_SHARED,
                content='Test content',
                tags=['test'],
                importance=5
            )
            assert result is False
            
            # Empty content validation
            validation_result = validation_engine.validate_content(
                content="",
                content_id="empty_test"
            )
            assert validation_result is not None
            
            # Nonexistent plan monitoring
            monitoring_data = reasoning_engine.monitor_plan_execution("nonexistent_plan")
            assert "error" in monitoring_data
            
        except Exception as e:
            # Should handle errors gracefully without crashing
            assert False, f"System integration should handle errors gracefully: {e}"
    
    def test_performance_integration(self, temp_project_root):
        """Test performance of integrated systems"""
        import time
        
        # Initialize all systems
        start_time = time.time()
        
        memory_manager = MemoryManager(temp_project_root)
        knowledge_manager = KnowledgeManager(temp_project_root)
        reasoning_engine = ReasoningEngine(temp_project_root)
        validation_engine = ValidationEngine(temp_project_root)
        
        initialization_time = time.time() - start_time
        
        # System initialization should be reasonable
        assert initialization_time < 5.0  # 5 seconds max
        
        # Test integrated operation performance
        start_time = time.time()
        
        # Quick workflow simulation
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"type": "guide"},
            brand_constraints={},
            target_personas=["Adaptive Alex"],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, "test_user")
        validation_result = validation_engine.validate_content(
            content="Test content for performance",
            content_id="performance_test"
        )
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Performance test memory',
            tags=['performance'],
            importance=5
        )
        
        operation_time = time.time() - start_time
        
        # Integrated operations should complete quickly
        assert operation_time < 3.0  # 3 seconds max
    
    def test_data_consistency_across_systems(self, temp_project_root):
        """Test data consistency across all systems"""
        # Initialize systems
        memory_manager = MemoryManager(temp_project_root)
        knowledge_manager = KnowledgeManager(temp_project_root)
        reasoning_engine = ReasoningEngine(temp_project_root)
        validation_engine = ValidationEngine(temp_project_root)
        
        # Create consistent test data
        test_content_id = "consistency_test_content"
        test_agent_role = "brand_author"
        
        # Store in memory
        memory_manager.store_memory(
            agent_role=test_agent_role,
            memory_type=MemoryType.CREW_SHARED,
            content=f'Content creation successful for {test_content_id}',
            tags=['content_creation', 'success'],
            importance=8,
            metadata={'content_id': test_content_id}
        )
        
        # Validate content
        validation_result = validation_engine.validate_content(
            content="Test content for consistency checking",
            content_id=test_content_id
        )
        
        # Create reasoning plan
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={"content_id": test_content_id},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = reasoning_engine.create_plan("content_creation", context, test_agent_role)
        
        # Verify data consistency
        # Memory should contain the stored content
        memories = memory_manager.retrieve_memory(
            agent_role=test_agent_role,
            memory_type=MemoryType.CREW_SHARED,
            tags=['content_creation']
        )
        assert len(memories) >= 1
        assert any(test_content_id in mem.metadata.get('content_id', '') for mem in memories)
        
        # Validation should have the result
        retrieved_validation = validation_engine.get_validation_result(validation_result.id)
        assert retrieved_validation is not None
        assert retrieved_validation.content_id == test_content_id
        
        # Reasoning should have the plan
        retrieved_plan = reasoning_engine.get_plan(plan.id)
        assert retrieved_plan is not None
        assert retrieved_plan.created_by == test_agent_role
    
    def test_scalability_with_multiple_operations(self, temp_project_root):
        """Test system scalability with multiple concurrent operations"""
        # Initialize systems
        memory_manager = MemoryManager(temp_project_root)
        knowledge_manager = KnowledgeManager(temp_project_root)
        reasoning_engine = ReasoningEngine(temp_project_root)
        validation_engine = ValidationEngine(temp_project_root)
        
        # Perform multiple operations to test scalability
        num_operations = 10
        
        for i in range(num_operations):
            # Memory operations
            memory_manager.store_memory(
                agent_role='brand_author',
                memory_type=MemoryType.CREW_SHARED,
                content=f'Scalability test memory {i}',
                tags=['scalability', 'test'],
                importance=5
            )
            
            # Validation operations
            validation_engine.validate_content(
                content=f"Test content {i} for scalability",
                content_id=f"scalability_test_{i}"
            )
            
            # Reasoning operations
            if i % 3 == 0:  # Create plans less frequently
                context = ReasoningContext(
                    task_type="content_creation",
                    content_requirements={"iteration": i},
                    brand_constraints={},
                    target_personas=[],
                    available_resources={},
                    success_criteria={}
                )
                reasoning_engine.create_plan("content_creation", context, f"test_user_{i}")
        
        # Verify all operations completed successfully
        all_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            tags=['scalability']
        )
        assert len(all_memories) >= num_operations
        
        stats = reasoning_engine.get_reasoning_stats()
        assert stats['total_plans'] >= num_operations // 3
        
        validation_stats = validation_engine.get_validation_stats()
        assert validation_stats['total_validations'] >= num_operations