# Makefile for {{ mcp_name | capitalize }} agent
{% if a2a_proxy %}
.PHONY: run-with-proxy reset
{% else %}
{% if enable_slim %}
.PHONY: run-a2a run-a2a-and-slim run-a2a-client reset
{% else %}
.PHONY: run-a2a run-a2a-client reset
{% endif %}
{% endif %}

{% if a2a_proxy %}
# Starts the WebSocket JSON-RPC upstream server used by the external “a2a-proxy” (set {{ mcp_name | upper }}_API_URL + {{ mcp_name | upper }}_TOKEN)
run-with-proxy:  ## Install deps (via uv) and run the WebSocket proxy
	uv pip install -e . --upgrade
	uv run python -m protocol_bindings.ws_proxy --host 127.0.0.1 --port $${PORT:-8000}
{% else %}
# Starts the A2A HTTP server (expects {{ mcp_name | upper }}_API_URL + {{ mcp_name | upper }}_TOKEN in env)
run-a2a:  ## Install deps (via uv) and run the A2A server
	uv pip install -e . --upgrade
	uv run python -m protocol_bindings.a2a_server --host 127.0.0.1 --port $${PORT:-8000}
{% if enable_slim %}
# Run HTTP A2A and SLIM bridge side-by-side via Docker Compose
.PHONY: run-a2a-and-slim
run-a2a-and-slim:
	@if [ ! -f docker-compose.yml ]; then echo "docker-compose.yml not found. Ensure this agent was generated with --enable-slim."; exit 1; fi
	docker build -t agent_{{ mcp_name }}:latest .
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
{% endif %}
{% endif %}

{% if not a2a_proxy %}
# Opens an interactive chat CLI wired to the locally-running A2A server
run-a2a-client:
	docker run -it --network=host ghcr.io/cnoe-io/agent-chat-cli:stable
{% endif %}

{% if not a2a_proxy %}
{% if generate_eval %}
# Starts the agent in evaluation mode (creates/updates eval/dataset.yaml)
run-a2a-eval-mode:
	uv pip install -e . --upgrade
	uv run python eval_mode.py
{% endif %}
{% endif %}

# Convenience: clean Python cache/dist artefacts
reset:
	find . -type d \( -name '__pycache__' -o -name '*.egg-info' \) -print0 | xargs -0 rm -rf

{% if generate_eval %}
.PHONY: eval
eval:
	uv pip install -e . --upgrade
	uv run python eval/evaluate_agent.py
{% endif %}
