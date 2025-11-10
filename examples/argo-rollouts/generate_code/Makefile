# Makefile for Argo_rollouts agent


.PHONY: run-a2a run-a2a-client run-mcp reset



# Ensure uv virtual environment exists before running any uv commands
.PHONY: ensure-uv-venv
ensure-uv-venv:
	@if ! uv venv --help >/dev/null 2>&1; then echo "uv not found. Please install uv: https://docs.astral.sh/uv/"; exit 1; fi
	@# Create venv if not already present
	@if [ ! -d ".venv" ]; then echo "Creating uv virtual environment (.venv)"; uv venv; fi


# Starts the A2A HTTP server (expects ARGO_ROLLOUTS_API_URL + ARGO_ROLLOUTS_TOKEN in env)
run-a2a: ensure-uv-venv  ## Install deps (via uv) and run the A2A server
	uv pip install -e . --upgrade
	uv run python -m protocol_bindings.a2a_server --host $${A2A_HOST:-0.0.0.0} --port $${A2A_PORT:-8000}

# Run the MCP server in HTTP mode (expects ARGO_ROLLOUTS_API_URL + ARGO_ROLLOUTS_TOKEN in env)
run-mcp: ensure-uv-venv  ## Run MCP server in HTTP mode
	@echo "Starting MCP server in HTTP mode on $${MCP_HOST:-localhost}:$${MCP_PORT:-3000}..."
	@echo "Make sure to set ARGO_ROLLOUTS_TOKEN and ARGO_ROLLOUTS_API_URL environment variables"
	MCP_MODE=http MCP_HOST=$${MCP_HOST:-localhost} MCP_PORT=$${MCP_PORT:-3000} uv run python -m mcp_argo_rollouts.server




# Opens an interactive chat CLI wired to the locally-running A2A server
run-a2a-client:
	docker run -it --network=host ghcr.io/cnoe-io/agent-chat-cli:stable






# Convenience: clean Python cache/dist artefacts
reset:
	find . -type d \( -name '__pycache__' -o -name '*.egg-info' \) -print0 | xargs -0 rm -rf

