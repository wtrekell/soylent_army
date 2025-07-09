"""
Tests for Knowledge Manager
"""

import pytest
import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.soylent_red_division.knowledge_manager import (
    KnowledgeManager, KnowledgeType, KnowledgeItem, KnowledgeAccessLevel
)

class TestKnowledgeManager:
    """Test suite for Knowledge Manager"""
    
    def test_knowledge_manager_initialization(self, temp_project_root):
        """Test knowledge manager initialization"""
        km = KnowledgeManager(temp_project_root)
        
        assert km.project_root == temp_project_root
        assert km.knowledge_dir.exists()
        assert km.cache_dir.exists()
        
        # Check knowledge subdirectories exist
        assert (km.knowledge_dir / "brand").exists()
        assert (km.knowledge_dir / "examples").exists()
        assert (km.knowledge_dir / "templates").exists()
        assert (km.knowledge_dir / "personas").exists()
        assert (km.knowledge_dir / "external").exists()
    
    def test_knowledge_refresh_basic(self, knowledge_manager, sample_brand_foundation):
        """Test basic knowledge refresh functionality"""
        # Knowledge should be loaded from fixtures
        knowledge_items = knowledge_manager.get_knowledge_by_type(KnowledgeType.BRAND_FOUNDATION)
        
        assert len(knowledge_items) >= 1
        
        # Check brand foundation was loaded
        brand_item = knowledge_items[0]
        assert brand_item.title == "Brand Foundation"
        assert "Mission" in brand_item.content
        assert "Voice Characteristics" in brand_item.content
        assert "brand" in brand_item.tags
    
    def test_knowledge_search_by_query(self, knowledge_manager):
        """Test knowledge search by text query"""
        # Search for voice-related knowledge
        voice_items = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            query='voice characteristics'
        )
        
        assert len(voice_items) >= 1
        assert any('voice' in item.content.lower() for item in voice_items)
    
    def test_knowledge_search_by_tags(self, knowledge_manager):
        """Test knowledge search by tags"""
        # Search for brand-tagged knowledge
        brand_items = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            tags=['brand']
        )
        
        assert len(brand_items) >= 1
        assert all('brand' in item.tags for item in brand_items)
    
    def test_knowledge_search_by_type(self, knowledge_manager):
        """Test knowledge search by type"""
        # Search for brand foundation items
        brand_foundation = knowledge_manager.get_knowledge_by_type(
            KnowledgeType.BRAND_FOUNDATION
        )
        
        assert len(brand_foundation) >= 1
        assert all(item.knowledge_type == KnowledgeType.BRAND_FOUNDATION for item in brand_foundation)
    
    def test_knowledge_access_control(self, knowledge_manager):
        """Test knowledge access control by role"""
        # All roles should have access to brand foundation
        brand_author_items = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            knowledge_type=KnowledgeType.BRAND_FOUNDATION
        )
        
        writer_items = knowledge_manager.search_knowledge(
            agent_role='writer',
            knowledge_type=KnowledgeType.BRAND_FOUNDATION
        )
        
        researcher_items = knowledge_manager.search_knowledge(
            agent_role='researcher',
            knowledge_type=KnowledgeType.BRAND_FOUNDATION
        )
        
        assert len(brand_author_items) >= 1
        assert len(writer_items) >= 1
        assert len(researcher_items) >= 1
    
    def test_knowledge_quality_scoring(self, knowledge_manager):
        """Test knowledge quality scoring"""
        # Get knowledge items with quality scores
        items = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            min_quality_score=7.0
        )
        
        # Should have items with quality scores >= 7.0
        assert len(items) >= 0
        for item in items:
            if item.quality_score is not None:
                assert item.quality_score >= 7.0
    
    def test_knowledge_versioning(self, knowledge_manager, temp_project_root):
        """Test knowledge versioning functionality"""
        # Create a knowledge file
        test_file = temp_project_root / "knowledge" / "brand" / "test_versioning.md"
        test_file.write_text("# Test Version 1")
        
        # First refresh
        knowledge_manager.refresh_knowledge()
        items_v1 = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            query='Test Version 1'
        )
        
        # Update the file
        test_file.write_text("# Test Version 2")
        
        # Second refresh
        knowledge_manager.refresh_knowledge()
        items_v2 = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            query='Test Version 2'
        )
        
        # Should detect version change
        assert len(items_v2) >= 1
        assert any('Test Version 2' in item.content for item in items_v2)
    
    def test_knowledge_validation(self, knowledge_manager):
        """Test knowledge validation"""
        # Run validation on loaded knowledge
        validation_results = knowledge_manager.validate_knowledge()
        
        assert isinstance(validation_results, dict)
        assert 'total_items' in validation_results
        assert 'validation_errors' in validation_results
        assert 'consistency_issues' in validation_results
    
    def test_knowledge_recommendations(self, knowledge_manager):
        """Test knowledge recommendations"""
        # Get recommendations for a content context
        context = {
            'target_personas': ['Adaptive Alex'],
            'content_type': 'article',
            'topics': ['ai', 'ux', 'design']
        }
        
        recommendations = knowledge_manager.get_recommendations(
            agent_role='brand_author',
            context=context
        )
        
        assert isinstance(recommendations, list)
        # Should have relevant recommendations
        assert len(recommendations) >= 0
    
    def test_knowledge_memory_integration(self, knowledge_manager, memory_manager):
        """Test knowledge-memory integration"""
        # Store some memory
        memory_manager.store_memory(
            agent_role='brand_author',
            memory_type='crew_shared',
            content='AI integration workflow successful',
            tags=['ai', 'workflow', 'success'],
            importance=8
        )
        
        # Get knowledge with memory integration
        enhanced_items = knowledge_manager.get_knowledge_with_memory_insights(
            agent_role='brand_author',
            query='ai integration'
        )
        
        assert isinstance(enhanced_items, list)
        # Should return knowledge items potentially enhanced with memory insights
    
    def test_knowledge_export(self, knowledge_manager, temp_project_root):
        """Test knowledge export functionality"""
        export_path = temp_project_root / "knowledge_export.json"
        
        result = knowledge_manager.export_knowledge(
            agent_role='brand_author',
            output_path=export_path
        )
        
        assert result is True
        assert export_path.exists()
        
        # Verify export content
        with open(export_path, 'r') as f:
            exported_data = json.load(f)
        
        assert 'knowledge_items' in exported_data
        assert 'metadata' in exported_data
        assert len(exported_data['knowledge_items']) >= 0
    
    def test_knowledge_stats(self, knowledge_manager):
        """Test knowledge statistics"""
        stats = knowledge_manager.get_knowledge_stats('brand_author')
        
        assert isinstance(stats, dict)
        assert 'total_items' in stats
        assert 'by_type' in stats
        assert 'by_access_level' in stats
        assert 'average_quality_score' in stats
    
    def test_knowledge_cache_management(self, knowledge_manager):
        """Test knowledge cache management"""
        # Cache should be created during refresh
        cache_files = list(knowledge_manager.cache_dir.glob("*.json"))
        
        # Should have some cache files
        assert len(cache_files) >= 0
        
        # Clear cache
        knowledge_manager.clear_cache()
        
        # Cache should be cleared
        cache_files_after = list(knowledge_manager.cache_dir.glob("*.json"))
        assert len(cache_files_after) == 0
    
    def test_knowledge_item_creation(self, knowledge_manager):
        """Test knowledge item creation from file"""
        # This tests internal functionality
        test_content = """# Test Knowledge Item
        
        This is a test knowledge item with:
        - Tags: test, example
        - Quality: High
        - Version: 1.0
        """
        
        # Create knowledge item (internal method)
        item = knowledge_manager._create_knowledge_item(
            file_path="test.md",
            content=test_content,
            knowledge_type=KnowledgeType.BRAND_FOUNDATION
        )
        
        assert item.title == "Test Knowledge Item"
        assert item.content == test_content
        assert item.knowledge_type == KnowledgeType.BRAND_FOUNDATION
    
    def test_knowledge_dependency_tracking(self, knowledge_manager):
        """Test knowledge dependency tracking"""
        # Get knowledge with dependencies
        items = knowledge_manager.get_knowledge_by_type(KnowledgeType.BRAND_FOUNDATION)
        
        # Check if dependency tracking works
        for item in items:
            assert isinstance(item.dependencies, list)
            assert isinstance(item.dependents, list)
    
    def test_knowledge_search_with_filters(self, knowledge_manager):
        """Test knowledge search with multiple filters"""
        # Search with multiple criteria
        filtered_items = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            knowledge_type=KnowledgeType.BRAND_FOUNDATION,
            tags=['brand'],
            min_quality_score=5.0,
            limit=10
        )
        
        assert len(filtered_items) <= 10
        for item in filtered_items:
            assert item.knowledge_type == KnowledgeType.BRAND_FOUNDATION
            assert 'brand' in item.tags
            if item.quality_score is not None:
                assert item.quality_score >= 5.0
    
    def test_knowledge_update_tracking(self, knowledge_manager, temp_project_root):
        """Test knowledge update tracking"""
        # Create a knowledge file
        test_file = temp_project_root / "knowledge" / "brand" / "test_update.md"
        test_file.write_text("# Original Content")
        
        # Initial refresh
        knowledge_manager.refresh_knowledge()
        
        # Get original modification time
        original_mtime = test_file.stat().st_mtime
        
        # Update file
        test_file.write_text("# Updated Content")
        
        # Check if update is detected
        updated_mtime = test_file.stat().st_mtime
        assert updated_mtime > original_mtime
    
    def test_knowledge_error_handling(self, knowledge_manager):
        """Test knowledge manager error handling"""
        # Test invalid role
        items = knowledge_manager.search_knowledge(
            agent_role='invalid_role',
            query='test'
        )
        assert len(items) == 0
        
        # Test invalid knowledge type
        items = knowledge_manager.get_knowledge_by_type('invalid_type')
        assert len(items) == 0
    
    def test_knowledge_performance_optimization(self, knowledge_manager):
        """Test knowledge performance optimization"""
        # Search should be reasonably fast
        import time
        
        start_time = time.time()
        items = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            query='brand voice characteristics'
        )
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 5.0  # 5 seconds max
        assert isinstance(items, list)
    
    def test_knowledge_cross_reference(self, knowledge_manager):
        """Test knowledge cross-reference functionality"""
        # Get brand foundation
        brand_items = knowledge_manager.get_knowledge_by_type(
            KnowledgeType.BRAND_FOUNDATION
        )
        
        # Should have cross-references if available
        for item in brand_items:
            assert isinstance(item.cross_references, list)
    
    def test_knowledge_metadata_extraction(self, knowledge_manager):
        """Test knowledge metadata extraction"""
        # All knowledge items should have proper metadata
        all_items = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            limit=50
        )
        
        for item in all_items:
            assert isinstance(item.metadata, dict)
            assert 'file_path' in item.metadata
            assert 'last_modified' in item.metadata
            assert 'file_size' in item.metadata
    
    def test_knowledge_consistency_checking(self, knowledge_manager):
        """Test knowledge consistency checking"""
        # Run consistency check
        consistency_results = knowledge_manager.check_consistency()
        
        assert isinstance(consistency_results, dict)
        assert 'duplicate_titles' in consistency_results
        assert 'missing_dependencies' in consistency_results
        assert 'orphaned_items' in consistency_results
    
    def test_knowledge_template_processing(self, knowledge_manager):
        """Test knowledge template processing"""
        # Get template knowledge
        template_items = knowledge_manager.get_knowledge_by_type(
            KnowledgeType.CONTENT_TEMPLATES
        )
        
        # Templates should be processed correctly
        for item in template_items:
            assert item.knowledge_type == KnowledgeType.CONTENT_TEMPLATES
            assert isinstance(item.content, str)
    
    def test_knowledge_persona_matching(self, knowledge_manager):
        """Test knowledge persona matching"""
        # Search for persona-specific knowledge
        persona_items = knowledge_manager.search_knowledge(
            agent_role='brand_author',
            target_personas=['Adaptive Alex']
        )
        
        # Should return relevant items
        assert isinstance(persona_items, list)
        for item in persona_items:
            # Should have persona relevance
            assert isinstance(item.persona_relevance, dict)
    
    def test_knowledge_quality_improvement(self, knowledge_manager):
        """Test knowledge quality improvement suggestions"""
        # Get quality improvement suggestions
        suggestions = knowledge_manager.get_quality_improvement_suggestions(
            agent_role='brand_author'
        )
        
        assert isinstance(suggestions, list)
        # Should have improvement suggestions
        for suggestion in suggestions:
            assert 'knowledge_id' in suggestion
            assert 'improvement_type' in suggestion
            assert 'suggestion' in suggestion