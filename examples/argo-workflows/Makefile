# Makefile for Argo Workflows MCP Server


.PHONY: run-mcp-server run-mcp-http run-a2a run-a2a-and-slim run-a2a-client run-a2a-eval-mode eval reset help




# Runs the MCP server in stdio mode (for testing with MCP clients)
run-mcp-server:  ## Install deps and run the MCP server in stdio mode
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && uv run python -m mcp_argo_workflows.server

# Runs the MCP server in HTTP/SSE mode (for MCP Inspector and other HTTP clients)
run-mcp-http:  ## Install deps and run the MCP server in HTTP mode
	cd mcp_server && uv pip install -e . --upgrade
	cd mcp_server && export $$(grep -v '^#' .env | xargs) && MCP_MODE=http MCP_HOST=0.0.0.0 MCP_PORT=$${MCP_PORT:-3000} uv run python -m mcp_argo_workflows.server



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
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Environment variables:"
	@echo "  ARGO_WORKFLOWS_API_URL        API URL (required)"
	@echo "  ARGO_WORKFLOWS_TOKEN          Authentication token (required)"
	@echo "  MCP_PORT                      MCP HTTP server port (default: 3000)"

	@echo ""
	@echo "  OPENAI_API_KEY                OpenAI API key for LLM overlay generation"
	@echo "  ANTHROPIC_API_KEY             Anthropic API key for LLM overlay generation"
	@echo "  LLM_PROVIDER                  LLM provider (openai or anthropic)"
