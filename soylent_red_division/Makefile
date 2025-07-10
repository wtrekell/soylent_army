# Makefile for Soylent Red Division

.PHONY: help install test test-unit test-integration test-e2e test-all clean lint format type-check security coverage

# Default target
help:
	@echo "Soylent Red Division - Make Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install          Install development dependencies"
	@echo "  install-test     Install testing dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run core functionality tests (no dependencies)"
	@echo "  test-core        Run core functionality tests (alias for test)"
	@echo "  test-pytest      Run comprehensive pytest suite (requires setup)"
	@echo "  test-unit        Run unit tests only (requires pytest)"
	@echo "  test-integration Run integration tests only (requires pytest)"
	@echo "  test-e2e         Run end-to-end tests only (requires pytest)"
	@echo "  test-fast        Run tests without slow markers (requires pytest)"
	@echo "  test-memory      Run memory system tests (requires pytest)"
	@echo "  test-knowledge   Run knowledge system tests (requires pytest)"
	@echo "  test-reasoning   Run reasoning system tests (requires pytest)"
	@echo "  test-validation  Run validation system tests (requires pytest)"
	@echo "  test-crew        Run crew and tools tests (requires pytest)"
	@echo "  coverage         Run tests with coverage report (requires pytest)"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint             Run linting checks"
	@echo "  format           Format code with black and isort"
	@echo "  type-check       Run type checking with mypy"
	@echo "  security         Run security scans"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean            Clean up generated files"
	@echo "  clean-cache      Clean pytest cache"

# Setup targets
install:
	pip install -e .

install-test:
	pip install -r tests/requirements.txt

# Testing targets
test:
	python3 tests/test_core_functionality.py

test-core:
	python3 tests/test_core_functionality.py

# Comprehensive testing (requires dependency resolution)
test-pytest:
	pytest tests/ -v

test-unit:
	pytest tests/test_memory_manager.py tests/test_knowledge_manager.py tests/test_reasoning_engine.py tests/test_validation_engine.py -v -m "unit"

test-integration:
	pytest tests/test_integration.py -v -m "integration"

test-e2e:
	pytest tests/test_end_to_end.py -v -m "e2e"

test-fast:
	pytest tests/ -v -m "not slow"

test-memory:
	pytest tests/test_memory_manager.py -v -m "memory"

test-knowledge:
	pytest tests/test_knowledge_manager.py -v -m "knowledge"

test-reasoning:
	pytest tests/test_reasoning_engine.py -v -m "reasoning"

test-validation:
	pytest tests/test_validation_engine.py -v -m "validation"

test-crew:
	pytest tests/test_crew_and_tools.py -v -m "crew or tools"

test-all:
	pytest tests/ -v --tb=short

coverage:
	pytest --cov=src/soylent_red_division --cov-report=html --cov-report=term-missing --cov-fail-under=70

# Code quality targets
lint:
	flake8 src tests
	black --check src tests
	isort --check-only src tests

format:
	black src tests
	isort src tests

type-check:
	mypy src --ignore-missing-imports --no-strict-optional

security:
	bandit -r src -f json -o bandit-report.json
	safety check

# Maintenance targets
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	rm -rf bandit-report.json
	rm -rf safety-report.json
	rm -rf test_artifacts/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-cache:
	rm -rf .pytest_cache/

# Development workflow
dev-setup: install install-test
	@echo "Development environment setup complete"

ci-test: test-unit test-integration test-crew test-e2e coverage
	@echo "All CI tests completed"

pre-commit: format lint type-check test-fast
	@echo "Pre-commit checks completed"

# System-specific tests
test-systems:
	@echo "Running system-specific test suites..."
	pytest tests/test_memory_manager.py -v --tb=short
	pytest tests/test_knowledge_manager.py -v --tb=short  
	pytest tests/test_reasoning_engine.py -v --tb=short
	pytest tests/test_validation_engine.py -v --tb=short
	@echo "System tests completed"

# Performance testing
test-performance:
	pytest tests/ -k "performance" --benchmark-only

# Debugging helpers
test-debug:
	pytest tests/ -v -s --tb=long --showlocals

test-pdb:
	pytest tests/ -v -s --pdb

# Documentation testing
test-docs:
	pytest tests/ --doctest-modules src/