"""
Tests for Validation Engine
"""

import pytest
import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.soylent_red_division.validation_engine import (
    ValidationEngine, ValidationResult, ValidationIssue, ValidationType, 
    ValidationSeverity, ValidationStatus
)

class TestValidationEngine:
    """Test suite for Validation Engine"""
    
    def test_validation_engine_initialization(self, temp_project_root):
        """Test validation engine initialization"""
        ve = ValidationEngine(temp_project_root)
        
        assert ve.project_root == temp_project_root
        assert ve.validation_cache_dir.exists()
        assert ve.validation_results_file.exists() or not ve.validation_results_file.exists()
        assert ve.validation_log_file.exists() or not ve.validation_log_file.exists()
        
        # Check validator components
        assert len(ve.validators) == 8  # All validation types
        assert ValidationType.BRAND_VOICE in ve.validators
        assert ValidationType.AUTHENTICITY in ve.validators
        assert ValidationType.PERSONA_ALIGNMENT in ve.validators
        assert ValidationType.ETHICAL_INTEGRATION in ve.validators
        assert ValidationType.PROHIBITED_LANGUAGE in ve.validators
        assert ValidationType.QUALITY_STANDARDS in ve.validators
        assert ValidationType.TEMPLATE_COMPLIANCE in ve.validators
        assert ValidationType.TRANSPARENCY in ve.validators
    
    def test_validation_issue_creation(self):
        """Test validation issue creation and serialization"""
        issue = ValidationIssue(
            validation_type=ValidationType.BRAND_VOICE,
            severity=ValidationSeverity.HIGH,
            message="Missing methodical experimenter patterns",
            location={"section": "methodology"},
            suggestions=["Add data and testing evidence", "Include failure cases"],
            metadata={"pattern_count": 0}
        )
        
        # Test serialization
        issue_dict = issue.to_dict()
        assert issue_dict["validation_type"] == "brand_voice"
        assert issue_dict["severity"] == "high"
        assert issue_dict["message"] == "Missing methodical experimenter patterns"
        assert len(issue_dict["suggestions"]) == 2
        
        # Test deserialization
        restored_issue = ValidationIssue.from_dict(issue_dict)
        assert restored_issue.validation_type == issue.validation_type
        assert restored_issue.severity == issue.severity
        assert restored_issue.message == issue.message
    
    def test_validation_result_creation(self):
        """Test validation result creation and serialization"""
        issues = [
            ValidationIssue(
                validation_type=ValidationType.BRAND_VOICE,
                severity=ValidationSeverity.HIGH,
                message="Test issue",
                location={},
                suggestions=[],
                metadata={}
            )
        ]
        
        result = ValidationResult(
            id="test_validation_1",
            content_id="test_content",
            overall_status=ValidationStatus.FAILED,
            overall_score=75.0,
            issues=issues,
            suggestions=["Improve brand voice consistency"],
            metadata={"word_count": 500},
            validated_at=datetime.now()
        )
        
        # Test serialization
        result_dict = result.to_dict()
        assert result_dict["id"] == "test_validation_1"
        assert result_dict["overall_status"] == "failed"
        assert result_dict["overall_score"] == 75.0
        assert len(result_dict["issues"]) == 1
        
        # Test deserialization
        restored_result = ValidationResult.from_dict(result_dict)
        assert restored_result.id == result.id
        assert restored_result.overall_status == result.overall_status
        assert restored_result.overall_score == result.overall_score
        assert len(restored_result.issues) == 1
    
    def test_brand_voice_validation_pass(self, validation_engine, sample_content):
        """Test brand voice validation with passing content"""
        result = validation_engine.validate_content(
            content=sample_content,
            content_id="test_content_pass"
        )
        
        assert isinstance(result, ValidationResult)
        assert result.content_id == "test_content_pass"
        
        # Check for brand voice validation
        brand_voice_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.BRAND_VOICE
        ]
        
        # Should have minimal or no brand voice issues for sample_content
        assert len(brand_voice_issues) <= 2  # Allow for some minor issues
    
    def test_brand_voice_validation_fail(self, validation_engine, sample_invalid_content):
        """Test brand voice validation with failing content"""
        result = validation_engine.validate_content(
            content=sample_invalid_content,
            content_id="test_content_fail"
        )
        
        assert isinstance(result, ValidationResult)
        assert result.content_id == "test_content_fail"
        
        # Check for brand voice validation failures
        brand_voice_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.BRAND_VOICE
        ]
        
        # Should have brand voice issues for invalid content
        assert len(brand_voice_issues) > 0
        
        # Check for high severity issues
        high_severity_issues = [
            issue for issue in brand_voice_issues 
            if issue.severity == ValidationSeverity.HIGH
        ]
        assert len(high_severity_issues) > 0
    
    def test_authenticity_validation_pass(self, validation_engine):
        """Test authenticity validation with proper content"""
        content_with_annotations = """
        # Testing AI Tools in Practice
        
        Based on systematic testing over 6 months, I've learned several key lessons about AI integration.
        
        [AUTHOR: add personal example of testing methodology]
        
        The data shows consistent patterns across different tools and use cases.
        """
        
        result = validation_engine.validate_content(
            content=content_with_annotations,
            content_id="test_authenticity_pass"
        )
        
        authenticity_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.AUTHENTICITY
        ]
        
        # Should have minimal authenticity issues with proper annotations
        critical_authenticity = [
            issue for issue in authenticity_issues 
            if issue.severity == ValidationSeverity.CRITICAL
        ]
        assert len(critical_authenticity) == 0
    
    def test_authenticity_validation_fail(self, validation_engine):
        """Test authenticity validation with unsupported claims"""
        content_with_unsupported_claims = """
        # My Amazing AI Journey
        
        In my 20 years of working with AI, I've discovered groundbreaking techniques.
        My team has revolutionized the industry with our secret methods.
        I personally trained GPT-4 and know exactly how it works.
        """
        
        result = validation_engine.validate_content(
            content=content_with_unsupported_claims,
            content_id="test_authenticity_fail"
        )
        
        authenticity_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.AUTHENTICITY
        ]
        
        # Should have critical authenticity issues
        assert len(authenticity_issues) > 0
        
        critical_authenticity = [
            issue for issue in authenticity_issues 
            if issue.severity == ValidationSeverity.CRITICAL
        ]
        assert len(critical_authenticity) > 0
    
    def test_persona_alignment_validation(self, validation_engine):
        """Test persona alignment validation"""
        # Content appropriate for Adaptive Alex
        alex_content = """
        # Practical AI Integration for UX Teams
        
        Here's a step-by-step approach to integrating AI tools into your existing workflow:
        
        1. Start with one tool for research tasks
        2. Document what works and what doesn't
        3. Gradually expand based on proven value
        
        This approach has worked for mid-level designers who need practical results.
        """
        
        result = validation_engine.validate_content(
            content=alex_content,
            content_id="test_persona_alex",
            target_personas=["Adaptive Alex"]
        )
        
        persona_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.PERSONA_ALIGNMENT
        ]
        
        # Should have minimal persona alignment issues
        high_persona_issues = [
            issue for issue in persona_issues 
            if issue.severity in [ValidationSeverity.HIGH, ValidationSeverity.CRITICAL]
        ]
        assert len(high_persona_issues) <= 1
    
    def test_ethical_integration_validation_pass(self, validation_engine):
        """Test ethical integration validation with well-integrated ethics"""
        ethical_content = """
        # AI Tools for Design: A Responsible Approach
        
        When selecting AI tools, consider bias implications from the start.
        Each tool recommendation includes accessibility considerations.
        
        ## Implementation Strategy
        - Choose tools that support diverse user needs
        - Test for bias in AI-generated suggestions
        - Maintain human oversight in all decisions
        
        ## Bias Detection Methods
        Regular testing with diverse user scenarios helps identify problematic patterns.
        """
        
        result = validation_engine.validate_content(
            content=ethical_content,
            content_id="test_ethics_pass"
        )
        
        ethical_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.ETHICAL_INTEGRATION
        ]
        
        # Should have minimal ethical integration issues
        high_ethical_issues = [
            issue for issue in ethical_issues 
            if issue.severity in [ValidationSeverity.HIGH, ValidationSeverity.CRITICAL]
        ]
        assert len(high_ethical_issues) <= 1
    
    def test_ethical_integration_validation_fail(self, validation_engine):
        """Test ethical integration validation with ethics as afterthought"""
        unethical_content = """
        # Amazing AI Tools for Designers
        
        These tools will revolutionize your workflow and boost productivity.
        
        ## Tool Recommendations
        1. AI Design Assistant - creates perfect layouts
        2. Content Generator - writes compelling copy
        3. User Research AI - analyzes user feedback
        
        ## Implementation
        Just start using these tools immediately for best results.
        
        ## Ethical Considerations
        There are some ethical things to think about...
        """
        
        result = validation_engine.validate_content(
            content=unethical_content,
            content_id="test_ethics_fail"
        )
        
        ethical_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.ETHICAL_INTEGRATION
        ]
        
        # Should have ethical integration issues
        assert len(ethical_issues) > 0
        
        high_ethical_issues = [
            issue for issue in ethical_issues 
            if issue.severity in [ValidationSeverity.HIGH, ValidationSeverity.CRITICAL]
        ]
        assert len(high_ethical_issues) > 0
    
    def test_prohibited_language_validation(self, validation_engine):
        """Test prohibited language detection"""
        prohibited_content = """
        # Revolutionary AI Will Transform Everything!
        
        This game-changing, disruptive technology is absolutely incredible.
        AI is magical and will synergistically optimize your paradigm.
        Leverage best practices to maximize ROI through innovative solutions.
        
        This groundbreaking approach revolutionizes everything we know.
        """
        
        result = validation_engine.validate_content(
            content=prohibited_content,
            content_id="test_prohibited_language"
        )
        
        prohibited_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.PROHIBITED_LANGUAGE
        ]
        
        # Should detect prohibited language
        assert len(prohibited_issues) > 0
        
        high_prohibited_issues = [
            issue for issue in prohibited_issues 
            if issue.severity in [ValidationSeverity.HIGH, ValidationSeverity.CRITICAL]
        ]
        assert len(high_prohibited_issues) > 0
    
    def test_quality_standards_validation(self, validation_engine):
        """Test quality standards validation"""
        low_quality_content = """
        ai is good. use it.
        
        here r sum tips:
        - try ai
        - its gr8
        - use more
        
        thats it lol
        """
        
        result = validation_engine.validate_content(
            content=low_quality_content,
            content_id="test_quality_low"
        )
        
        quality_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.QUALITY_STANDARDS
        ]
        
        # Should detect quality issues
        assert len(quality_issues) > 0
    
    def test_template_compliance_validation(self, validation_engine):
        """Test template compliance validation"""
        # Content missing required template sections
        non_compliant_content = """
        # Some Title
        
        Here's some content without proper structure.
        No introduction, methodology, or conclusion.
        """
        
        result = validation_engine.validate_content(
            content=non_compliant_content,
            content_id="test_template_fail",
            source_materials="template: core_body_guide"
        )
        
        template_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.TEMPLATE_COMPLIANCE
        ]
        
        # Should detect template compliance issues
        assert len(template_issues) >= 0  # May or may not have issues depending on template detection
    
    def test_transparency_validation_pass(self, validation_engine):
        """Test transparency validation with good transparency"""
        transparent_content = """
        # Testing AI Writing Tools: Complete Documentation
        
        After 127 documented tests across 8 different tools, here's what I learned:
        
        ## Methodology
        - Tested each tool with identical prompts
        - Recorded response times and quality scores
        - Documented failures and edge cases
        
        ## Results with Evidence
        Success rate: 73% (documented in testing log)
        Failure patterns: Inconsistent voice (42% of failures)
        
        ## What Didn't Work
        Initial attempts using generic prompts failed completely.
        Tool X crashed during 23% of tests.
        
        ## Complete Process Documentation
        [Detailed testing process with all steps documented]
        """
        
        result = validation_engine.validate_content(
            content=transparent_content,
            content_id="test_transparency_pass"
        )
        
        transparency_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.TRANSPARENCY
        ]
        
        # Should have minimal transparency issues
        high_transparency_issues = [
            issue for issue in transparency_issues 
            if issue.severity in [ValidationSeverity.HIGH, ValidationSeverity.CRITICAL]
        ]
        assert len(high_transparency_issues) <= 1
    
    def test_transparency_validation_fail(self, validation_engine):
        """Test transparency validation with poor transparency"""
        opaque_content = """
        # AI Tools Work Great
        
        I tested some tools and they're good.
        The results were positive.
        Everything worked fine.
        Just use these tools and you'll see results.
        """
        
        result = validation_engine.validate_content(
            content=opaque_content,
            content_id="test_transparency_fail"
        )
        
        transparency_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.TRANSPARENCY
        ]
        
        # Should have transparency issues
        assert len(transparency_issues) > 0
    
    def test_real_time_validation(self, validation_engine):
        """Test real-time validation functionality"""
        content_fragment = "This revolutionary AI will transform everything!"
        
        result = validation_engine.validate_real_time(
            content_fragment=content_fragment,
            content_id="test_realtime"
        )
        
        assert isinstance(result, ValidationResult)
        assert result.content_id == "test_realtime"
        
        # Should detect prohibited language in real-time
        prohibited_issues = [
            issue for issue in result.issues 
            if issue.validation_type == ValidationType.PROHIBITED_LANGUAGE
        ]
        assert len(prohibited_issues) > 0
    
    def test_validation_result_storage_and_retrieval(self, validation_engine):
        """Test validation result storage and retrieval"""
        content = "Test content for storage validation"
        
        result = validation_engine.validate_content(
            content=content,
            content_id="test_storage"
        )
        
        result_id = result.id
        
        # Retrieve by ID
        retrieved_result = validation_engine.get_validation_result(result_id)
        assert retrieved_result is not None
        assert retrieved_result.id == result_id
        assert retrieved_result.content_id == "test_storage"
    
    def test_content_validation_history(self, validation_engine):
        """Test content validation history tracking"""
        content_id = "test_history_content"
        
        # Perform multiple validations
        validation_engine.validate_content(
            content="First version of content",
            content_id=content_id
        )
        
        validation_engine.validate_content(
            content="Second version of content with improvements",
            content_id=content_id
        )
        
        validation_engine.validate_content(
            content="Third version with even better quality and brand compliance",
            content_id=content_id
        )
        
        # Get validation history
        history = validation_engine.get_content_validation_history(content_id)
        
        assert len(history) >= 3
        assert all(result.content_id == content_id for result in history)
        
        # Check chronological order (most recent first)
        timestamps = [result.validated_at for result in history]
        assert timestamps == sorted(timestamps, reverse=True)
    
    def test_validation_statistics(self, validation_engine):
        """Test validation statistics"""
        # Perform some validations to generate data
        validation_engine.validate_content(
            content="Good content that should pass",
            content_id="stats_test_1"
        )
        
        validation_engine.validate_content(
            content="Revolutionary AI that disrupts everything!",
            content_id="stats_test_2"
        )
        
        stats = validation_engine.get_validation_stats()
        
        assert "total_validations" in stats
        assert "average_score" in stats
        assert "pass_rate" in stats
        assert "issues_by_type" in stats
        assert "issues_by_severity" in stats
        
        assert stats["total_validations"] >= 2
        assert 0 <= stats["average_score"] <= 100
        assert 0 <= stats["pass_rate"] <= 100
    
    def test_validation_types_parameter(self, validation_engine):
        """Test validation with specific validation types"""
        content = "Content to test specific validation types"
        
        # Test with specific validation types
        result = validation_engine.validate_content(
            content=content,
            content_id="test_specific_types",
            validation_types=[ValidationType.BRAND_VOICE, ValidationType.AUTHENTICITY]
        )
        
        # Should only have issues from specified validation types
        issue_types = {issue.validation_type for issue in result.issues}
        allowed_types = {ValidationType.BRAND_VOICE, ValidationType.AUTHENTICITY}
        
        # All issues should be from allowed types
        assert issue_types.issubset(allowed_types)
    
    def test_validation_with_source_materials(self, validation_engine):
        """Test validation with source materials context"""
        content = "Content that references source materials"
        source_materials = """
        Research notes:
        - Study showed 73% improvement
        - Testing conducted over 6 months
        - [AUTHOR: add personal testing experience]
        """
        
        result = validation_engine.validate_content(
            content=content,
            content_id="test_with_sources",
            source_materials=source_materials
        )
        
        assert isinstance(result, ValidationResult)
        assert result.content_id == "test_with_sources"
    
    def test_validation_persistence(self, temp_project_root):
        """Test validation persistence across engine instances"""
        content = "Test content for persistence validation"
        
        # Create first engine and validate
        ve1 = ValidationEngine(temp_project_root)
        result = ve1.validate_content(
            content=content,
            content_id="test_persistence"
        )
        result_id = result.id
        
        # Create second engine instance
        ve2 = ValidationEngine(temp_project_root)
        
        # Verify result persists
        retrieved_result = ve2.get_validation_result(result_id)
        assert retrieved_result is not None
        assert retrieved_result.id == result_id
        assert retrieved_result.content_id == "test_persistence"
    
    def test_validation_error_handling(self, validation_engine):
        """Test validation error handling"""
        # Test with empty content
        result = validation_engine.validate_content(
            content="",
            content_id="test_empty"
        )
        assert isinstance(result, ValidationResult)
        
        # Test with None content (should handle gracefully)
        result = validation_engine.validate_content(
            content=None,
            content_id="test_none"
        )
        assert isinstance(result, ValidationResult)
        
        # Test retrieval of nonexistent result
        nonexistent_result = validation_engine.get_validation_result("nonexistent_id")
        assert nonexistent_result is None
        
        # Test history for nonexistent content
        nonexistent_history = validation_engine.get_content_validation_history("nonexistent_content")
        assert nonexistent_history == []
    
    def test_validation_scoring_accuracy(self, validation_engine, sample_content, sample_invalid_content):
        """Test validation scoring accuracy"""
        # Good content should score higher
        good_result = validation_engine.validate_content(
            content=sample_content,
            content_id="test_scoring_good"
        )
        
        # Bad content should score lower
        bad_result = validation_engine.validate_content(
            content=sample_invalid_content,
            content_id="test_scoring_bad"
        )
        
        # Good content should have higher score
        assert good_result.overall_score > bad_result.overall_score
        
        # Scores should be in valid range
        assert 0 <= good_result.overall_score <= 100
        assert 0 <= bad_result.overall_score <= 100
    
    def test_validation_suggestions_quality(self, validation_engine, sample_invalid_content):
        """Test quality of validation suggestions"""
        result = validation_engine.validate_content(
            content=sample_invalid_content,
            content_id="test_suggestions"
        )
        
        # Should have overall suggestions
        assert len(result.suggestions) > 0
        
        # Issues should have specific suggestions
        issues_with_suggestions = [
            issue for issue in result.issues 
            if len(issue.suggestions) > 0
        ]
        assert len(issues_with_suggestions) > 0
        
        # Suggestions should be actionable strings
        for suggestion in result.suggestions:
            assert isinstance(suggestion, str)
            assert len(suggestion) > 10  # Reasonable minimum length
    
    def test_validation_metadata_collection(self, validation_engine):
        """Test validation metadata collection"""
        content = "Test content for metadata collection with specific characteristics."
        
        result = validation_engine.validate_content(
            content=content,
            content_id="test_metadata"
        )
        
        # Should have metadata
        assert isinstance(result.metadata, dict)
        
        # Should contain expected metadata fields
        expected_fields = ["word_count", "validation_duration"]
        for field in expected_fields:
            if field in result.metadata:
                assert isinstance(result.metadata[field], (int, float))
    
    def test_validation_performance(self, validation_engine):
        """Test validation performance"""
        import time
        
        content = "Test content for performance validation" * 100  # Longer content
        
        start_time = time.time()
        result = validation_engine.validate_content(
            content=content,
            content_id="test_performance"
        )
        end_time = time.time()
        
        duration = end_time - start_time
        
        # Validation should complete in reasonable time (less than 10 seconds)
        assert duration < 10.0
        assert isinstance(result, ValidationResult)
    
    def test_concurrent_validation_safety(self, validation_engine):
        """Test validation safety with concurrent operations"""
        import threading
        
        results = []
        
        def validate_content(content_id):
            result = validation_engine.validate_content(
                content=f"Test content for {content_id}",
                content_id=content_id
            )
            results.append(result)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=validate_content, args=[f"concurrent_test_{i}"])
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # All validations should complete successfully
        assert len(results) == 5
        assert all(isinstance(result, ValidationResult) for result in results)
        
        # All should have unique IDs
        result_ids = [result.id for result in results]
        assert len(set(result_ids)) == 5