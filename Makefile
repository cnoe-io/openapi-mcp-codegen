# Makefile

.PHONY: build setup-venv activate-venv install run add-copyright-license-headers lint ruff-fix generate generate-petstore generate-argocd generate-argo-rollouts generate-splunk build-agents-local build-agents-push build-agents-check uv-sync cz-changelog test release help

add-copyright-license-headers:
	@echo "Adding copyright license headers..."
	docker run --rm -v $(shell pwd)/openapi_mcp_codegen:/workspace ghcr.io/google/addlicense:latest -c "CNOE" -l apache -s=only -v /workspace

setup-venv: check-uv
	@echo "======================================="
	@echo " Setting up the Virtual Environment   "
	@echo "======================================="
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		echo "Virtual environment created."; \
	else \
		echo "Virtual environment already exists."; \
	fi

	@echo "======================================="
	@echo " Activating virtual environment       "
	@echo "======================================="
	@echo "To activate venv manually, run: source .venv/bin/activate"
	. .venv/bin/activate

check-uv:
	@echo "======================================="
	@echo " Checking if uv CLI is installed       "
	@echo "======================================="
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "uv CLI not found. Running uv-install..."; \
		$(MAKE) uv-install; \
	else \
		echo "uv CLI is already installed."; \
	fi

uv-install:
	@echo "======================================="
	@echo " Installing uv CLI                    "
	@echo "======================================="
	curl -LsSf https://astral.sh/uv/install.sh | sh

activate-venv:
	@echo "Activating virtual environment..."
	@if [ -d "venv" ]; then \
		. venv/bin/activate; \
	else \
		echo "Virtual environment not found. Please run 'make setup-venv' first."; \
	fi

lint: setup-venv
	@echo "Running ruff..."
	. .venv/bin/activate && uv run python -m ruff check openapi_mcp_codegen tests

ruff-fix: setup-venv
	@echo "Running ruff and fix lint errors..."
	. .venv/bin/activate && uv run python -m ruff check openapi_mcp_codegen tests --fix

generate: uv-sync
	@echo "Running the application with arguments: $(filter-out $@,$(MAKECMDGOALS))"
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen $(filter-out $@,$(MAKECMDGOALS))"

generate-petstore: uv-sync
	@echo "Generating code for Petstore example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen generate-mcp --spec-file examples/petstore/openapi-petstore.json --output-dir examples/petstore/generate_code --enhance-docstring-with-llm"

generate-petstore-agent: uv-sync
	@echo "Generating code for Petstore example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen generate-mcp --spec-file examples/openapi-petstore.json --output-dir examples/petstore/generate_code --enhance-docstring-with-llm --generate-agent"

generate-petstore-agent-eval-system-prompt: uv-sync
	@echo "Generating code for Petstore example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen generate-mcp --spec-file examples/openapi-petstore.json --output-dir examples/petstore/generate_code --enhance-docstring-with-llm --generate-agent --generate-eval --generate-system-prompt"

generate-argocd: setup-venv install
	@echo "Generating code for ArgoCD example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen generate-mcp --spec-file examples/argocd/openapi-argocd.json --output-dir examples/argocd/generate_code"

generate-argocd-agent: setup-venv install
	@echo "Generating code for ArgoCD example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen generate-mcp --spec-file examples/argocd/openapi-argocd.json --output-dir examples/argocd/generate_code --generate-agent"

generate-argocd-agent-eval-system-prompt: setup-venv install
	@echo "Generating code for ArgoCD example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen generate-mcp --spec-file examples/argocd/openapi-argocd.json --output-dir examples/argocd/generate_code --generate-agent --generate-eval --generate-system-prompt"


generate-argo-workflows: setup-venv install
	@echo "Generating code for Argo Workflows example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen --spec-file examples/argo-workflows/openapi-argo-workflows.json --output-dir examples/argo-workflows/generate_code"

generate-argo-workflows-agent: setup-venv install
	@echo "Generating code for Argo Workflows example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen --spec-file examples/argo-workflows/openapi-argo-workflows.json --output-dir examples/argo-workflows/generate_code --generate-agent"

generate-argo-workflows-eval-system-prompt: setup-venv install
	@echo "Generating code for Argo Workflows example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen --spec-file examples/argo-workflows/openapi-argo-workflows.json --output-dir examples/argo-workflows/generate_code --generate-agent --generate-eval --generate-system-prompt"

generate-argo-rollouts: setup-venv install
	@echo "Generating code for Argo Rollouts example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen generate-mcp --spec-file examples/argo-rollouts/openapi-argo-rollouts.json --output-dir examples/argo-rollouts/generate_code"

generate-argo-rollouts-agent: setup-venv install
	@echo "Generating code for Argo Rollouts example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen generate-mcp --spec-file examples/argo-rollouts/openapi-argo-rollouts.json --output-dir examples/argo-rollouts/generate_code --generate-agent"

generate-argo-rollouts-agent-eval-system-prompt: setup-venv install
	@echo "Generating code for Argo Rollouts example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen generate-mcp --spec-file examples/argo-rollouts/openapi-argo-rollouts.json --output-dir examples/argo-rollouts/generate_code --generate-agent --generate-eval --generate-system-prompt"

# Docker build targets for Argo agents
build-agents-check:
	@echo "Checking prerequisites for multi-arch Docker builds..."
	@command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
	@docker buildx version >/dev/null 2>&1 || { echo "❌ Docker buildx is required but not available."; exit 1; }
	@echo "✅ Prerequisites check passed"

