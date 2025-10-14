# Makefile for Argo_workflows agent


.PHONY: run-a2a run-a2a-client reset



# Ensure uv virtual environment exists before running any uv commands
.PHONY: ensure-uv-venv
ensure-uv-venv:
	@if ! uv venv --help >/dev/null 2>&1; then echo "uv not found. Please install uv: https://docs.astral.sh/uv/"; exit 1; fi
	@# Create venv if not already present
	@if [ ! -d ".venv" ]; then echo "Creating uv virtual environment (.venv)"; uv venv; fi


# Starts the A2A HTTP server (expects ARGO_WORKFLOWS_API_URL + ARGO_WORKFLOWS_TOKEN in env)
run-a2a: ensure-uv-venv  ## Install deps (via uv) and run the A2A server
	uv pip install -e . --upgrade
	uv run python -m protocol_bindings.a2a_server --host 0.0.0.0 --port $${PORT:-8000}




# Opens an interactive chat CLI wired to the locally-running A2A server
run-a2a-client:
	docker run -it --network=host ghcr.io/cnoe-io/agent-chat-cli:stable






# Convenience: clean Python cache/dist artefacts
reset:
	find . -type d \( -name '__pycache__' -o -name '*.egg-info' \) -print0 | xargs -0 rm -rf

