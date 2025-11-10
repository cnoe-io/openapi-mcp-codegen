# Petstore Example

The Petstore example demonstrates basic MCP server generation with a simple REST API.

## Overview

- **API**: Swagger Petstore (OpenAPI 3.0)
- **Operations**: 20 endpoints for pet management
- **Features**: Basic CRUD operations, file uploads, simple authentication

## Quick Start

```bash
cd examples/petstore
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file openapi_petstore.json \
  --output-dir . \
  --generate-agent \
  --generate-eval
```

## Generated Structure

```
examples/petstore/
├── mcp_server/           # Generated MCP server
├── agent/                # LangGraph agent (if --generate-agent)
├── eval/                 # Evaluation framework (if --generate-eval)
├── openapi_petstore.json # Original API specification
└── config.yaml          # Configuration file
```

## Testing

```bash
# Start mock server
uv run python petstore_mock_server.py

# Start agent (in new terminal)
make run-a2a

# Test with client (in new terminal)
make run-a2a-client
```

For complete walkthrough, see the README in `examples/petstore/`.
