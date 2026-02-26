# Kademos - Build System
# Standard targets for development and CI (parity with CircleCI)

.PHONY: all check lint test build-tools clean help validate-json check-drift

# Default target
all: check test

# Help target
help:
	@echo "Kademos - Available targets:"
	@echo ""
	@echo "  make check         - Run all validation checks (JSON + Markdown)"
	@echo "  make lint          - Run Markdown linting only"
	@echo "  make test          - Run Python unit tests"
	@echo "  make build-tools   - Install Python development dependencies"
	@echo "  make validate-json - Validate JSON file syntax"
	@echo "  make check-drift   - Check for ASVS standard drift against upstream"
	@echo "  make clean         - Remove generated files and caches"
	@echo ""

# Combined check target: JSON validation + Markdown linting
check: validate-json lint
	@echo "All checks passed."

# JSON validation using jq (skip if jq not installed)
validate-json:
	@echo "Validating JSON files..."
	@if command -v jq >/dev/null 2>&1; then \
		find . -name "*.json" -not -path "./node_modules/*" -not -path "./.venv/*" | while read file; do \
			if ! jq empty "$$file" 2>/dev/null; then \
				echo "ERROR: Invalid JSON in $$file"; \
				exit 1; \
			fi; \
		done; \
		echo "JSON validation passed."; \
	else \
		echo "WARNING: jq not found. Skipping JSON validation."; \
	fi

# Markdown linting (requires markdownlint-cli or npx)
lint:
	@echo "Linting Markdown files..."
	@if command -v markdownlint >/dev/null 2>&1; then \
		markdownlint '**/*.md' --ignore node_modules --ignore .venv || true; \
	elif command -v npx >/dev/null 2>&1; then \
		npx markdownlint-cli '**/*.md' --ignore node_modules --ignore .venv || true; \
	else \
		echo "WARNING: markdownlint not found. Install with: npm install -g markdownlint-cli"; \
	fi
	@echo "Markdown linting complete."

# Run Python unit tests (parity with CircleCI test-and-validate)
test:
	@echo "Running unit tests..."
	@if [ -d ".venv" ]; then \
		.venv/bin/python -m pytest tests/ -v --tb=short; \
	else \
		python3 -m pytest tests/ -v --tb=short; \
	fi

# Install Python development dependencies
build-tools:
	@echo "Installing development dependencies..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	@.venv/bin/pip install --upgrade pip
	@.venv/bin/pip install -r requirements-dev.txt
	@.venv/bin/pip install -e ".[cli]"
	@echo "Development environment ready. Activate with: source .venv/bin/activate"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -rf .venv
	@rm -rf __pycache__ */__pycache__ */*/__pycache__
	@rm -rf .pytest_cache tests/.pytest_cache
	@rm -rf *.egg-info
	@rm -rf .coverage htmlcov
	@rm -rf dist build
	@echo "Clean complete."

# Check for ASVS standard drift against upstream
# Usage: make check-drift [UPSTREAM_URL=<url>]
UPSTREAM_URL ?= ""
check-drift:
	@echo "Checking for ASVS standard drift..."
	@if [ -d ".venv" ]; then \
		PYTHON=".venv/bin/python"; \
	else \
		PYTHON="python3"; \
	fi; \
	if [ -n "$(UPSTREAM_URL)" ]; then \
		$$PYTHON -m tools resources --drift --upstream-url "$(UPSTREAM_URL)" || true; \
	else \
		$$PYTHON -m tools resources --drift --offline || true; \
	fi
