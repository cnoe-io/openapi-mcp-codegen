# Basic Usage

Learn how to use OpenAPI MCP Codegen for common scenarios and understand the available CLI options.

## Basic Generation

Generate a simple MCP server from an OpenAPI specification:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file your-api-spec.json \
  --output-dir ./generated_mcp_server
```

## CLI Options

### Core Generation Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--spec-file` | Path to OpenAPI specification (JSON/YAML) | `--spec-file api.json` |
| `--output-dir` | Output directory for generated code | `--output-dir ./mcp_server` |

### Enhancement Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--generate-agent` | Create LangGraph React agent | `false` |
| `--generate-eval` | Include evaluation framework | `false` |
| `--generate-system-prompt` | Generate AI system prompt | `false` |
| `--enhance-docstring-with-llm` | Use LLM for docstring enhancement | `false` |

### Experimental Flags

| Flag | Description | Status |
|------|-------------|--------|
| `--enable-slim` | Enable SLIM transport support | Experimental |
| `--with-a2a-proxy` | Generate WebSocket upstream server | Experimental |

## Common Usage Patterns

### 1. Basic MCP Server

For simple API integration:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir examples/petstore/mcp_server
```

**Generated**:
- MCP server package
- API client code
- Tool modules for each endpoint
- Configuration templates

### 2. Complete Agent System

For full AI agent development:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir examples/petstore \
  --generate-agent \
  --generate-eval \
  --generate-system-prompt
```

**Generated**:
- MCP server package
- LangGraph React agent
- A2A server wrapper
- Evaluation framework
- System prompt optimization
- Makefile for development

### 3. Enhanced with LLM Pipeline

For AI-optimized documentation:

```bash
# Set LLM API key
export OPENAI_API_KEY=your-key-here

# Generate with enhancements
python -m openapi_mcp_codegen.enhance_and_generate \
    examples/argo-workflows/openapi_argo_workflows.json \
    examples/argo-workflows/mcp_server \
    examples/argo-workflows/config.yaml \
    --save-overlay overlay.yaml \
    --save-enhanced-spec enhanced_openapi.json
```

**Benefits**:
- AI-generated descriptions optimized for function calling
- OpenAI-compatible format (&lt;300 characters)
- "Use when:" context patterns
- Smart parameter handling for complex schemas

## Configuration Files

### config.yaml Structure

```yaml
# Package Identification
title: petstore                     # → mcp_petstore package
description: Petstore API MCP Server
author: Your Name
email: you@example.com
version: 0.1.0
license: Apache-2.0
python_version: 3.8

# API Authentication
headers:
  Authorization: Bearer {token}      # Placeholder for runtime token
  Accept: application/json
  Content-Type: application/json

# Python Dependencies
poetry_dependencies: |
  python = ">=3.8,<4.0"
  httpx = ">=0.24.0"
  python-dotenv = ">=1.0.0"
  pydantic = ">=2.0.0"
  mcp = ">=1.9.0"

# Enhancement Configuration (Optional)
overlay_enhancements:
  enabled: true
  use_llm: true
  max_description_length: 300
  enhance_crud_operations: true
  add_use_cases: true
```

### Environment Variables

```bash
# API Configuration (Required)
PETSTORE_API_URL=https://petstore.swagger.io/v2
PETSTORE_TOKEN=your-api-token

# LLM Configuration (Optional, for enhancements)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=openai  # or anthropic

# Evaluation/Tracing (Optional)
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
```

## Generated Code Patterns

### Tool Function Structure

Generated tools follow consistent patterns:

```python
async def pet_service_find_pets_by_status(
    param_status: str = None
) -> Any:
    """
    Find pets by status

    OpenAPI Description:
        Find pets by status. Use when: you need to filter pets by
        their availability status (available, pending, sold).

    Args:
        param_status (str): Pet status filter

    Returns:
        Any: List of pets matching the status filter
    """
    logger.debug("Making GET request to /pet/findByStatus")

    params = {}
    if param_status is not None:
        params["status"] = param_status

    success, response = await make_api_request(
        "/pet/findByStatus",
        method="GET",
        params=params
    )

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}

    return response
```

### Smart Parameter Handling

For complex schemas (>10 nested parameters):

```python
# Instead of 1000+ parameters, use clean dictionary interface
async def complex_operation(
    body_metadata: Dict[str, Any] = None,
    body_spec: Dict[str, Any] = None
) -> Any:
    """Clean interface for complex Kubernetes-style schemas"""
```

## Development Workflow

### 1. Setup Environment

```bash
cd generated_mcp_server/
uv venv && source .venv/bin/activate
uv sync
```

### 2. Configure API Access

```bash
cp .env.example .env
# Edit .env with your API credentials
```

### 3. Test MCP Server

```bash
# Run in stdio mode
uv run python -m mcp_petstore.server

# Or use generated Makefile
make run-mcp-server
```

### 4. Test with Agent (if generated)

```bash
# Start agent server
make run-a2a

# In new terminal, start client
make run-a2a-client
```

## Best Practices

### File Organization
- Keep original OpenAPI specs in version control
- Store `config.yaml` and `prompt.yaml` (if using enhancements)
- Generated code can be recreated, so consider gitignore
- Save overlays for review and customization

### Configuration
- Use environment variables for secrets (API keys, tokens)
- Document required environment variables in README
- Provide `.env.example` templates
- Use descriptive package names in `config.yaml`

### Testing
- Use mock servers for development testing
- Include evaluation datasets when using `--generate-eval`
- Test with real API endpoints before deployment
- Monitor LangFuse traces for agent behavior

### Enhancements
- Review generated overlays before production use
- Customize descriptions for domain-specific terminology
- Iterate on prompts for better LLM enhancement
- Use rule-based fallback if LLM unavailable

## Next Steps

- [Configure your environment](./configuration.md) in detail
- [Explore the examples](./examples.md) for different API types
- [Learn about CLI commands](../cli/commands.md)
- [Understand troubleshooting](../cli/troubleshooting.md)
