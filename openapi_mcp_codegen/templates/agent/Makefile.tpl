# Makefile for {{ mcp_name | capitalize }} agent
{% if a2a_proxy %}
.PHONY: run-with-proxy reset
{% else %}
.PHONY: run-a2a run-a2a-client run-a2a-eval-mode reset
{% endif %}

{% if a2a_proxy %}
# Starts the WebSocket JSON-RPC upstream server used by the external “a2a-proxy” (set {{ mcp_name | upper }}_API_URL + {{ mcp_name | upper }}_TOKEN)
run-with-proxy:  ## Install deps (via uv) and run the WebSocket proxy
	uv pip install -e . --upgrade
	uv run python -m protocol_bindings.ws_proxy --host 0.0.0.0 --port $${PORT:-8000}
{% else %}
# Starts the A2A HTTP server (expects {{ mcp_name | upper }}_API_URL + {{ mcp_name | upper }}_TOKEN in env)
run-a2a:  ## Install deps (via uv) and run the A2A server
	uv pip install -e . --upgrade
	uv run python -m protocol_bindings.a2a_server --host 0.0.0.0 --port $${PORT:-8000}
{% endif %}

{% if not a2a_proxy %}
# Opens an interactive chat CLI wired to the locally-running A2A server
run-a2a-client:
	docker run -it --network=host ghcr.io/cnoe-io/agent-chat-cli:stable
{% endif %}

{% if not a2a_proxy %}
# Starts the agent in evaluation mode (creates/updates eval/dataset.yaml)
run-a2a-eval-mode:
	uv pip install -e . --upgrade
	uv run python eval_mode.py
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
