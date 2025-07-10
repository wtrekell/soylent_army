"""
Tests for Crew and Tools
Tests the crew configuration, tool integration, and agent behavior
"""

import pytest
import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock

from src.soylent_red_division.crew import SoylentRedDivision
from src.soylent_red_division.tools.memory_tools import (
    MemorySearchTool, MemoryStoreTool, InteractionMemoryTool, 
    FeedbackMemoryTool, BrandDecisionMemoryTool, MemoryStatsTool
)
from src.soylent_red_division.tools.knowledge_tools import (
    KnowledgeSearchTool, KnowledgeGetTool, KnowledgeByTypeTool,
    BrandContextTool, KnowledgeUpdateTool, KnowledgeValidationTool, KnowledgeStatsTool
)
from src.soylent_red_division.tools.planning_tools import (
    CreatePlanTool, MakeDecisionTool, GetPlanTool, UpdatePlanTool,
    UpdateStepTool, AnalyzeTaskTool, PlanningStatsTool
)
from src.soylent_red_division.tools.validation_tools import (
    ValidateContentTool, ValidateRealTimeTool, GetValidationResultTool,
    GetValidationHistoryTool, ValidationStatsTool
)

class TestSoylentRedDivisionCrew:
    """Test suite for Soylent Red Division crew"""
    
    def test_crew_initialization(self, temp_project_root):
        """Test crew initialization and configuration"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Verify core systems are initialized
        assert crew.memory_manager is not None
        assert crew.knowledge_manager is not None
        assert crew.reasoning_engine is not None
        assert crew.validation_engine is not None
        assert crew.reasoning_integration is not None
        
        # Verify LLM manager
        assert crew.llm_manager is not None
        
        # Verify brand knowledge loaded
        assert crew.brand_context is not None
        assert len(crew.brand_context) > 0
    
    def test_crew_agent_configuration(self, temp_project_root):
        """Test agent configuration and setup"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        crew_instance = crew.crew()
        
        # Should have at least the writer agent
        assert len(crew_instance.agents) >= 1
        
        # Check writer agent configuration
        writer_agent = crew_instance.agents[0]
        assert writer_agent.role == "Syntax & Empathy Brand Writer & Voice Guardian"
        
        # Agent should have access to all tool categories
        agent_tools = writer_agent.tools
        tool_names = [tool.name for tool in agent_tools]
        
        # Should have memory tools
        memory_tool_names = ['memory_search', 'memory_store', 'interaction_memory', 'feedback_memory', 'brand_decision_memory', 'memory_stats']
        assert any(tool_name in tool_names for tool_name in memory_tool_names)
        
        # Should have knowledge tools
        knowledge_tool_names = ['knowledge_search', 'knowledge_get', 'knowledge_by_type', 'brand_context', 'knowledge_stats']
        assert any(tool_name in tool_names for tool_name in knowledge_tool_names)
        
        # Should have planning tools
        planning_tool_names = ['create_plan', 'make_decision', 'get_plan', 'analyze_task', 'planning_stats']
        assert any(tool_name in tool_names for tool_name in planning_tool_names)
        
        # Should have validation tools
        validation_tool_names = ['validate_content', 'validate_real_time', 'get_validation_result', 'validation_stats']
        assert any(tool_name in tool_names for tool_name in validation_tool_names)
    
    def test_crew_task_configuration(self, temp_project_root):
        """Test task configuration and setup"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        crew_instance = crew.crew()
        
        # Should have the writing task
        assert len(crew_instance.tasks) >= 1
        
        writing_task = crew_instance.tasks[0]
        assert "brand" in writing_task.description.lower()
        assert "compliance" in writing_task.description.lower()
        
        # Task should be assigned to the writer agent
        assert writing_task.agent == crew_instance.agents[0]
    
    @patch('src.soylent_red_division.crew.SoylentRedDivision._get_brand_context')
    def test_crew_brand_knowledge_integration(self, mock_brand_context, temp_project_root):
        """Test brand knowledge integration in crew"""
        # Mock brand context
        mock_brand_context.return_value = "Test brand context with voice characteristics"
        
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Verify brand context is integrated
        assert crew.brand_context == "Test brand context with voice characteristics"
        mock_brand_context.assert_called_once()
    
    def test_brand_author_crew_creation(self, temp_project_root):
        """Test brand author collaborative crew creation"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        brand_author_crew = crew.brand_author_crew()
        
        # Should have agents and tasks configured for collaboration
        assert len(brand_author_crew.agents) >= 1
        assert len(brand_author_crew.tasks) >= 1
        
        # Should be configured for initial draft creation
        task = brand_author_crew.tasks[0]
        assert "draft" in task.description.lower() or "initial" in task.description.lower()
    
    def test_feedback_crew_creation(self, temp_project_root):
        """Test feedback processing crew creation"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        feedback_crew = crew.feedback_crew(
            feedback_input="This needs more practical examples",
            draft_path="/test/path/draft.md",
            revision_history="Initial draft created"
        )
        
        # Should have agents and tasks configured for feedback processing
        assert len(feedback_crew.agents) >= 1
        assert len(feedback_crew.tasks) >= 1
        
        # Should be configured for revision
        task = feedback_crew.tasks[0]
        assert "feedback" in task.description.lower() or "revision" in task.description.lower()
    
    def test_signoff_crew_creation(self, temp_project_root):
        """Test signoff crew creation"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        signoff_crew = crew.signoff_crew(
            final_draft_path="/test/path/final_draft.md",
            signoff_confirmation="Approved for editing"
        )
        
        # Should have agents and tasks configured for signoff
        assert len(signoff_crew.agents) >= 1
        assert len(signoff_crew.tasks) >= 1
        
        # Should be configured for finalization
        task = signoff_crew.tasks[0]
        assert "signoff" in task.description.lower() or "final" in task.description.lower()

