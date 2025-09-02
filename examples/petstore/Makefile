# Makefile for Petstore agent


.PHONY: run-a2a run-a2a-and-slim run-a2a-client reset




# Starts the A2A HTTP server (expects PETSTORE_API_URL + PETSTORE_TOKEN in env)
run-a2a:  ## Install deps (via uv) and run the A2A server
	uv pip install -e . --upgrade
	uv run python -m protocol_bindings.a2a_server --host 127.0.0.1 --port $${PORT:-8000}

# Run HTTP A2A and SLIM bridge side-by-side via Docker Compose
.PHONY: run-a2a-and-slim
run-a2a-and-slim:
	@if [ ! -f docker-compose.yml ]; then echo "docker-compose.yml not found. Ensure this agent was generated with --enable-slim."; exit 1; fi
	docker build -t agent_petstore:latest .
	SLIM_ENDPOINT=$${SLIM_ENDPOINT:-http://localhost:46357} \
	A2A_PORT=$${PORT:-8000} \
	SLIM_A2A_PORT=$${SLIM_PORT:-8001} \
	docker compose up

.PHONY: run-slim-client
run-slim-client:
	docker run -it --network=host \
		-e AGENT_CHAT_PROTOCOL=slim \
		-e SLIM_ENDPOINT=$${SLIM_ENDPOINT:-http://0.0.0.0:46357} \
		-e SLIM_REMOTE_CARD=$${SLIM_REMOTE_CARD:-http://0.0.0.0:8000/.well-known/agent.json} \
		ghcr.io/cnoe-io/agent-chat-cli:stable




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
