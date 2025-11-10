# Common Makefile for CNOE Agent Projects
# --------------------------------------------------
# This file provides common targets for building, testing, and running CNOE agents.
# Include this file in your agent's Makefile to get all common functionality.
#
# Required variables to be set in your agent's Makefile:
#   AGENT_NAME - The name of your agent (e.g., slack, github, komodor)
#
# Optional variables:
#   AGENT_DIR_NAME - Defaults to agent-$(AGENT_NAME)
#   AGENT_PKG_NAME - Defaults to agent_$(AGENT_NAME)
#   MCP_SERVER_DIR - Defaults to mcp_$(AGENT_NAME)
# --------------------------------------------------

# Ensure AGENT_NAME is set
ifndef AGENT_NAME
$(error AGENT_NAME must be set before including common.mk)
endif

# Default derived variables
AGENT_DIR_NAME ?= agent-$(AGENT_NAME)
MCP_AGENT_DIR_NAME ?= mcp-$(AGENT_NAME)
AGENT_PKG_NAME ?= agent_$(AGENT_NAME)
MCP_SERVER_DIR ?= mcp_$(AGENT_NAME)

# Repository root for Docker build context (agents are at ai_platform_engineering/agents/{agent}/)
REPO_ROOT ?= $(shell git rev-parse --show-toplevel 2>/dev/null || echo "../../..")

# Helper variables for virtual environment management
venv-activate = . .venv/bin/activate
load-env = set -a && . .env && set +a
venv-run = $(venv-activate) && $(load-env) &&

## -------------------------------------------------
.DEFAULT_GOAL = run

# Common PHONY targets
.PHONY: \
	build setup-venv clean-pyc clean-venv clean-build-artifacts clean \
	check-env copy-env-from-root \
	uv-sync uv-install \
	lint ruff ruff-fix \
	run run-a2a run-mcp \
	run-a2a-client run-mcp-client \
	langgraph-dev evals test \
	build-docker-a2a build-docker-a2a-tag build-docker-a2a-push build-docker-a2a-tag-and-push \
	run-docker-a2a \
	registry-agntcy-directory \
	add-copyright-license-headers help

## ========== Setup & Clean ==========


clean-pyc:         ## Remove Python bytecode and __pycache__
	@find . -type d -name "__pycache__" -exec rm -rf {} + || echo "No __pycache__ directories found."

clean-venv:        ## Remove the virtual environment
	@rm -rf .venv && echo "Virtual environment removed." || echo "No virtual environment found."

clean-build-artifacts: ## Remove dist/, build/, egg-info/
	@rm -rf dist $(AGENT_PKG_NAME).egg-info || echo "No build artifacts found."

clean:             ## Clean all build artifacts and cache
	@$(MAKE) clean-pyc
	@$(MAKE) clean-venv
	@$(MAKE) clean-build-artifacts
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + || echo "No .pytest_cache directories found."

## ========== Environment Helpers ==========

check-env:         ## Check if .env file exists
	@if [ ! -f ".env" ]; then \
		echo "Warning: .env file not found in $$(pwd)"; \
		$(MAKE) copy-env-from-root; \
	fi

copy-env-from-root: ## Copy .env file from root directory
	@echo "Root directory: $(shell git rev-parse --show-toplevel)"
	@if [ -f "../../../.env" ]; then \
		cp ../../../.env . && echo ".env file copied from root directory."; \
	else \
		echo "Error: .env file not found in root directory."; exit 1; \
	fi
	@echo ""
	@echo "Environment variables for MCP server connection:"
	@echo "  MCP_HOST (default: localhost)"
	@echo "  MCP_PORT (default: 3001)"

## ========== UV Management ==========

# Use local venv setup
setup-venv:        ## Use local venv (already setup)
	@echo "Using local virtual environment..."
	@if [ ! -d ".venv" ]; then \
		echo "Error: Local .venv not found. Please run 'uv sync' in this directory."; \
		exit 1; \
	fi

uv-sync: ## Use local dependencies (already synced)
	@echo "Dependencies should be synced in local directory..."
	@if [ ! -d ".venv" ]; then \
		echo "Please run 'uv sync' in this directory first."; \
		exit 1; \
	fi

uv-install:        ## Install uv package manager
	@if ! command -v uv &> /dev/null; then \
		read -p "uv is not installed. Do you want to install it? (y/n): " confirm; \
		if [ "$$confirm" = "y" ]; then \
			curl -LsSf https://astral.sh/uv/install.sh | sh; \
		else \
			echo "uv installation skipped."; \
			exit 1; \
		fi; \
	else \
		echo "uv is already installed."; \
	fi

## ========== Build & Lint ==========

build: setup-venv  ## Build the package
	@echo "Build target for uv-based projects - no specific build step required"

lint: setup-venv     ## Lint code with ruff
	@source .venv/bin/activate && python -m ruff check $(AGENT_PKG_NAME) tests --select E,F --ignore F403 --ignore E402 --line-length 320

ruff: lint				   ## Run ruff linter (alias for lint)

ruff-fix: setup-venv ## Auto-fix lint issues with ruff
	@source .venv/bin/activate && python -m ruff check $(AGENT_PKG_NAME) tests --fix

## ========== Run ==========

run: run-a2a ## Run the agent application (default to A2A)

run-a2a: setup-venv check-env ## Run A2A agent
	@echo "Starting $(AGENT_NAME) agent on port $${A2A_PORT:-11000}..."
	@source .venv/bin/activate && \
	python -m $(AGENT_PKG_NAME) --host 0.0.0.0 --port $${A2A_PORT:-11000}

run-mcp: setup-venv check-env ## Run MCP server in HTTP mode
	@MCP_MODE=HTTP source .venv/bin/activate && python ../mcp_server/mcp_argo_workflows/server.py

## ========== Clients ==========

run-a2a-client: setup-venv ## Run A2A client script
	@$(MAKE) check-env
	@source .venv/bin/activate && agent-chat-cli --agent-url http://localhost:$${A2A_PORT:-11000}

run-mcp-client: setup-venv ## Run MCP client script
	@$(MAKE) check-env
	@echo "Use: uvx https://github.com/cnoe-io/agent-chat-cli.git mcp"

langgraph-dev: setup-venv ## Run LangGraph dev mode
	@source .venv/bin/activate && langgraph dev

evals: setup-venv ## Run agentevals with test cases
	@source .venv/bin/activate && python evals/strict_match/test_strict_match.py

## ========== Tests ==========

test: setup-venv build ## Run tests using pytest and coverage
	@source .venv/bin/activate && pytest -v --tb=short --disable-warnings --maxfail=1 --ignore=evals

## ========== Licensing & Help ==========

add-copyright-license-headers: ## Add license headers
	docker run --rm -v $(shell pwd)/$(AGENT_PKG_NAME):/workspace ghcr.io/google/addlicense:latest -c "CNOE" -l apache -s=only -v /workspace

help: ## Show this help message
	@echo "Available targets for $(AGENT_NAME) agent:"
	@echo "Variables:"
	@echo "  AGENT_NAME=$(AGENT_NAME)"
	@echo "  AGENT_DIR_NAME=$(AGENT_DIR_NAME)"
	@echo "  AGENT_PKG_NAME=$(AGENT_PKG_NAME)"
	@echo ""
	@echo "Targets:"
	@grep -h -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}' | sort
