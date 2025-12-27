# @generated "all" Claude-Sonnet-4.5

.PHONY: test lint format check clean install install-dev help mypy

help:
	@echo "Available targets:"
	@echo "  make install      - Install package (non-editable)"
	@echo "  make install-dev  - Install package in editable mode with dev dependencies"
	@echo "  make format       - Format code with black"
	@echo "  make lint         - Run pylint on source and tests"
	@echo "  make mypy         - Run mypy type checking"
	@echo "  make test         - Run pytest"
	@echo "  make check        - Run all checks (format, lint, mypy, test)"
	@echo "  make clean        - Remove Python artifacts"

install:
	pip install .

install-dev:
	pip install -e .[dev]

format:
	@echo "Formatting code with black..."
	black src/ tests/

lint:
	@echo "Running pylint on source code..."
	pylint src/gittergraph/
	@echo "Running pylint on tests..."
	pylint tests/

mypy:
	@echo "Running mypy type checking..."
	mypy src/gittergraph/ tests/

test:
	@echo "Running tests with pytest..."
	pytest tests/ -v

check: format lint mypy test
	@echo "✓ All checks passed!"

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