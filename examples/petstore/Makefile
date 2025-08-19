# Makefile for Petstore agent

.PHONY: run-a2a run-a2a-client reset



# Starts the A2A HTTP server (expects PETSTORE_API_URL + PETSTORE_TOKEN in env)
run-a2a:  ## Install deps (via uv) and run the A2A server
	uv pip install -e . --upgrade
	uv run python -m protocol_bindings.a2a_server --host 127.0.0.1 --port $${PORT:-8000}



# Opens an interactive chat CLI wired to the locally-running A2A server
run-a2a-client:
	docker run -it --network=host ghcr.io/cnoe-io/agent-chat-cli:stable




# Starts the agent in evaluation mode (creates/updates eval/dataset.yaml)
run-a2a-eval-mode:
	uv pip install -e . --upgrade
	uv run python eval_mode.py



# Convenience: clean Python cache/dist artefacts
reset:
	find . -type d \( -name '__pycache__' -o -name '*.egg-info' \) -print0 | xargs -0 rm -rf


.PHONY: eval
eval:
	uv pip install -e . --upgrade
	uv run python eval/evaluate_agent.py