class TestMemoryTools:
    """Test suite for Memory Tools"""
    
    def test_memory_search_tool(self, memory_manager):
        """Test memory search tool functionality"""
        # Store test memory
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type='crew_shared',
            content='AI integration successful with Tool X',
            tags=['ai', 'integration', 'success'],
            importance=8
        )
        
        tool = MemorySearchTool(memory_manager=memory_manager)
        
        # Test search
        result = tool._run(
            agent_role='brand_author',
            query='AI integration',
            memory_type='crew_shared'
        )
        
        assert isinstance(result, str)
        assert 'Tool X' in result or 'integration' in result
    
    def test_memory_store_tool(self, memory_manager):
        """Test memory store tool functionality"""
        tool = MemoryStoreTool(memory_manager=memory_manager)
        
        result = tool._run(
            agent_role='brand_author',
            memory_type='crew_shared',
            content='Test memory storage from tool',
            tags=['test', 'tool'],
            importance=7
        )
        
        assert isinstance(result, str)
        assert 'stored' in result.lower() or 'success' in result.lower()
        
        # Verify memory was stored
        memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type='crew_shared',
            tags=['test', 'tool']
        )
        assert len(memories) >= 1
    
    def test_interaction_memory_tool(self, memory_manager):
        """Test interaction memory tool functionality"""
        tool = InteractionMemoryTool(memory_manager=memory_manager)
        
        result = tool._run(
            agent_role='brand_author',
            interaction_type='feedback_session',
            participants=['brand_author', 'writer'],
            outcome='successful_revision',
            key_insights=['voice_improvement', 'persona_alignment'],
            importance=8
        )
        
        assert isinstance(result, str)
        assert 'interaction' in result.lower()
        
        # Verify interaction memory was stored
        memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type='crew_shared',
            tags=['interaction']
        )
        assert len(memories) >= 1
    
    def test_feedback_memory_tool(self, memory_manager):
        """Test feedback memory tool functionality"""
        tool = FeedbackMemoryTool(memory_manager=memory_manager)
        
        result = tool._run(
            agent_role='brand_author',
            feedback_type='structural',
            feedback_content='Needs more practical examples',
            effectiveness_rating=8,
            implementation_success=True,
            lessons_learned=['practical_examples_important', 'structure_clarity']
        )
        
        assert isinstance(result, str)
        assert 'feedback' in result.lower()
        
        # Verify feedback memory was stored
        memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type='crew_shared',
            tags=['feedback']
        )
        assert len(memories) >= 1
    
    def test_brand_decision_memory_tool(self, memory_manager):
        """Test brand decision memory tool functionality"""
        tool = BrandDecisionMemoryTool(memory_manager=memory_manager)
        
        result = tool._run(
            agent_role='brand_author',
            decision_context='persona_targeting',
            decision_made='target_adaptive_alex',
            reasoning='practical_implementation_focus',
            brand_impact='high',
            consistency_notes='aligns_with_brand_values'
        )
        
        assert isinstance(result, str)
        assert 'brand decision' in result.lower()
        
        # Verify brand decision memory was stored
        memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type='external_consolidated',
            tags=['brand_decision']
        )
        assert len(memories) >= 1
    
    def test_memory_stats_tool(self, memory_manager):
        """Test memory stats tool functionality"""
        # Store some test memories
        for i in range(3):
            memory_manager.store_memory(
                agent_role='brand_author',
                memory_type='crew_shared',
                content=f'Test memory {i}',
                tags=['test'],
                importance=5
            )
        
        tool = MemoryStatsTool(memory_manager=memory_manager)
        
        result = tool._run(agent_role='brand_author')
        
        assert isinstance(result, str)
        assert 'memory statistics' in result.lower()
        assert 'crew_shared' in result.lower()

