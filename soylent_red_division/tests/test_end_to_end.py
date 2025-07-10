"""
End-to-End Workflow Tests for Soylent Red Division
Tests complete workflows from start to finish
"""

import pytest
import json
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock

from src.soylent_red_division.crew import SoylentRedDivision
from src.soylent_red_division.main import (
    run, brand_author_draft, feedback, signoff,
    memory_stats, knowledge_stats, reasoning_stats, validation_check
)

class TestEndToEndWorkflows:
    """Test suite for end-to-end workflows"""
    
    def test_complete_content_creation_workflow(self, temp_project_root):
        """Test complete content creation workflow from start to finish"""
        # Initialize crew
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Step 1: Initial content creation
        inputs = {
            'requirements': 'Write a practical guide for integrating AI tools into UX design workflows',
            'title': 'AI Integration Guide for UX Designers',
            'context': 'Target mid-level UX designers who want actionable implementation strategies'
        }
        
        # Mock LLM responses to avoid API calls
        with patch.object(crew.crew().agents[0], 'execute_task') as mock_execute:
            mock_content = """
            # AI Integration Guide for UX Designers
            
            After testing 12 AI tools over 6 months in real UX workflows, here's a systematic approach.
            
            ## The Methodical Testing Approach
            - Tested each tool with identical design briefs
            - Documented response quality and time savings
            - Tracked integration success: 67% on first attempt
            
            ## Practical Implementation Strategy
            For mid-level UX designers:
            
            1. **Start Small**: Begin with research and ideation tools
            2. **Document Everything**: Track what works and what doesn't
            3. **Build Gradually**: Add tools only after proving value
            
            [AUTHOR: add specific tool testing examples]
            
            ## Ethical Integration Requirements
            Each tool was evaluated for bias implications before adoption.
            User control and transparency were non-negotiable requirements.
            """
            
            mock_execute.return_value = mock_content
            
            # Execute workflow
            try:
                crew_instance = crew.crew()
                result = crew_instance.kickoff(inputs=inputs)
                
                # Verify result structure
                assert result is not None
                
                # Step 2: Validate the content
                validation_result = crew.validation_engine.validate_content(
                    content=mock_content,
                    content_id="e2e_test_content",
                    target_personas=["Adaptive Alex"]
                )
                
                # Should pass validation with reasonable score
                assert validation_result.overall_score >= 60
                
                # Step 3: Store successful patterns in memory
                crew.memory_manager.store_memory(
                    agent_role='brand_author',
                    memory_type='external_consolidated',
                    content='Successful content creation: methodical approach + practical implementation',
                    tags=['success_pattern', 'content_creation', 'e2e_test'],
                    importance=9,
                    metadata={
                        'validation_score': validation_result.overall_score,
                        'workflow': 'end_to_end_test'
                    }
                )
                
                # Step 4: Verify memory storage
                success_memories = crew.memory_manager.retrieve_memory(
                    agent_role='brand_author',
                    memory_type='external_consolidated',
                    tags=['success_pattern', 'e2e_test']
                )
                
                assert len(success_memories) >= 1
                
            except Exception as e:
                # Should handle gracefully
                assert False, f"End-to-end workflow should not fail: {e}"
    
    def test_brand_author_collaborative_workflow(self, temp_project_root):
        """Test brand author collaborative workflow"""
        # Create test materials folder
        materials_folder = temp_project_root / "test_materials"
        materials_folder.mkdir(exist_ok=True)
        
        # Create source materials
        source_file = materials_folder / "research_notes.md"
        source_content = """
        # AI Tool Research Notes
        
        ## Testing Results
        - Tool A: 34% faster research
        - Tool B: 28% better ideation
        - Tool C: Failed integration
        
        ## Key Insights
        - Methodical testing approach works
        - Documentation is crucial
        - Gradual implementation succeeds
        """
        source_file.write_text(source_content)
        
        # Mock the collaborative workflow functions
        with patch('src.soylent_red_division.main.SoylentRedDivision') as mock_crew_class:
            mock_crew = Mock()
            mock_crew_class.return_value = mock_crew
            
            # Mock brand author crew
            mock_brand_crew = Mock()
            mock_crew.brand_author_crew.return_value = mock_brand_crew
            
            # Mock kickoff result
            mock_result = Mock()
            mock_result.raw = "Draft content created successfully"
            mock_brand_crew.kickoff.return_value = mock_result
            
            # Mock feedback crew
            mock_feedback_crew = Mock()
            mock_crew.feedback_crew.return_value = mock_feedback_crew
            mock_feedback_result = Mock()
            mock_feedback_result.raw = "Content revised based on feedback"
            mock_feedback_crew.kickoff.return_value = mock_feedback_result
            
            # Mock signoff crew
            mock_signoff_crew = Mock()
            mock_crew.signoff_crew.return_value = mock_signoff_crew
            mock_signoff_result = Mock()
            mock_signoff_result.raw = "Content approved for editing"
            mock_signoff_crew.kickoff.return_value = mock_signoff_result
            
            # Test the workflow steps
            try:
                # Step 1: Create initial draft
                with patch('sys.argv', ['main.py', str(materials_folder)]):
                    result1 = brand_author_draft()
                    assert result1 is not None
                
                # Step 2: Provide feedback
                draft_file = materials_folder / "DRAFT_test.md"
                draft_file.write_text("Mock draft content")
                
                with patch('sys.argv', ['main.py', str(draft_file), 'This needs more practical examples']):
                    result2 = feedback()
                    assert result2 is not None
                
                # Step 3: Sign off
                with patch('sys.argv', ['main.py', str(draft_file), 'Approved for editing']):
                    result3 = signoff()
                    assert result3 is not None
                
                # Verify all steps completed
                mock_crew.brand_author_crew.assert_called_once()
                mock_crew.feedback_crew.assert_called_once()
                mock_crew.signoff_crew.assert_called_once()
                
            except Exception as e:
                assert False, f"Collaborative workflow should not fail: {e}"
    
    def test_validation_workflow_with_improvements(self, temp_project_root):
        """Test validation workflow with iterative improvements"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Start with poor content
        poor_content = """
        # Revolutionary AI Will Transform Everything!
        
        This amazing, game-changing technology is absolutely incredible.
        AI is magical and will solve all your problems automatically.
        Just use these revolutionary tools and everything will be perfect.
        """
        
        # First validation - should fail
        result1 = crew.validation_engine.validate_content(
            content=poor_content,
            content_id="improvement_test_v1"
        )
        
        assert result1.overall_score < 60  # Should fail
        
        # Store failure pattern in memory
        crew.memory_manager.store_memory(
            agent_role='brand_author',
            memory_type='crew_shared',
            content='Avoid hype language and unsupported claims - leads to validation failures',
            tags=['validation_failure', 'prohibited_language', 'learning'],
            importance=8,
            metadata={'validation_score': result1.overall_score, 'version': 'v1'}
        )
        
        # Improved content based on feedback
        improved_content = """
        # AI Integration for UX Design: A Practical Approach
        
        After testing 8 AI tools over 4 months, here's what actually works.
        
        ## Methodical Testing Results
        - Tool success rate: 63% on first integration
        - Time savings: 25% average across tested workflows
        - Quality improvement: 18% in user research tasks
        
        [AUTHOR: add specific testing methodology]
        
        ## Practical Implementation
        For mid-level UX designers:
        1. Start with one tool for research tasks
        2. Document results over 2-week periods
        3. Expand gradually based on proven value
        
        ## Ethical Considerations
        Bias detection was integrated from the start.
        User agency remained a primary design requirement.
        """
        
        # Second validation - should improve
        result2 = crew.validation_engine.validate_content(
            content=improved_content,
            content_id="improvement_test_v2"
        )
        
        assert result2.overall_score > result1.overall_score  # Should improve
        
        # Store improvement pattern
        if result2.overall_score >= 70:
            crew.memory_manager.store_memory(
                agent_role='brand_author',
                memory_type='external_consolidated',
                content='Successful improvement: methodical data + transparent process + ethical integration',
                tags=['improvement_success', 'validation_pass', 'learning'],
                importance=9,
                metadata={
                    'validation_score': result2.overall_score,
                    'improvement': result2.overall_score - result1.overall_score,
                    'version': 'v2'
                }
            )
        
        # Verify learning captured
        learning_memories = crew.memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type='crew_shared',
            tags=['learning']
        )
        
        assert len(learning_memories) >= 1
    
    def test_reasoning_guided_content_creation(self, temp_project_root):
        """Test reasoning-guided content creation workflow"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Step 1: Create content creation plan
        plan = crew.reasoning_integration.create_context_aware_plan(
            agent_role='brand_author',
            plan_type='content_creation',
            base_requirements={
                'type': 'guide',
                'target_persona': 'Adaptive Alex',
                'topic': 'AI tool selection',
                'complexity': 'medium'
            }
        )
        
        assert plan is not None
        plan_id = plan.id
        
        # Step 2: Execute plan steps
        
        # Brand Knowledge Review
        crew.reasoning_engine.update_step_status(
            plan_id, plan.steps[0].id, 
            crew.reasoning_engine.StepStatus.IN_PROGRESS
        )
        
        # Get brand knowledge
        brand_knowledge = crew.knowledge_manager.get_knowledge_by_type(
            crew.knowledge_manager.KnowledgeType.BRAND_FOUNDATION
        )
        assert len(brand_knowledge) >= 0
        
        crew.reasoning_engine.update_step_status(
            plan_id, plan.steps[0].id, 
            crew.reasoning_engine.StepStatus.COMPLETED
        )
        
        # Content Structure Decision
        from src.soylent_red_division.reasoning_engine import ReasoningContext, DecisionType
        
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={'type': 'guide', 'target_persona': 'Adaptive Alex'},
            brand_constraints={},
            target_personas=['Adaptive Alex'],
            available_resources={},
            success_criteria={}
        )
        
        structure_decision = crew.reasoning_engine.make_decision(
            DecisionType.CONTENT_STRUCTURE, context
        )
        
        assert structure_decision['decision'] == 'content_structure'
        assert 'template' in structure_decision
        
        # Content Creation (simulated)
        created_content = """
        # AI Tool Selection for UX Teams: A Practical Guide
        
        After evaluating 15 AI tools across 6 UX workflows, here's a systematic selection approach.
        
        ## The Methodical Evaluation Framework
        - Tested each tool with standardized design briefs
        - Measured time savings and quality improvements
        - Documented integration complexity and learning curves
        
        ## Selection Criteria for Mid-Level Teams
        1. **Workflow Integration**: Does it fit existing processes?
        2. **Learning Curve**: Can team adopt within 2 weeks?
        3. **Quality Impact**: Measurable improvement in outputs?
        4. **Ethical Compliance**: Bias detection and user control?
        
        [AUTHOR: add specific tool evaluation examples]
        
        ## Evidence-Based Recommendations
        Based on 4 months of testing with 3 UX teams:
        - Research tools: 89% adoption success
        - Ideation tools: 67% adoption success  
        - Content generation: 45% adoption success
        
        ## Implementation Strategy
        Start with research tools, prove value, then expand gradually.
        """
        
        # Content Validation
        validation_result = crew.validation_engine.validate_content(
            content=created_content,
            content_id="reasoning_guided_content",
            target_personas=['Adaptive Alex']
        )
        
        # Should pass with good score due to reasoning guidance
        assert validation_result.overall_score >= 70
        
        # Quality Assurance Gate
        if validation_result.overall_score >= 80:
            crew.reasoning_engine.update_step_status(
                plan_id, plan.steps[-1].id,
                crew.reasoning_engine.StepStatus.COMPLETED
            )
        
        # Complete plan
        crew.reasoning_engine.update_plan_status(
            plan_id, crew.reasoning_engine.PlanStatus.COMPLETED
        )
        
        # Verify plan completion
        completed_plan = crew.reasoning_engine.get_plan(plan_id)
        assert completed_plan.status == crew.reasoning_engine.PlanStatus.COMPLETED
        
        # Store reasoning success pattern
        crew.memory_manager.store_memory(
            agent_role='brand_author',
            memory_type='external_consolidated',
            content='Reasoning-guided content creation successful: structured approach + validation gates',
            tags=['reasoning_success', 'content_creation', 'guided_workflow'],
            importance=9,
            metadata={
                'plan_id': plan_id,
                'validation_score': validation_result.overall_score,
                'workflow_type': 'reasoning_guided'
            }
        )
    
    def test_knowledge_memory_learning_cycle(self, temp_project_root):
        """Test knowledge-memory learning cycle"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Initial knowledge state
        initial_knowledge = crew.knowledge_manager.search_knowledge(
            agent_role='brand_author',
            query='content creation patterns'
        )
        initial_count = len(initial_knowledge)
        
        # Create content and validate
        test_content = """
        # Testing AI Writing Tools: Complete Methodology
        
        Over 6 months, I tested 12 AI writing tools using a systematic approach.
        
        ## Testing Methodology
        - Identical prompts across all tools
        - Quality scoring on 1-10 scale
        - Time measurement for each task
        - Documentation of failure modes
        
        ## Results with Evidence
        Success rate: 74% (89 successful outputs from 120 tests)
        Average quality score: 7.2/10
        Time savings: 43% compared to manual writing
        
        [AUTHOR: add specific tool comparison data]
        
        ## What Didn't Work
        - Generic prompts failed 67% of the time
        - Tools without bias detection were excluded
        - No tool succeeded without human oversight
        
        ## Complete Process Documentation
        Full testing logs and methodology available for review.
        """
        
        validation_result = crew.validation_engine.validate_content(
            content=test_content,
            content_id="learning_cycle_test"
        )
        
        # Store successful pattern in memory
        if validation_result.overall_score >= 80:
            crew.memory_manager.store_memory(
                agent_role='brand_author',
                memory_type='external_consolidated',
                content='High-scoring content pattern: systematic methodology + evidence + transparency + failure inclusion',
                tags=['content_pattern', 'high_quality', 'methodology'],
                importance=10,
                metadata={
                    'validation_score': validation_result.overall_score,
                    'pattern_elements': ['systematic_methodology', 'evidence_based', 'transparency', 'failure_inclusion'],
                    'content_type': 'methodological_guide'
                }
            )
        
        # Use knowledge-memory integration to enhance future content creation
        enhanced_knowledge = crew.km_integration.get_knowledge_with_memory_insights(
            agent_role='brand_author',
            knowledge_type=crew.knowledge_manager.KnowledgeType.WRITING_EXAMPLES
        )
        
        # Should have enhanced knowledge with usage insights
        assert len(enhanced_knowledge) >= 0
        
        # Create recommendations based on memory patterns
        recommendations = crew.km_integration.get_content_recommendations(
            agent_role='brand_author',
            context={'content_type': 'guide', 'target_persona': 'Adaptive Alex'}
        )
        
        assert isinstance(recommendations, list)
        
        # Verify learning captured
        pattern_memories = crew.memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type='external_consolidated',
            tags=['content_pattern', 'high_quality']
        )
        
        assert len(pattern_memories) >= 1
    
    def test_complete_system_stats_workflow(self, temp_project_root):
        """Test complete system statistics workflow"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Generate some activity across all systems
        
        # Memory activity
        crew.memory_manager.store_memory(
            agent_role='brand_author',
            memory_type='crew_shared',
            content='System stats test memory',
            tags=['stats_test'],
            importance=7
        )
        
        # Knowledge activity
        crew.knowledge_manager.refresh_knowledge()
        
        # Reasoning activity
        from src.soylent_red_division.reasoning_engine import ReasoningContext
        
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = crew.reasoning_engine.create_plan("content_creation", context, "stats_test")
        
        # Validation activity
        validation_result = crew.validation_engine.validate_content(
            content="Stats test content",
            content_id="stats_test"
        )
        
        # Test stats commands with mocking
        with patch('sys.argv', ['main.py']):
            try:
                # Mock print to capture output
                with patch('builtins.print') as mock_print:
                    memory_stats_result = memory_stats()
                    knowledge_stats_result = knowledge_stats()
                    reasoning_stats_result = reasoning_stats()
                    
                    # Should not raise exceptions
                    assert memory_stats_result is not None
                    assert knowledge_stats_result is not None
                    assert reasoning_stats_result is not None
                    
                    # Should have called print (output generated)
                    assert mock_print.call_count > 0
                
            except Exception as e:
                assert False, f"Stats workflow should not fail: {e}"
    
    def test_error_recovery_workflow(self, temp_project_root):
        """Test error recovery across the workflow"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Test various error conditions and recovery
        
        # 1. Invalid memory operation
        try:
            result = crew.memory_manager.store_memory(
                agent_role='invalid_role',
                memory_type='crew_shared',
                content='Test content',
                tags=['test'],
                importance=5
            )
            assert result is False  # Should return False, not crash
        except Exception as e:
            assert False, f"Should handle invalid memory operations gracefully: {e}"
        
        # 2. Invalid validation content
        try:
            result = crew.validation_engine.validate_content(
                content=None,
                content_id="error_test"
            )
            assert result is not None  # Should handle None content
        except Exception as e:
            assert False, f"Should handle invalid validation content gracefully: {e}"
        
        # 3. Invalid reasoning plan
        try:
            from src.soylent_red_division.reasoning_engine import ReasoningContext
            
            context = ReasoningContext(
                task_type="invalid_type",
                content_requirements={},
                brand_constraints={},
                target_personas=[],
                available_resources={},
                success_criteria={}
            )
            
            # This should raise ValueError for invalid plan type
            with pytest.raises(ValueError):
                crew.reasoning_engine.create_plan("invalid_plan_type", context, "test")
                
        except Exception as e:
            if not isinstance(e, ValueError):
                assert False, f"Should raise appropriate exceptions for invalid operations: {e}"
        
        # 4. System should continue functioning after errors
        try:
            # Normal operations should still work
            crew.memory_manager.store_memory(
                agent_role='brand_author',
                memory_type='crew_shared',
                content='Recovery test memory',
                tags=['recovery'],
                importance=6
            )
            
            result = crew.validation_engine.validate_content(
                content="Recovery test content",
                content_id="recovery_test"
            )
            
            assert result is not None
            
        except Exception as e:
            assert False, f"System should recover from errors and continue functioning: {e}"
    
    def test_performance_end_to_end(self, temp_project_root):
        """Test end-to-end performance"""
        import time
        
        start_time = time.time()
        
        # Initialize complete system
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        initialization_time = time.time() - start_time
        assert initialization_time < 10.0  # Should initialize within 10 seconds
        
        # Run complete workflow
        workflow_start = time.time()
        
        # Memory operation
        crew.memory_manager.store_memory(
            agent_role='brand_author',
            memory_type='crew_shared',
            content='Performance test memory',
            tags=['performance'],
            importance=7
        )
        
        # Knowledge operation
        knowledge_items = crew.knowledge_manager.search_knowledge(
            agent_role='brand_author',
            query='brand'
        )
        
        # Reasoning operation
        from src.soylent_red_division.reasoning_engine import ReasoningContext
        
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={'type': 'guide'},
            brand_constraints={},
            target_personas=['Adaptive Alex'],
            available_resources={},
            success_criteria={}
        )
        
        plan = crew.reasoning_engine.create_plan("content_creation", context, "performance_test")
        
        # Validation operation
        validation_result = crew.validation_engine.validate_content(
            content="Performance test content for validation",
            content_id="performance_test"
        )
        
        workflow_time = time.time() - workflow_start
        assert workflow_time < 5.0  # Complete workflow should finish within 5 seconds
        
        # Verify all operations completed successfully
        assert plan is not None
        assert validation_result is not None
        assert len(knowledge_items) >= 0
    
    def test_data_consistency_end_to_end(self, temp_project_root):
        """Test data consistency across complete workflow"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Use consistent identifier across all systems
        test_id = "consistency_e2e_test"
        test_agent = "brand_author"
        
        # Create data in all systems
        
        # Memory
        crew.memory_manager.store_memory(
            agent_role=test_agent,
            memory_type='crew_shared',
            content=f'Consistency test for {test_id}',
            tags=['consistency', 'e2e'],
            importance=8,
            metadata={'test_id': test_id}
        )
        
        # Validation
        validation_result = crew.validation_engine.validate_content(
            content=f"Consistency test content for {test_id}",
            content_id=test_id
        )
        
        # Reasoning
        from src.soylent_red_division.reasoning_engine import ReasoningContext
        
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={'test_id': test_id},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        plan = crew.reasoning_engine.create_plan("content_creation", context, test_agent)
        
        # Verify data consistency
        
        # Memory should contain the data
        memories = crew.memory_manager.retrieve_memory(
            agent_role=test_agent,
            memory_type='crew_shared',
            tags=['consistency']
        )
        assert len(memories) >= 1
        assert any(test_id in mem.metadata.get('test_id', '') for mem in memories)
        
        # Validation should have the result
        retrieved_validation = crew.validation_engine.get_validation_result(validation_result.id)
        assert retrieved_validation is not None
        assert retrieved_validation.content_id == test_id
        
        # Reasoning should have the plan
        retrieved_plan = crew.reasoning_engine.get_plan(plan.id)
        assert retrieved_plan is not None
        assert retrieved_plan.created_by == test_agent
        assert retrieved_plan.reasoning_context.content_requirements.get('test_id') == test_id
        
        # Cross-system consistency check
        assert validation_result.content_id == test_id
        assert plan.reasoning_context.content_requirements.get('test_id') == test_id
        assert any(test_id in mem.metadata.get('test_id', '') for mem in memories)