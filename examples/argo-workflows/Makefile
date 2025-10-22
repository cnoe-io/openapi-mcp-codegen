# Makefile for Argo Workflows MCP Server


.PHONY: run-mcp-server run-mcp-http run-a2a run-a2a-client run-a2a-eval-mode \
        validate validate-original \
        generate-agw-config run-agentgateway stop-agentgateway agw-validate \
        generate-enhanced generate-overlay apply-overlay generate-mcp \
        reset clean help




# Runs the MCP server in stdio mode (for testing with MCP clients)
run-mcp-server:  ## Install deps and run the MCP server in stdio mode
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && uv run python -m mcp_argo_workflows.server

# Runs the MCP server in HTTP/SSE mode (for MCP Inspector and other HTTP clients)
run-mcp-http:  ## Install deps and run the MCP server in HTTP mode
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && export $$(grep -v '^#' .env | xargs) && MCP_MODE=http MCP_HOST=0.0.0.0 MCP_PORT=$${MCP_PORT:-3000} uv run python -m mcp_argo_workflows.server

# Starts the A2A HTTP server (expects ARGO_WORKFLOWS_API_URL + ARGO_WORKFLOWS_TOKEN in env)
run-a2a:  ## Install deps (via uv) and run the A2A server
	cd mcp_server && uv pip install -e . --upgrade
	export $$(grep -v '^#' .env | xargs) && cd mcp_server && uv run python -m protocol_bindings.a2a_server --host 0.0.0.0 --port $${PORT:-8000}

# Opens an interactive chat CLI wired to the locally-running A2A server
run-a2a-client:  ## Run agent chat client (connects to A2A server)
	docker run -it --network=host ghcr.io/cnoe-io/agent-chat-cli:stable

# Starts the agent in evaluation mode (creates/updates eval/dataset.yaml)
run-a2a-eval-mode:  ## Run agent in evaluation mode
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && uv run python eval_mode.py

# ============================================================================
# Validation Targets
# ============================================================================

# Validate OpenAPI spec
.PHONY: validate
validate:  ## Validate enhanced OpenAPI specification
	python ../../tests/test_openapi_validation.py enhanced_openapi.json

# Validate original spec
.PHONY: validate-original
validate-original:  ## Validate original OpenAPI specification
	python ../../tests/test_openapi_validation.py openapi_argo_workflows.json -v

# ============================================================================
# AgentGateway Targets
# ============================================================================

# Generate AgentGateway configuration from config.yaml
.PHONY: generate-agw-config
generate-agw-config:  ## Generate AgentGateway configuration file
	python ../../scripts/generate_agw_config.py config.yaml agw.yaml

# Start AgentGateway server
.PHONY: run-agentgateway
run-agentgateway:  ## Start AgentGateway server with enhanced OpenAPI spec
	agentgateway -f agw.yaml 2>&1 | tee agentgateway.log

# Stop AgentGateway server
.PHONY: stop-agentgateway
stop-agentgateway:  ## Stop running AgentGateway server
	@pkill -f "agentgateway -f agw.yaml" || echo "No AgentGateway process found"

# Validate AgentGateway configuration
.PHONY: agw-validate
agw-validate:  ## Validate AgentGateway configuration and OpenAPI spec
	@echo "Validating OpenAPI spec..."
	@python ../../tests/test_openapi_validation.py enhanced_openapi.json
	@echo ""
	@echo "✓ OpenAPI spec is valid"

# ============================================================================
# Generation Targets
# ============================================================================

# Generate enhanced MCP server with overlay
.PHONY: generate-enhanced
generate-enhanced:  ## Generate MCP server with LLM-enhanced overlay
	python -m openapi_mcp_codegen.enhance_and_generate \
		openapi_argo_workflows.json \
		mcp_server \
		config.yaml \
		--save-overlay overlay.yaml \
		--save-enhanced-spec enhanced_openapi.json

# Generate overlay only
.PHONY: generate-overlay
generate-overlay:  ## Generate OpenAPI overlay with LLM enhancements
	python -m openapi_mcp_codegen.overlay_generator \
		openapi_argo_workflows.json \
		overlay.yaml

# Apply existing overlay
.PHONY: apply-overlay
apply-overlay:  ## Apply overlay to OpenAPI spec
	python -m openapi_mcp_codegen.overlay_applier \
		openapi_argo_workflows.json \
		overlay.yaml \
		enhanced_openapi.json

# Generate MCP server from enhanced spec
.PHONY: generate-mcp
generate-mcp:  ## Generate MCP server from enhanced OpenAPI spec
	python -m openapi_mcp_codegen \
		--spec-file enhanced_openapi.json \
		--output-dir mcp_server

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
	@echo "Argo Workflows MCP Server - Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Environment variables:"
	@echo "  ARGO_WORKFLOWS_API_URL        API URL (required for runtime)"
	@echo "  ARGO_WORKFLOWS_TOKEN          Authentication token (required for runtime)"
	@echo "  MCP_PORT                      MCP HTTP server port (default: 3000)"
	@echo "  PORT                          A2A server port (default: 8000)"
	@echo ""
	@echo "LLM Enhancement (for generation):"
	@echo "  OPENAI_API_KEY                OpenAI API key for LLM overlay generation"
	@echo "  ANTHROPIC_API_KEY             Anthropic API key for LLM overlay generation"
	@echo "  LLM_PROVIDER                  LLM provider (openai or anthropic)"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. make generate-enhanced     # Generate with LLM enhancements"
	@echo "  2. make validate              # Validate the generated spec"
	@echo "  3. make generate-agw-config   # Generate AgentGateway config"
	@echo "  4. make run-agentgateway      # Start AgentGateway"
