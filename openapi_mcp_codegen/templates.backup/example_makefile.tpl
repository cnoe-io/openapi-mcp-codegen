# Makefile for {{ mcp_name | replace('_', ' ') | title }} MCP Server


.PHONY: run-mcp-server run-mcp-http run-a2a run-a2a-and-slim run-a2a-client run-a2a-eval-mode eval reset help




# Runs the MCP server in stdio mode (for testing with MCP clients)
run-mcp-server:  ## Install deps and run the MCP server in stdio mode
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && uv run python -m mcp_{{ mcp_name }}.server

# Runs the MCP server in HTTP/SSE mode (for MCP Inspector and other HTTP clients)
run-mcp-http:  ## Install deps and run the MCP server in HTTP mode
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && export $$(grep -v '^#' .env | xargs) && MCP_MODE=http MCP_HOST=0.0.0.0 MCP_PORT=$${MCP_PORT:-3000} uv run python -m mcp_{{ mcp_name }}.server

{% if generate_agent %}
# Starts the A2A HTTP server (expects {{ mcp_name | upper }}_API_URL + {{ mcp_name | upper }}_TOKEN in env)
run-a2a:  ## Install deps (via uv) and run the A2A server
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && uv run python -m protocol_bindings.a2a_server --host 127.0.0.1 --port $${PORT:-8000}

{% if enable_slim %}
# Run HTTP A2A and SLIM bridge side-by-side via Docker Compose
.PHONY: run-a2a-and-slim
run-a2a-and-slim:
	@if [ ! -f mcp_server/docker-compose.yml ]; then echo "docker-compose.yml not found. Ensure this agent was generated with --enable-slim."; exit 1; fi
	cd mcp_server && docker build -t agent_{{ mcp_name }}:latest .
	cd mcp_server && SLIM_ENDPOINT=$${SLIM_ENDPOINT:-http://localhost:46357} \
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




# Opens an interactive chat CLI wired to the locally-running A2A server
run-a2a-client:
	docker run -it --network=host ghcr.io/cnoe-io/agent-chat-cli:stable

{% if generate_eval %}


# Starts the agent in evaluation mode (creates/updates eval/dataset.yaml)
run-a2a-eval-mode:
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && uv run python eval_mode.py



# Run the evaluation suite
.PHONY: eval
eval:
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && uv run python eval/evaluate_agent.py
{% endif %}
{% endif %}

# Generate enhanced MCP server with overlay
.PHONY: generate-enhanced
generate-enhanced:  ## Generate MCP server with LLM-enhanced overlay
	python -m openapi_mcp_codegen.enhance_and_generate \
		openapi_{{ mcp_name }}.json \
		mcp_server \
		config.yaml \
		--save-overlay overlay.yaml \
		--save-enhanced-spec enhanced_openapi.json

# Generate overlay only
.PHONY: generate-overlay
generate-overlay:  ## Generate OpenAPI overlay with LLM enhancements
	python -m openapi_mcp_codegen.overlay_generator \
		openapi_{{ mcp_name }}.json \
		overlay.yaml

# Apply existing overlay
.PHONY: apply-overlay
apply-overlay:  ## Apply overlay to OpenAPI spec
	python -m openapi_mcp_codegen.overlay_applier \
		openapi_{{ mcp_name }}.json \
		overlay.yaml \
		enhanced_openapi.json

# Generate MCP server from enhanced spec
.PHONY: generate-mcp
generate-mcp:  ## Generate MCP server from enhanced OpenAPI spec
	python -m openapi_mcp_codegen \
		--spec-file enhanced_openapi.json \
		--output-dir mcp_server{% if generate_agent %} \
		--generate-agent{% endif %}{% if generate_eval %} \
		--generate-eval{% endif %}

# Convenience: clean Python cache/dist artefacts
reset:
	find . -type d \( -name '__pycache__' -o -name '*.egg-info' -o -name '.pytest_cache' \) -print0 | xargs -0 rm -rf
	cd mcp_server 2>/dev/null && find . -type d \( -name '__pycache__' -o -name '*.egg-info' \) -print0 | xargs -0 rm -rf || true

# Clean generated files
.PHONY: clean
clean:  ## Remove generated files and artifacts
	rm -rf mcp_server
	rm -f enhanced_openapi.json
	rm -f overlay.yaml

# Help target
.PHONY: help
help:  ## Show this help message
	@echo "{{ mcp_name | replace('_', ' ') | title }} MCP Server - Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Environment variables:"
	@echo "  {{ mcp_name | upper }}_API_URL        API URL (required)"
	@echo "  {{ mcp_name | upper }}_TOKEN          Authentication token (required)"
	@echo "  MCP_PORT                      MCP HTTP server port (default: 3000)"
{% if generate_agent %}
	@echo "  PORT                          A2A server port (default: 8000)"
{% if enable_slim %}
	@echo "  SLIM_PORT                     SLIM A2A server port (default: 8001)"
{% endif %}
{% endif %}
	@echo ""
	@echo "  OPENAI_API_KEY                OpenAI API key for LLM overlay generation"
	@echo "  ANTHROPIC_API_KEY             Anthropic API key for LLM overlay generation"
	@echo "  LLM_PROVIDER                  LLM provider (openai or anthropic)"

