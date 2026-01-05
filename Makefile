.PHONY: help install install-dev sync lock update clean clean-all \
        lint lint-fix format format-check type security check \
        test test-fast test-cov test-unit test-integration \
        tox tox-py38 tox-py39 tox-py310 tox-py311 tox-py312 tox-py313 \
        docs docs-serve docs-clean \
        build publish publish-test version \
        pre-commit ci

# Colors for terminal output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Default target
.DEFAULT_GOAL := help

# Project settings
PACKAGE_NAME := sonarqube
SRC_DIR := src
TEST_DIR := tests
DOCS_DIR := docs

##@ General

help: ## Show this help message
	@echo "$(BLUE)SonarQube SDK - Development Commands$(RESET)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make $(GREEN)<target>$(RESET)\n\n"} \
		/^[a-zA-Z_0-9-]+:.*?##/ { printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2 } \
		/^##@/ { printf "\n$(YELLOW)%s$(RESET)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation & Dependencies

install: ## Install package in production mode
	uv sync --no-dev

install-dev: ## Install package with all development dependencies
	uv sync --all-extras

sync: ## Sync dependencies from lock file
	uv sync

lock: ## Generate/update lock file
	uv lock

update: ## Update all dependencies to latest versions
	uv lock --upgrade
	uv sync

##@ Code Quality

lint: ## Run Ruff linter
	uv run ruff check $(SRC_DIR) $(TEST_DIR)

lint-fix: ## Run Ruff linter with auto-fix
	uv run ruff check --fix $(SRC_DIR) $(TEST_DIR)

format: ## Format code with Ruff
	uv run ruff format $(SRC_DIR) $(TEST_DIR)

format-check: ## Check code formatting without changes
	uv run ruff format --check $(SRC_DIR) $(TEST_DIR)

type: ## Run MyPy type checker
	uv run mypy $(SRC_DIR)

security: ## Run Bandit security checker
	uv run bandit -r $(SRC_DIR) -c pyproject.toml

security-report: ## Run Bandit and generate JSON report
	uv run bandit -r $(SRC_DIR) -c pyproject.toml -f json -o bandit-report.json

check: lint type security ## Run all code quality checks (lint, type, security)
	@echo "$(GREEN)All checks passed!$(RESET)"

##@ Testing

test: ## Run tests with pytest
	uv run pytest $(TEST_DIR) -v

test-fast: ## Run tests without coverage (faster)
	uv run pytest $(TEST_DIR) -v --no-cov

test-cov: ## Run tests with coverage report
	uv run pytest $(TEST_DIR) --cov=$(SRC_DIR)/$(PACKAGE_NAME) --cov-report=term-missing --cov-report=html --cov-report=xml

test-unit: ## Run only unit tests
	uv run pytest $(TEST_DIR) -v -m "not integration"

test-integration: ## Run only integration tests
	uv run pytest $(TEST_DIR) -v -m "integration"

test-failed: ## Re-run only failed tests
	uv run pytest $(TEST_DIR) --lf -v

test-debug: ## Run tests with debug output
	uv run pytest $(TEST_DIR) -v -s --tb=long

##@ Tox - Multi-version Testing

tox: ## Run tox for all Python versions
	uv run tox

tox-parallel: ## Run tox in parallel mode
	uv run tox -p auto

tox-py38: ## Run tox for Python 3.8
	uv run tox -e py38

tox-py39: ## Run tox for Python 3.9
	uv run tox -e py39

tox-py310: ## Run tox for Python 3.10
	uv run tox -e py310

tox-py311: ## Run tox for Python 3.11
	uv run tox -e py311

tox-py312: ## Run tox for Python 3.12
	uv run tox -e py312

tox-py313: ## Run tox for Python 3.13
	uv run tox -e py313

tox-lint: ## Run tox lint environment
	uv run tox -e lint

tox-type: ## Run tox type checking environment
	uv run tox -e type

tox-security: ## Run tox security environment
	uv run tox -e security

##@ Documentation

docs: ## Build documentation with Sphinx
	uv run sphinx-build -b html $(DOCS_DIR) $(DOCS_DIR)/_build/html

docs-serve: docs ## Build and serve documentation locally
	@echo "$(BLUE)Serving docs at http://localhost:8000$(RESET)"
	cd $(DOCS_DIR)/_build/html && uv run python -m http.server 8000

docs-clean: ## Clean documentation build
	rm -rf $(DOCS_DIR)/_build

docs-check: ## Check documentation for warnings/errors
	uv run sphinx-build -b html $(DOCS_DIR) $(DOCS_DIR)/_build/html -W --keep-going

##@ Build & Publish

build: clean ## Build source and wheel distributions
	uv build
	@echo "$(GREEN)Build complete! Check dist/ directory$(RESET)"

publish-test: build ## Publish package to TestPyPI
	uv publish --publish-url https://test.pypi.org/legacy/
	@echo "$(GREEN)Published to TestPyPI!$(RESET)"

publish: build ## Publish package to PyPI
	uv publish
	@echo "$(GREEN)Published to PyPI!$(RESET)"

version: ## Show current package version
	@uv run python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"

##@ Cleanup

clean: ## Remove build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf $(SRC_DIR)/*.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-all: clean docs-clean ## Remove all generated files (build, docs, cache)
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf .tox/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf coverage.xml
	rm -rf bandit-report.json
	@echo "$(GREEN)All generated files removed!$(RESET)"

##@ Development Workflow

pre-commit: format lint type security test ## Run all checks before committing
	@echo "$(GREEN)All pre-commit checks passed!$(RESET)"

ci: ## Run full CI pipeline (format-check, lint, type, security, test-cov)
	@echo "$(BLUE)Running CI pipeline...$(RESET)"
	$(MAKE) format-check
	$(MAKE) lint
	$(MAKE) type
	$(MAKE) security
	$(MAKE) test-cov
	@echo "$(GREEN)CI pipeline completed successfully!$(RESET)"

ci-full: ci tox ## Run full CI pipeline including all Python versions
	@echo "$(GREEN)Full CI pipeline completed!$(RESET)"

dev: install-dev ## Setup development environment
	@echo "$(GREEN)Development environment ready!$(RESET)"
	@echo "Run 'make help' to see available commands"

##@ Utilities

repl: ## Start Python REPL with package loaded
	uv run python -c "from sonarqube import SonarQubeClient; print('SonarQubeClient imported successfully')" && uv run python

shell: ## Start IPython shell (if installed)
	uv run ipython

tree: ## Show project structure
	@tree -I '__pycache__|*.egg-info|.git|.tox|.mypy_cache|.ruff_cache|.pytest_cache|htmlcov|dist|build|_build' -a

todo: ## Find TODO comments in codebase
	@grep -rn "TODO\|FIXME\|XXX\|HACK" $(SRC_DIR) $(TEST_DIR) --include="*.py" || echo "No TODOs found!"

lines: ## Count lines of code
	@find $(SRC_DIR) -name "*.py" | xargs wc -l | tail -1
	@echo "Test files:"
	@find $(TEST_DIR) -name "*.py" | xargs wc -l | tail -1

