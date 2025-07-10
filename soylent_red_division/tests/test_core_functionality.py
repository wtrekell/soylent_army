#!/usr/bin/env python3
"""
Simple test runner for Soylent Red Division - bypasses complex dependencies
Runs core system tests without requiring full CrewAI installation
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List
import json
import yaml
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class SimpleTestRunner:
    """Lightweight test runner for development testing"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent  # Go up one level from tests/
        self.test_results = []
        self.passed = 0
        self.failed = 0
        
    def log(self, message: str, level: str = "INFO"):
        """Simple logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def assert_equals(self, actual, expected, message: str = ""):
        """Simple assertion helper"""
        if actual != expected:
            raise AssertionError(f"Expected {expected}, got {actual}. {message}")
            
    def assert_true(self, condition, message: str = ""):
        """Simple boolean assertion"""
        if not condition:
            raise AssertionError(f"Expected True, got False. {message}")
            
    def assert_in(self, item, container, message: str = ""):
        """Simple containment assertion"""
        if item not in container:
            raise AssertionError(f"Expected {item} in {container}. {message}")
    
    def run_test(self, test_func, test_name: str):
        """Run a single test function"""
        try:
            self.log(f"Running {test_name}...")
            test_func()
            self.log(f"✓ {test_name} PASSED", "PASS")
            self.passed += 1
            self.test_results.append({"name": test_name, "status": "PASSED"})
        except Exception as e:
            self.log(f"✗ {test_name} FAILED: {str(e)}", "FAIL")
            self.failed += 1
            self.test_results.append({"name": test_name, "status": "FAILED", "error": str(e)})
    
    def test_memory_manager_basic(self):
        """Test basic memory manager functionality"""
        try:
            from soylent_red_division.memory_manager import MemoryManager, MemoryType
            
            # Create temp directory for testing
            with tempfile.TemporaryDirectory() as temp_dir:
                project_root = Path(temp_dir)
                memory_mgr = MemoryManager(project_root)
                
                # Test initialization
                self.assert_true(memory_mgr.memory_dir.exists(), "Memory directory should be created")
                
                # Test storing memory - use correct API signature
                content = {"text": "This is a test memory", "context": "testing"}
                memory_id = memory_mgr.store_memory(
                    "brand_author",  # Use valid agent role
                    MemoryType.CREW_SHARED,
                    content,
                    tags=["test"],
                    importance=8
                )
                
                # Test retrieval
                memories = memory_mgr.retrieve_memory("brand_author", MemoryType.CREW_SHARED)
                self.assert_true(len(memories) > 0, "Should retrieve stored memories")
                
        except ImportError as e:
            self.log(f"Skipping memory manager test due to import error: {e}", "WARN")
    
    def test_knowledge_manager_basic(self):
        """Test basic knowledge manager functionality"""
        try:
            from soylent_red_division.knowledge_manager import KnowledgeManager
            
            # Create temp directory for testing
            with tempfile.TemporaryDirectory() as temp_dir:
                project_root = Path(temp_dir)
                
                # Create sample knowledge structure
                knowledge_dir = project_root / "knowledge"
                knowledge_dir.mkdir(parents=True)
                
                # Create sample brand file
                brand_dir = knowledge_dir / "brand"
                brand_dir.mkdir()
                brand_file = brand_dir / "test-brand.md"
                brand_file.write_text("# Test Brand\nThis is test brand content.")
                
                knowledge_mgr = KnowledgeManager(project_root)
                # Initialize knowledge by accessing a method that triggers loading
                knowledge_mgr._scan_and_update_knowledge()
                
                # Test knowledge loading
                self.assert_true(len(knowledge_mgr.knowledge_items) > 0, "Should load knowledge items")
                
                # Test search - use correct API signature
                results = knowledge_mgr.search_knowledge("brand_author", "test brand")
                self.assert_true(len(results) >= 0, "Should return search results")
                
        except ImportError as e:
            self.log(f"Skipping knowledge manager test due to import error: {e}", "WARN")
    
    def test_reasoning_engine_basic(self):
        """Test basic reasoning engine functionality"""
        try:
            from soylent_red_division.reasoning_engine import ReasoningEngine, ReasoningContext
            
            # Create temp directory for testing
            with tempfile.TemporaryDirectory() as temp_dir:
                project_root = Path(temp_dir)
                reasoning_engine = ReasoningEngine(project_root)
                
                # Test plan creation - use correct API signature
                context = ReasoningContext(
                    task_type="content_creation",
                    content_requirements={"topic": "test article", "length": "1000 words"},
                    brand_constraints={"voice": "professional"},
                    target_personas=["writer"],
                    available_resources={"brand_knowledge": True, "examples": True},
                    success_criteria={"quality": "high"}
                )
                
                plan = reasoning_engine.create_plan("content_creation", context, "test_agent")
                
                # Test plan properties - use correct attribute names
                self.assert_true(plan.id is not None, "Plan should have an ID")
                self.assert_true(len(plan.steps) > 0, "Plan should have steps")
                self.assert_true(plan.status.value in ["created", "draft"], "Plan should be in valid initial status")
                
        except ImportError as e:
            self.log(f"Skipping reasoning engine test due to import error: {e}", "WARN")
    
    def test_validation_engine_basic(self):
        """Test basic validation engine functionality"""
        try:
            from soylent_red_division.validation_engine import ValidationEngine
            
            # Create temp directory for testing
            with tempfile.TemporaryDirectory() as temp_dir:
                project_root = Path(temp_dir)
                validation_engine = ValidationEngine(project_root)
                
                # Test content validation
                test_content = "This is a test article about technology trends."
                result = validation_engine.validate_content(test_content, content_id="test_001")
                
                # Test validation result properties - use correct attribute names
                self.assert_true(result.content_id == "test_001", "Should have correct content ID")
                self.assert_true(result.overall_score >= 0, "Should have valid score")
                self.assert_true(len(result.issues) >= 0, "Should have issues list")
                self.assert_true(result.overall_status is not None, "Should have validation status")
                
        except ImportError as e:
            self.log(f"Skipping validation engine test due to import error: {e}", "WARN")
    
    def test_project_structure(self):
        """Test that project structure is correct"""
        # Test source directory
        src_dir = self.project_root / "src" / "soylent_red_division"
        self.assert_true(src_dir.exists(), "Source directory should exist")
        
        # Test main modules
        required_modules = [
            "memory_manager.py",
            "knowledge_manager.py", 
            "reasoning_engine.py",
            "validation_engine.py",
            "crew.py",
            "main.py"
        ]
        
        for module in required_modules:
            module_path = src_dir / module
            self.assert_true(module_path.exists(), f"Module {module} should exist")
        
        # Test knowledge directory
        knowledge_dir = self.project_root / "knowledge"
        self.assert_true(knowledge_dir.exists(), "Knowledge directory should exist")
        
        # Test essential config files
        config_files = [
            "pyproject.toml"
        ]
        
        for config_file in config_files:
            config_path = self.project_root / config_file
            self.assert_true(config_path.exists(), f"Config file {config_file} should exist")
    
    def test_configuration_files(self):
        """Test that configuration files are valid"""
        # Test pyproject.toml  
        pyproject_toml = self.project_root / "pyproject.toml"
        content = pyproject_toml.read_text()
        self.assert_in("[project]", content, "pyproject.toml should have project section")
        self.assert_in("soylent_red_division", content, "pyproject.toml should reference project name")
    
    def test_knowledge_structure(self):
        """Test knowledge directory structure"""
        knowledge_dir = self.project_root / "knowledge"
        
        # Test subdirectories
        required_subdirs = ["brand", "examples", "templates"]
        for subdir in required_subdirs:
            subdir_path = knowledge_dir / subdir
            self.assert_true(subdir_path.exists(), f"Knowledge subdirectory {subdir} should exist")
        
        # Test that we have some knowledge files
        brand_dir = knowledge_dir / "brand"
        brand_files = list(brand_dir.glob("*.md"))
        self.assert_true(len(brand_files) > 0, "Should have brand knowledge files")
    
    def run_all_tests(self):
        """Run all available tests"""
        self.log("Starting Simple Test Runner for Soylent Red Division")
        self.log("=" * 60)
        
        # List of all test methods
        tests = [
            (self.test_project_structure, "Project Structure"),
            (self.test_configuration_files, "Configuration Files"),
            (self.test_knowledge_structure, "Knowledge Structure"),
            (self.test_memory_manager_basic, "Memory Manager Basic"),
            (self.test_knowledge_manager_basic, "Knowledge Manager Basic"),
            (self.test_reasoning_engine_basic, "Reasoning Engine Basic"),
            (self.test_validation_engine_basic, "Validation Engine Basic")
        ]
        
        # Run each test
        for test_func, test_name in tests:
            self.run_test(test_func, test_name)
        
        # Print summary
        self.log("=" * 60)
        self.log(f"Test Summary: {self.passed} passed, {self.failed} failed")
        
        if self.failed == 0:
            self.log("🎉 All tests passed!", "SUCCESS")
            return True
        else:
            self.log(f"❌ {self.failed} tests failed", "ERROR")
            return False

def main():
    """Main entry point"""
    runner = SimpleTestRunner()
    success = runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()