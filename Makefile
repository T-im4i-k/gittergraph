# @generated "all" Claude-Sonnet-4.5

.PHONY: test lint lint-src lint-all mypy mypy-src mypy-all format format-src format-all check check-src check-all clean install install-dev help

help:
	@echo "Available targets:"
	@echo ""
	@echo "Installation:"
	@echo "  make install      - Install package (non-editable)"
	@echo "  make install-dev  - Install package in editable mode with dev dependencies"
	@echo ""
	@echo "Formatting:"
	@echo "  make format       - Format source code with isort and black"
	@echo "  make format-all   - Format source code and tests"
	@echo ""
	@echo "Linting:"
	@echo "  make lint         - Run pylint on source code (default)"
	@echo "  make lint-all     - Run pylint on source code and tests"
	@echo ""
	@echo "Type checking:"
	@echo "  make mypy         - Run mypy on source code (default)"
	@echo "  make mypy-all     - Run mypy on source code and tests"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run pytest"
	@echo ""
	@echo "Combined checks:"
	@echo "  make check        - Run all checks on source code (format, lint, mypy, test)"
	@echo "  make check-all    - Run all checks on source and tests (comprehensive)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove Python artifacts"

install:
	pip install .

install-dev:
	pip install -e .[dev]


# Formatting targets
format-src:
	@echo "Sorting imports in source code with isort..."
	isort src/
	@echo "Formatting source code with black..."
	black src/

format-all:
	@echo "Sorting imports with isort..."
	isort src/ tests/
	@echo "Formatting code with black..."
	black src/ tests/

format: format-src


# Linting targets
lint-src:
	@echo "Running pylint on source code..."
	pylint src/gittergraph/

lint-all:
	@echo "Running pylint on source code..."
	pylint src/gittergraph/
	@echo "Running pylint on tests..."

	# disable warnings about redefined-outer-name and protected-access in tests
	pylint tests/ --disable=W0621,W0212

lint: lint-src


# Type checking targets
mypy-src:
	@echo "Running mypy type checking on source code..."
	mypy src/gittergraph/

mypy-all:
	@echo "Running mypy type checking on source and tests..."
	mypy src/gittergraph/ tests/

mypy: mypy-src


# Testing target
test:
	@echo "Running tests with pytest..."
	pytest tests/


# Combined check targets
check-src: format-src lint-src mypy-src test
	@echo "✓ All source checks passed!"

check-all: format-all lint-all mypy-all test
	@echo "✓ All checks passed!"

check: check-src

clean:
	@echo "Cleaning Python artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✓ Cleanup complete!"