build-agents-local: build-agents-check
	@echo "Building Argo agent containers locally (multi-arch)..."
	@echo "Services: argo-workflows -> agent-argo-workflows, argocd -> agent-argocd, argo-rollouts -> agent-argo-rollouts"
	@echo "Tags: ghcr.io/cnoe-io/{service}-{mcp|a2a}:autogen-{timestamp}"
	./build-agents.sh

build-agents-push: build-agents-check
	@echo "Building and pushing Argo agent containers to ghcr.io/cnoe-io..."
	@echo "⚠️  This will push to the cnoe-io organization registry"
	@echo "Services: argo-workflows -> agent-argo-workflows, argocd -> agent-argocd, argo-rollouts -> agent-argo-rollouts"
	./build-agents.sh --push

# Individual service build targets for testing
build-agent-argo-workflows: build-agents-check
	@echo "Building agent-argo-workflows containers locally..."
	@if [ ! -d "examples/argo-workflows/generate_code" ]; then \
		echo "❌ Generated code not found. Run 'make generate-argo-workflows-agent' first."; \
		exit 1; \
	fi
	./build-agents.sh argo-workflows

build-agent-argocd: build-agents-check
	@echo "Building agent-argocd containers locally..."
	@if [ ! -d "examples/argocd/generate_code" ]; then \
		echo "❌ Generated code not found. Run 'make generate-argocd-agent' first."; \
		exit 1; \
	fi
	./build-agents.sh argocd

build-agent-argo-rollouts: build-agents-check
	@echo "Building agent-argo-rollouts containers locally..."
	@if [ ! -d "examples/argo-rollouts/generate_code" ]; then \
		echo "❌ Generated code not found. Run 'make generate-argo-rollouts-agent' first."; \
		exit 1; \
	fi
	./build-agents.sh argo-rollouts

uv-sync: setup-venv
	@echo "Running uv sync..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv sync"

install: uv-sync
	@echo "Installing package in development mode..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv pip install -e ."

generate-backstage: uv-sync
	@echo "Generating code for Backstage example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen --spec-file examples/backstage/openapi.yaml --output-dir examples/backstage/generate_code --enhance-docstring-with-llm --generate-agent"

generate-splunk: uv-sync
	@echo "Generating code for Splunk example..."
	@echo "Loading environment variables..."
	@bash -c "set +a; [ -f .env ] && { echo 'Loading .env file...'; set -a; source .env; set +a; } || echo 'No .env file found, continuing...'; \
	source .venv/bin/activate && uv run python -m openapi_mcp_codegen --spec-file examples/splunk/openapi.json --output-dir examples/splunk/generate_code --enhance-docstring-with-llm --generate-agent"

# This rule allows passing arguments to the run target
%:
	@:

cz-changelog: setup-venv
	@echo "======================================="
	@echo " Checking and installing commitizen    "
	@echo "======================================="
	. .venv/bin/activate && pip show commitizen >/dev/null 2>&1 || . .venv/bin/activate && pip install -U commitizen
	@echo "======================================="
	@echo " Generating changelog with cz-changelog"
	@echo "======================================="
	. .venv/bin/activate && cz bump --changelog

test: setup-venv
	@echo "======================================="
	@echo " Running pytest on tests directory     "
	@echo "======================================="
	. .venv/bin/activate && uv run python -m pytest tests


## ========== Release & Versioning ==========
release: setup-venv  ## Bump version and create a release
	@. .venv/bin/activate; uv add commitizen --dev
	@. .venv/bin/activate; git tag -d stable || echo "No stable tag found."
	@. .venv/bin/activate; cz changelog
	@git add CHANGELOG.md
	@git commit -m "docs: update changelog"
	@. .venv/bin/activate; cz bump --increment PATCH
	@. .venv/bin/activate; git tag -f stable
	@echo "Version bumped and stable tag updated successfully."


help:
	@echo "Available targets:"
	@echo "  add-copyright-license-headers  Add copyright license headers to source files"
	@echo "  setup-venv                     Create virtual environment in .venv and install dependencies"
	@echo "  activate-venv                  Activate the virtual environment"
	@echo "  install                        Install the package"
	@echo "  lint                           Run ruff linter on codebase"
	@echo "  ruff-fix                       Run ruff and fix lint errors"
	@echo "  generate [ARGS]                Build, install, and run the application with optional arguments"
	@echo "  generate-petstore              Generate code for the Petstore example"
	@echo "  generate-argocd                Generate code for the ArgoCD example"
	@echo "  generate-argo-rollouts         Generate code for the Argo Rollouts example"
	@echo "  generate-splunk                Generate code for the Splunk example"
	@echo ""
	@echo "Docker build targets:"
	@echo "  build-agents-check             Check Docker prerequisites for multi-arch builds"
	@echo "  build-agents-local             Build all Argo agent containers locally (multi-arch)"
	@echo "  build-agents-push              Build and push all Argo agent containers to registry"
	@echo "  build-agent-argo-workflows     Build agent-argo-workflows containers locally"
	@echo "  build-agent-argocd             Build agent-argocd containers locally"
	@echo "  build-agent-argo-rollouts      Build agent-argo-rollouts containers locally"
	@echo ""
	@echo "  cz-changelog                   Generate changelog using commitizen"
	@echo "  test                           Run tests using pytest"
	@echo "  test-venv                      Set up test virtual environment and install test dependencies"
	@echo "  release                        Bump version and create a release"
	@echo "  help                           Show this help message"
