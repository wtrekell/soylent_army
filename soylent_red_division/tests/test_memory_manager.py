"""
Tests for Memory Manager
"""

import pytest
import json
from datetime import datetime, timedelta
from pathlib import Path

from src.soylent_red_division.memory_manager import (
    MemoryManager, MemoryType, MemoryEntry, MemoryAccessLevel
)

class TestMemoryManager:
    """Test suite for Memory Manager"""
    
    def test_memory_manager_initialization(self, temp_project_root):
        """Test memory manager initialization"""
        mm = MemoryManager(temp_project_root)
        
        assert mm.project_root == temp_project_root
        assert mm.memory_dir.exists()
        assert mm.memory_dir.is_dir()
        
        # Check memory files exist
        assert mm.crew_shared_file.exists()
        assert mm.agent_specific_file.exists()
        assert mm.external_consolidated_file.exists()
        assert mm.session_temporary_file.exists()
    
    def test_store_memory_basic(self, memory_manager):
        """Test basic memory storage"""
        result = memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Test memory content',
            tags=['test', 'basic'],
            importance=8
        )
        
        assert result is True
        
        # Verify memory was stored
        memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            tags=['test']
        )
        
        assert len(memories) == 1
        assert memories[0].content == 'Test memory content'
        assert 'test' in memories[0].tags
        assert memories[0].importance == 8
    
    def test_store_memory_with_metadata(self, memory_manager):
        """Test memory storage with metadata"""
        metadata = {
            'context': 'unit_test',
            'tool_used': 'pytest',
            'success_rate': 0.95
        }
        
        result = memory_manager.store_memory(
            agent_role='writer',
            memory_type=MemoryType.AGENT_SPECIFIC,
            content='Memory with metadata',
            tags=['metadata', 'test'],
            importance=7,
            metadata=metadata
        )
        
        assert result is True
        
        # Verify metadata was stored
        memories = memory_manager.retrieve_memory(
            agent_role='writer',
            memory_type=MemoryType.AGENT_SPECIFIC,
            tags=['metadata']
        )
        
        assert len(memories) == 1
        assert memories[0].metadata == metadata
        assert memories[0].metadata['success_rate'] == 0.95
    
    def test_memory_access_control(self, memory_manager):
        """Test memory access control by role"""
        # Store memory as brand_author
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
            content='Admin only memory',
            tags=['admin', 'restricted'],
            importance=9
        )
        
        # brand_author should have access
        admin_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
            tags=['admin']
        )
        assert len(admin_memories) == 1
        
        # writer should have read-only access
        writer_memories = memory_manager.retrieve_memory(
            agent_role='writer',
            memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
            tags=['admin']
        )
        assert len(writer_memories) == 1
        
        # researcher should have read-only access
        researcher_memories = memory_manager.retrieve_memory(
            agent_role='researcher',
            memory_type=MemoryType.EXTERNAL_CONSOLIDATED,
            tags=['admin']
        )
        assert len(researcher_memories) == 1
    
    def test_memory_search_by_query(self, memory_manager):
        """Test memory search by text query"""
        # Store test memories
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='AI integration was successful with Tool X',
            tags=['ai', 'integration', 'success'],
            importance=8
        )
        
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Brand validation failed on first attempt',
            tags=['brand', 'validation', 'failure'],
            importance=7
        )
        
        # Search for AI-related memories
        ai_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            query='AI integration'
        )
        
        assert len(ai_memories) == 1
        assert 'Tool X' in ai_memories[0].content
        
        # Search for validation memories
        validation_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            query='validation'
        )
        
        assert len(validation_memories) == 1
        assert 'failed' in validation_memories[0].content
    
    def test_memory_search_by_tags(self, memory_manager):
        """Test memory search by tags"""
        # Store memories with different tags
        memory_manager.store_memory(
            agent_role='writer',
            memory_type=MemoryType.CREW_SHARED,
            content='Success story 1',
            tags=['success', 'workflow', 'ai'],
            importance=8
        )
        
        memory_manager.store_memory(
            agent_role='writer',
            memory_type=MemoryType.CREW_SHARED,
            content='Success story 2',
            tags=['success', 'brand', 'validation'],
            importance=7
        )
        
        memory_manager.store_memory(
            agent_role='writer',
            memory_type=MemoryType.CREW_SHARED,
            content='Failure case',
            tags=['failure', 'workflow'],
            importance=6
        )
        
        # Search for success stories
        success_memories = memory_manager.retrieve_memory(
            agent_role='writer',
            memory_type=MemoryType.CREW_SHARED,
            tags=['success']
        )
        
        assert len(success_memories) == 2
        
        # Search for workflow-related memories
        workflow_memories = memory_manager.retrieve_memory(
            agent_role='writer',
            memory_type=MemoryType.CREW_SHARED,
            tags=['workflow']
        )
        
        assert len(workflow_memories) == 2
    
    def test_memory_importance_filtering(self, memory_manager):
        """Test memory filtering by importance"""
        # Store memories with different importance levels
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Critical issue',
            tags=['critical'],
            importance=10
        )
        
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Important issue',
            tags=['important'],
            importance=8
        )
        
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Minor issue',
            tags=['minor'],
            importance=4
        )
        
        # Get high importance memories
        high_importance = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            min_importance=8
        )
        
        assert len(high_importance) == 2
        assert all(mem.importance >= 8 for mem in high_importance)
    
    def test_memory_time_filtering(self, memory_manager):
        """Test memory filtering by time"""
        # Store memory
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Recent memory',
            tags=['recent'],
            importance=7
        )
        
        # Search for recent memories
        recent_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            since=datetime.now() - timedelta(minutes=1)
        )
        
        assert len(recent_memories) == 1
        assert recent_memories[0].content == 'Recent memory'
    
    def test_memory_consolidation_basic(self, memory_manager):
        """Test basic memory consolidation"""
        # Store similar memories
        for i in range(15):
            memory_manager.store_memory(
                agent_role='brand_author',
                memory_type=MemoryType.CREW_SHARED,
                content=f'Similar memory {i}',
                tags=['similar', 'test'],
                importance=5
            )
        
        # Trigger consolidation
        original_count = len(memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            tags=['similar']
        ))
        
        # Check consolidation candidates
        stats = memory_manager.get_memory_stats('brand_author')
        crew_shared_stats = stats[MemoryType.CREW_SHARED]
        
        assert crew_shared_stats['consolidation_candidates'] > 0
        assert crew_shared_stats['total_entries'] >= 15
    
    def test_memory_consolidation_execution(self, memory_manager):
        """Test memory consolidation execution"""
        # Store many similar memories to trigger consolidation
        for i in range(25):
            memory_manager.store_memory(
                agent_role='brand_author',
                memory_type=MemoryType.CREW_SHARED,
                content=f'Consolidation test memory {i}',
                tags=['consolidation', 'test', 'similar'],
                importance=5
            )
        
        # Get original count
        original_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            tags=['consolidation']
        )
        original_count = len(original_memories)
        
        # Run consolidation
        results = memory_manager.manual_consolidation(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED
        )
        
        # Verify consolidation occurred
        assert MemoryType.CREW_SHARED in results
        result = results[MemoryType.CREW_SHARED]
        assert result['original_count'] == original_count
        assert result['consolidated_count'] < original_count
        assert result['space_saved'] > 0
    
    def test_memory_stats(self, memory_manager):
        """Test memory statistics"""
        # Store test memories
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Stats test memory',
            tags=['stats'],
            importance=8
        )
        
        # Get stats
        stats = memory_manager.get_memory_stats('brand_author')
        
        assert MemoryType.CREW_SHARED in stats
        crew_stats = stats[MemoryType.CREW_SHARED]
        
        assert crew_stats['total_entries'] >= 1
        assert crew_stats['average_importance'] > 0
        assert 'oldest_entry' in crew_stats
        assert 'newest_entry' in crew_stats
    
    def test_memory_search_across_types(self, memory_manager):
        """Test search across multiple memory types"""
        # Store memories in different types
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Cross-type search test 1',
            tags=['cross-search'],
            importance=8
        )
        
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.AGENT_SPECIFIC,
            content='Cross-type search test 2',
            tags=['cross-search'],
            importance=7
        )
        
        # Search across all types
        results = memory_manager.search_across_memories(
            agent_role='brand_author',
            query='cross-type',
            limit=10
        )
        
        # Should find memories from multiple types
        assert len(results) >= 2
        memory_types = set()
        for memory_type, memories in results.items():
            if memories:
                memory_types.add(memory_type)
        
        assert len(memory_types) >= 2
    
    def test_memory_export(self, memory_manager, temp_project_root):
        """Test memory export functionality"""
        # Store test memory
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Export test memory',
            tags=['export'],
            importance=8
        )
        
        # Export memory
        export_path = temp_project_root / "test_export.json"
        result = memory_manager.export_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            output_path=export_path
        )
        
        assert result is True
        assert export_path.exists()
        
        # Verify export content
        with open(export_path, 'r') as f:
            exported_data = json.load(f)
        
        assert 'memories' in exported_data
        assert 'metadata' in exported_data
        assert len(exported_data['memories']) >= 1
    
    def test_memory_persistence(self, temp_project_root):
        """Test memory persistence across manager instances"""
        # Create first manager and store memory
        mm1 = MemoryManager(temp_project_root)
        mm1.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Persistence test memory',
            tags=['persistence'],
            importance=9
        )
        
        # Create second manager instance
        mm2 = MemoryManager(temp_project_root)
        
        # Verify memory persists
        memories = mm2.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            tags=['persistence']
        )
        
        assert len(memories) == 1
        assert memories[0].content == 'Persistence test memory'
        assert memories[0].importance == 9
    
    def test_session_memory_clearing(self, memory_manager):
        """Test session memory clearing"""
        # Store session memory
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.SESSION_TEMPORARY,
            content='Session memory',
            tags=['session'],
            importance=5
        )
        
        # Verify session memory exists
        session_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.SESSION_TEMPORARY,
            tags=['session']
        )
        assert len(session_memories) == 1
        
        # Clear session memory
        memory_manager.clear_session_memory()
        
        # Verify session memory is cleared
        session_memories = memory_manager.retrieve_memory(
            agent_role='brand_author',
            memory_type=MemoryType.SESSION_TEMPORARY,
            tags=['session']
        )
        assert len(session_memories) == 0
    
    def test_memory_error_handling(self, memory_manager):
        """Test memory manager error handling"""
        # Test invalid memory type
        with pytest.raises(ValueError):
            memory_manager.store_memory(
                agent_role='brand_author',
                memory_type='invalid_type',
                content='Test',
                tags=['test'],
                importance=5
            )
        
        # Test invalid agent role
        result = memory_manager.store_memory(
            agent_role='invalid_role',
            memory_type=MemoryType.CREW_SHARED,
            content='Test',
            tags=['test'],
            importance=5
        )
        assert result is False
        
        # Test invalid importance
        result = memory_manager.store_memory(
            agent_role='brand_author',
            memory_type=MemoryType.CREW_SHARED,
            content='Test',
            tags=['test'],
            importance=15  # Invalid, should be 1-10
        )
        assert result is False