# ASVS Compliance Starter Kit - Build System
# Standard targets for development and CI

.PHONY: all check lint test build-tools clean help validate-json validate-policies verify-security validate-terraform check-drift

# Default target
all: check test

# Help target
help:
	@echo "ASVS Compliance Starter Kit - Available targets:"
	@echo ""
	@echo "  make check            - Run all validation checks (JSON + Markdown)"
	@echo "  make lint             - Run Markdown linting only"
	@echo "  make test             - Run Python unit tests"
	@echo "  make build-tools      - Install Python development dependencies"
	@echo "  make validate-json    - Validate JSON file syntax"
	@echo "  make validate-policies - Run ASVS compliance gate validation"
	@echo "  make validate-terraform - Validate Terraform template formatting"
	@echo "  make verify-security  - Run verification suite against a target URL"
	@echo "  make check-drift      - Check for ASVS standard drift against upstream"
	@echo "  make clean            - Remove generated files and caches"
	@echo ""

# Combined check target: JSON validation + Markdown linting
check: validate-json lint
	@echo "All checks passed."

# JSON validation using jq
validate-json:
	@echo "Validating JSON files..."
	@find . -name "*.json" -not -path "./node_modules/*" -not -path "./.venv/*" | while read file; do \
		if ! jq empty "$$file" 2>/dev/null; then \
			echo "ERROR: Invalid JSON in $$file"; \
			exit 1; \
		fi; \
	done
	@echo "JSON validation passed."

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

# Run Python unit tests
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
	@.venv/bin/pip install -e .
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

# Run ASVS compliance gate validation (against test fixtures)
# Note: The repo's own templates are intentionally placeholders for users to customize
validate-policies:
	@echo "Running ASVS compliance gate validation..."
	@echo "Testing against good_repo fixture (valid filled-in templates)..."
	@if [ -d ".venv" ]; then \
		.venv/bin/python -m tools.compliance_gate \
			--docs-path tests/fixtures/good_repo/Decision-Templates \
			--level 2 \
			--config policies/data.json \
			--format text; \
	else \
		python3 -m tools.compliance_gate \
			--docs-path tests/fixtures/good_repo/Decision-Templates \
			--level 2 \
			--config policies/data.json \
			--format text; \
	fi
	@echo ""
	@echo "Note: Use 'make validate-policies DOCS_PATH=<your-path>' to validate your own templates."

# Validate Terraform template formatting
# Requires: terraform CLI (https://www.terraform.io/downloads)
validate-terraform:
	@echo "Validating Terraform template formatting..."
	@if command -v terraform >/dev/null 2>&1; then \
		terraform fmt -check -diff 02-Implementation-Guidance/Languages/Terraform/*.tf; \
		echo "Terraform format validation passed."; \
	else \
		echo "WARNING: terraform not found. Install from https://www.terraform.io/downloads"; \
		echo "Skipping Terraform validation."; \
	fi

# Run ASVS verification suite against a target URL
# Usage: make verify-security TARGET_URL=https://example.com
# Note: Requires 'requests' library. Install with: pip install requests
TARGET_URL ?= ""
verify-security:
	@if [ -z "$(TARGET_URL)" ]; then \
		echo "Usage: make verify-security TARGET_URL=https://example.com"; \
		echo ""; \
		echo "This runs the ASVS Verification Suite against a target web application."; \
		echo "It checks for security headers, cookie attributes, CSRF protection, and more."; \
		exit 1; \
	fi
	@echo "Running ASVS Verification Suite against $(TARGET_URL)..."
	@if [ -d ".venv" ]; then \
		.venv/bin/python -m tools.verification_suite \
			--target-url "$(TARGET_URL)" \
			--format text; \
	else \
		python3 -m tools.verification_suite \
			--target-url "$(TARGET_URL)" \
			--format text; \
	fi

# Check for ASVS standard drift against upstream
# Compares local ASVS reference files against the official OWASP ASVS
# Usage: make check-drift [UPSTREAM_URL=<url>]
UPSTREAM_URL ?= ""
check-drift:
	@echo "Checking for ASVS standard drift..."
	@if [ -d ".venv" ]; then \
		if [ -n "$(UPSTREAM_URL)" ]; then \
			.venv/bin/python -m tools.drift_detector --upstream-url "$(UPSTREAM_URL)"; \
		else \
			.venv/bin/python -m tools.drift_detector --offline; \
		fi; \
	else \
		if [ -n "$(UPSTREAM_URL)" ]; then \
			python3 -m tools.drift_detector --upstream-url "$(UPSTREAM_URL)"; \
		else \
			python3 -m tools.drift_detector --offline; \
		fi; \
	fi
