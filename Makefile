# @generated "all" Claude-Sonnet-4.5

.PHONY: help install install-dev
.PHONY: format format-src format-all
.PHONY: check-format check-format-src check-format-all
.PHONY: lint lint-src lint-all
.PHONY: mypy mypy-src mypy-all
.PHONY: test test-cov
.PHONY: check check-src check-all
.PHONY: clean

help:
	@echo "Available targets:"
	@echo ""
	@echo "Installation:"
	@echo "  make install            - Install package (non-editable)"
	@echo "  make install-dev        - Install package in editable mode with dev dependencies"
	@echo ""
	@echo "Formatting:"
	@echo "  make format             - Format source code with isort and black"
	@echo "  make format-all         - Format source code and tests"
	@echo ""
	@echo "Formatting checking:"
	@echo "  make check-format       - Check source code formatting with isort and black"
	@echo "  make check-format-all   - Check source code and tests formatting"
	@echo ""
	@echo "Linting:"
	@echo "  make lint               - Run pylint on source code"
	@echo "  make lint-all           - Run pylint on source code and tests"
	@echo ""
	@echo "Type checking:"
	@echo "  make mypy               - Run mypy on source code"
	@echo "  make mypy-all           - Run mypy on source code and tests"
	@echo ""
	@echo "Testing:"
	@echo "  make test               - Run pytest"
	@echo "  make test-cov           - Run pytest with coverage report"
	@echo ""
	@echo "Combined checks:"
	@echo "  make check              - Run all checks on source code (format, lint, mypy, test)"
	@echo "  make check-all          - Run all checks on source and tests"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean              - Remove Python artifacts"

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


# Formatting check targets
check-format-src:
	@echo "Checking import order in source code with isort..."
	@isort --check-only --diff src/
	@echo "Checking source code formatting with black..."
	@black --check --diff src/

check-format-all:
	@echo "Checking import order with isort..."
	@isort --check-only --diff src/ tests/
	@echo "Checking code formatting with black..."
	@black --check --diff src/ tests/

check-format: check-format-src


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


# Testing targets
test:
	@echo "Running tests with pytest..."
	pytest tests/

test-cov:
	@echo "Running tests with coverage report..."
	pytest tests/ --cov=src/gittergraph


# Combined check targets
check-src: check-format-src lint-src mypy-src test
	@echo "✓ All source checks passed!"

check-all: check-format-all lint-all mypy-all test
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