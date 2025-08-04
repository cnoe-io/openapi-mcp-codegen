# Makefile

.PHONY: build setup-venv activate-venv install run add-copyright-license-headers lint ruff-fix generate generate-petstore generate-argocd generate-splunk uv-sync cz-changelog test release help

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
	@echo "Sourcing .env with set +a"
	@set +a; [ -f .env ] && . .env || true
	. .venv/bin/activate && uv run python -m openapi_mcp_codegen $(filter-out $@,$(MAKECMDGOALS))


generate-petstore: uv-sync
	@echo "Generating code for Petstore example..."
	@echo "Sourcing .env with set +a"
	@set +a; [ -f .env ] && . .env || true
	. .venv/bin/activate && uv run python -m openapi_mcp_codegen --spec-file examples/petstore/openapi_petstore.json --output-dir examples/petstore/mcp_server --enhance-docstring-with-llm

generate-argocd: setup-venv install
	@echo "Generating code for ArgoCD example..."
	@echo "Sourcing .env with set +a"
	@set +a; [ -f .env ] && . .env || true; . .venv/bin/activate && uv run python -m openapi_mcp_codegen --spec-file examples/argocd/openapi_argocd.json --output-dir examples/argocd/mcp_server --enhance-docstring-with-llm

uv-sync: setup-venv
	@echo "Running uv sync..."
	@echo "Sourcing .env with set +a"
	@set +a; [ -f .env ] && . .env || true; . .venv/bin/activate && uv sync

generate-splunk: uv-sync
	@echo "Generating code for Splunk example..."
	@echo "Sourcing .env with set +a"
	@set +a; [ -f .env ] && . .env || true; . .venv/bin/activate && uv run python -m openapi_mcp_codegen --spec-file examples/splunk/openapi.json --output-dir examples/splunk/mcp_server --enhance-docstring-with-llm --generate-agent

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
	@. .venv/bin/activate; poetry install
	@. .venv/bin/activate; poetry add commitizen --dev
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
	@echo "  generate-splunk                Generate code for the Splunk example"
	@echo "  cz-changelog                   Generate changelog using commitizen"
	@echo "  test                           Run tests using pytest"
	@echo "  test-venv                      Set up test virtual environment and install test dependencies"
	@echo "  release                        Bump version and create a release"
	@echo "  help                           Show this help message"
