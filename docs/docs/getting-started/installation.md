# Installation

## Prerequisites

- Python 3.8 or higher
- uv package manager (recommended) or pip

## Install uv (Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Using uvx (No Installation Required)

Run OpenAPI MCP Codegen directly without installation:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file your-spec.json \
  --output-dir ./output
```

## Local Installation

For development or repeated use:

```bash
# Clone repository
git clone https://github.com/cnoe-io/openapi-mcp-codegen.git
cd openapi-mcp-codegen

# Setup environment
uv venv && source .venv/bin/activate
uv sync

# Verify installation
python -m openapi_mcp_codegen --help
```

## Verify Installation

```bash
# Check version
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen --version

# Run with example
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir test_output
```

Next: [Basic Usage](./basic-usage.md)