class TestKnowledgeTools:
    """Test suite for Knowledge Tools"""
    
    def test_knowledge_search_tool(self, knowledge_manager):
        """Test knowledge search tool functionality"""
        tool = KnowledgeSearchTool(knowledge_manager=knowledge_manager)
        
        result = tool._run(
            agent_role='brand_author',
            query='brand voice characteristics'
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_knowledge_get_tool(self, knowledge_manager):
        """Test knowledge get tool functionality"""
        # Get available knowledge items
        all_items = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            query='',
            limit=1
        )
        
        if all_items:
            tool = KnowledgeGetTool(knowledge_manager=knowledge_manager)
            
            result = tool._run(
                agent_role='brand_author',
                item_id=all_items[0].id
            )
            
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_knowledge_by_type_tool(self, knowledge_manager):
        """Test knowledge by type tool functionality"""
        tool = KnowledgeByTypeTool(knowledge_manager=knowledge_manager)
        
        result = tool._run(
            agent_role='brand_author',
            knowledge_type='brand_foundation'
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_brand_context_tool(self, knowledge_manager):
        """Test brand context tool functionality"""
        tool = BrandContextTool(knowledge_manager=knowledge_manager)
        
        result = tool._run(
            agent_role='brand_author',
            context_type='full'
        )
        
        assert isinstance(result, str)
        assert len(result) > 0
        assert 'brand' in result.lower()
    
    def test_knowledge_stats_tool(self, knowledge_manager):
        """Test knowledge stats tool functionality"""
        tool = KnowledgeStatsTool(knowledge_manager=knowledge_manager)
        
        result = tool._run(agent_role='brand_author')
        
        assert isinstance(result, str)
        assert 'knowledge statistics' in result.lower()

class TestPlanningTools:
    """Test suite for Planning Tools"""
    
    def test_create_plan_tool(self, reasoning_engine):
        """Test create plan tool functionality"""
        tool = CreatePlanTool(reasoning_engine=reasoning_engine)
        
        result = tool._run(
            agent_role='brand_author',
            plan_type='content_creation',
            task_requirements='Create guide for AI integration',
            target_personas=['Adaptive Alex'],
            success_criteria='Brand compliant, practical guidance'
        )
        
        assert isinstance(result, str)
        assert 'plan created' in result.lower()
        assert 'content_creation' in result.lower()
    
    def test_make_decision_tool(self, reasoning_engine):
        """Test make decision tool functionality"""
        tool = MakeDecisionTool(reasoning_engine=reasoning_engine)
        
        result = tool._run(
            agent_role='brand_author',
            decision_type='content_structure',
            task_context='Creating practical guide for UX designers',
            content_requirements='Step-by-step implementation',
            target_personas=['Adaptive Alex']
        )
        
        assert isinstance(result, str)
        assert 'decision' in result.lower()
        assert 'content_structure' in result.lower()
    
    def test_analyze_task_tool(self, reasoning_engine):
        """Test analyze task tool functionality"""
        tool = AnalyzeTaskTool(reasoning_engine=reasoning_engine)
        
        result = tool._run(
            agent_role='brand_author',
            task_description='Write comprehensive guide on AI tool integration for UX teams',
            context_information='Target mid-level designers, practical focus'
        )
        
        assert isinstance(result, str)
        assert 'analysis' in result.lower()
        assert len(result) > 100  # Should provide detailed analysis
    
    def test_planning_stats_tool(self, reasoning_engine):
        """Test planning stats tool functionality"""
        # Create a test plan first
        from src.soylent_red_division.reasoning_engine import ReasoningContext
        
        context = ReasoningContext(
            task_type="content_creation",
            content_requirements={},
            brand_constraints={},
            target_personas=[],
            available_resources={},
            success_criteria={}
        )
        
        reasoning_engine.create_plan("content_creation", context, "test_user")
        
        tool = PlanningStatsTool(reasoning_engine=reasoning_engine)
        
        result = tool._run(agent_role='brand_author')
        
        assert isinstance(result, str)
        assert 'planning statistics' in result.lower()

class TestValidationTools:
    """Test suite for Validation Tools"""
    
    def test_validate_content_tool(self, validation_engine):
        """Test validate content tool functionality"""
        tool = ValidateContentTool(validation_engine=validation_engine)
        
        test_content = """
        # AI Integration Guide
        
        After testing 10 tools over 3 months, here's what works:
        
        [AUTHOR: add personal testing examples]
        
        The data shows 67% improvement in research efficiency.
        """
        
        result = tool._run(
            agent_role='brand_author',
            content=test_content,
            content_id='test_validation',
            target_personas=['Adaptive Alex']
        )
        
        assert isinstance(result, str)
        assert 'validation' in result.lower()
        assert 'score' in result.lower()
    
    def test_validate_real_time_tool(self, validation_engine):
        """Test validate real-time tool functionality"""
        tool = ValidateRealTimeTool(validation_engine=validation_engine)
        
        result = tool._run(
            agent_role='brand_author',
            content_fragment='This revolutionary AI will transform everything!',
            content_id='realtime_test'
        )
        
        assert isinstance(result, str)
        assert 'validation' in result.lower()
        # Should detect prohibited language
        assert 'revolutionary' in result.lower() or 'prohibited' in result.lower()
    
    def test_validation_stats_tool(self, validation_engine):
        """Test validation stats tool functionality"""
        # Perform a validation first to generate data
        validation_engine.validate_content(
            content="Test content for stats",
            content_id="stats_test"
        )
        
        tool = ValidationStatsTool(validation_engine=validation_engine)
        
        result = tool._run(agent_role='brand_author')
        
        assert isinstance(result, str)
        assert 'validation statistics' in result.lower()

class TestToolIntegration:
    """Test suite for tool integration with crew"""
    
    def test_tool_access_permissions(self, temp_project_root):
        """Test tool access permissions by agent role"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Test different agent roles have appropriate tool access
        writer_tools = crew._get_tools('writer')
        brand_author_tools = crew._get_tools('brand_author')
        
        # Both should have access to core tools
        writer_tool_names = [tool.name for tool in writer_tools]
        brand_author_tool_names = [tool.name for tool in brand_author_tools]
        
        # Should have memory tools
        assert 'memory_search' in writer_tool_names
        assert 'memory_search' in brand_author_tool_names
        
        # Should have knowledge tools
        assert 'knowledge_search' in writer_tool_names
        assert 'knowledge_search' in brand_author_tool_names
        
        # Should have validation tools
        assert 'validate_content' in writer_tool_names
        assert 'validate_content' in brand_author_tool_names
    
    def test_tool_error_handling(self, temp_project_root):
        """Test tool error handling with invalid inputs"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Test memory search tool with invalid role
        memory_tool = MemorySearchTool(memory_manager=crew.memory_manager)
        
        try:
            result = memory_tool._run(
                agent_role='invalid_role',
                query='test query'
            )
            # Should handle gracefully
            assert isinstance(result, str)
            assert 'error' in result.lower() or 'not found' in result.lower() or len(result) == 0
        except Exception as e:
            # Should not raise unhandled exceptions
            assert False, f"Tool should handle errors gracefully: {e}"
    
    def test_tool_performance(self, temp_project_root):
        """Test tool performance and response times"""
        import time
        
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Test memory search performance
        memory_tool = MemorySearchTool(memory_manager=crew.memory_manager)
        
        start_time = time.time()
        result = memory_tool._run(
            agent_role='brand_author',
            query='test performance query'
        )
        end_time = time.time()
        
        # Should complete quickly
        assert end_time - start_time < 2.0  # 2 seconds max
        assert isinstance(result, str)
    
    @patch('src.soylent_red_division.crew.SoylentRedDivision._get_brand_context')
    def test_crew_kickoff_simulation(self, mock_brand_context, temp_project_root):
        """Test crew kickoff simulation"""
        mock_brand_context.return_value = "Mock brand context"
        
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Test inputs
        test_inputs = {
            'requirements': 'Write a guide about AI prompt engineering for UX designers',
            'title': 'AI Prompt Engineering Guide',
            'context': 'For mid-level UX designers looking to integrate AI tools'
        }
        
        # Mock the LLM responses to avoid actual API calls
        with patch.object(crew.crew().agents[0], 'execute_task') as mock_execute:
            mock_execute.return_value = "Mock task execution result"
            
            try:
                # This would normally call LLMs, so we're just testing setup
                crew_instance = crew.crew()
                assert crew_instance is not None
                assert len(crew_instance.agents) >= 1
                assert len(crew_instance.tasks) >= 1
                
                # Verify task configuration
                task = crew_instance.tasks[0]
                assert task.agent is not None
                assert len(task.tools) > 0
                
            except Exception as e:
                # Should not fail on setup
                assert False, f"Crew setup should not fail: {e}"
    
    def test_tool_chain_integration(self, temp_project_root):
        """Test tool chain integration and data flow"""
        crew = SoylentRedDivision(project_root=temp_project_root)
        
        # Simulate tool chain: knowledge → planning → validation → memory
        
        # 1. Knowledge search
        knowledge_tool = KnowledgeSearchTool(knowledge_manager=crew.knowledge_manager)
        knowledge_result = knowledge_tool._run(
            agent_role='brand_author',
            query='brand voice'
        )
        assert isinstance(knowledge_result, str)
        
        # 2. Create plan based on knowledge
        planning_tool = CreatePlanTool(reasoning_engine=crew.reasoning_engine)
        plan_result = planning_tool._run(
            agent_role='brand_author',
            plan_type='content_creation',
            task_requirements='Create brand-compliant content',
            target_personas=['Adaptive Alex'],
            success_criteria='High brand compliance score'
        )
        assert isinstance(plan_result, str)
        
        # 3. Validate content
        validation_tool = ValidateContentTool(validation_engine=crew.validation_engine)
        validation_result = validation_tool._run(
            agent_role='brand_author',
            content='Test content for validation',
            content_id='chain_test'
        )
        assert isinstance(validation_result, str)
        
        # 4. Store memory about the process
        memory_tool = MemoryStoreTool(memory_manager=crew.memory_manager)
        memory_result = memory_tool._run(
            agent_role='brand_author',
            memory_type='crew_shared',
            content='Tool chain integration test completed successfully',
            tags=['tool_chain', 'integration', 'test'],
            importance=7
        )
        assert isinstance(memory_result, str)
        
        # Verify all tools executed successfully
        assert 'error' not in knowledge_result.lower()
        assert 'error' not in plan_result.lower()
        assert 'error' not in validation_result.lower()
        assert 'error' not in memory_result.lower()
    
    def test_concurrent_tool_usage(self, temp_project_root):
        """Test concurrent tool usage safety"""
        import threading
        
        crew = SoylentRedDivision(project_root=temp_project_root)
        results = []
        
        def use_memory_tool(tool_id):
            memory_tool = MemoryStoreTool(memory_manager=crew.memory_manager)
            result = memory_tool._run(
                agent_role='brand_author',
                memory_type='crew_shared',
                content=f'Concurrent test memory {tool_id}',
                tags=['concurrent', 'test'],
                importance=5
            )
            results.append(result)
        
        # Create multiple threads using tools concurrently
        threads = []
        for i in range(3):
            thread = threading.Thread(target=use_memory_tool, args=[i])
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # All should complete successfully
        assert len(results) == 3
        assert all(isinstance(result, str) for result in results)
        assert all('error' not in result.lower() for result in results)