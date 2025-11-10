# {{ agent_display_name }} Agent Makefile
# --------------------------------------------------
# This Makefile provides targets for the {{ agent_display_name }} agent.
# --------------------------------------------------

# Agent configuration
AGENT_NAME = {{ agent_name }}
AGENT_PKG_NAME = agent_{{ agent_name }}
MCP_SERVER_URL = {{ mcp_server_url }}

# Virtual environment setup
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
UV = uv

.PHONY: help setup-venv setup-env check-env uv-sync clean run-a2a test

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup-venv: ## Create and setup virtual environment
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		$(UV) venv $(VENV_DIR); \
	fi

setup-env: ## Create .env file from template (if it doesn't exist)
	@if [ ! -f ".env" ]; then \
		echo "Creating .env file..."; \
		cp .env.example .env; \
		echo "✅ .env file created from .env.example"; \
		echo "📝 Please edit .env to configure your API keys and settings"; \
	else \
		echo "⚠️  .env file already exists, skipping creation"; \
	fi

check-env: ## Check if required environment variables are set
	@echo "Checking environment configuration..."
	@echo "MCP_SERVER_URL: $(MCP_SERVER_URL)"
	@echo "Agent Package: $(AGENT_PKG_NAME)"

uv-sync: setup-venv ## Sync dependencies with uv
	$(UV) sync

clean: ## Clean up generated files and virtual environment
	rm -rf $(VENV_DIR)
	rm -rf __pycache__
	rm -rf *.egg-info
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

run-a2a: setup-venv check-env uv-sync ## Run A2A agent with uvicorn
	$(UV) run python -m $(AGENT_PKG_NAME) --host 0.0.0.0 --port $${A2A_PORT:-8000}

test: setup-venv uv-sync ## Run tests
	$(UV) run pytest

format: setup-venv uv-sync ## Format code with ruff
	$(UV) run ruff format .

lint: setup-venv uv-sync ## Lint code with ruff
	$(UV) run ruff check .

install: setup-venv uv-sync ## Install the agent package
	$(UV) pip install -e .

# Development shortcuts
dev: setup-venv setup-env uv-sync format lint ## Setup development environment
	@echo "Development environment ready!"

run: run-a2a ## Alias for run-a2a
