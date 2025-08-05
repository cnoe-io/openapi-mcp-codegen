# 🚀 OpenAPI to MCP Server Code Generator

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Conventional Commits](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/conventional_commits.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/conventional_commits.yml)
[![Ruff Linter](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/ruff.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/ruff.yml)
[![Super Linter](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/superlinter.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/superlinter.yml)
[![Unit Tests](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/unittest.yaml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/unittest.yaml)
[![Dependabot Updates](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/dependabot/dependabot-updates)

---

## Project Overview

This tool generates **Model Context Protocol (MCP) servers** from OpenAPI specifications, creating Python packages that can be used by AI assistants to interact with APIs. The core architecture transforms OpenAPI specs into structured MCP servers with tools, models, and client code.

## Key Architecture Components

### Core Generation Flow

- `openapi_mcp_codegen/mcp_codegen.py`: Main generator class that orchestrates code generation
- `openapi_mcp_codegen/templates/`: Jinja2 templates for all generated components
- Generated structure: `mcp_<service_name>/` with submodules for `api/`, `models/`, `tools/`, `server.py`

### Template System Patterns

- Templates use `.tpl` extension and Jinja2 syntax
- Generated files include copyright headers from `config.yaml`
- Tool modules auto-generated from OpenAPI paths/operations
- Models generated from OpenAPI schemas with Python type mapping

## Essential Development Workflows

### Local Development Commands

```bash
# Initial setup (requires uv CLI)
uv sync

# Generate MCP server from spec
uv run openapi_mcp_codegen --spec-file <spec.json> --output-dir <output>

# Generate with LLM-enhanced docstrings (requires LLM env vars)
uv run openapi_mcp_codegen --spec-file <spec.json> --output-dir <output> --enhance-docstring-with-llm

# Generate with agent wrapper (creates LangGraph React agent + A2A server)
uv run openapi_mcp_codegen --spec-file <spec.json> --output-dir <output> --generate-agent
```

### Makefile Shortcuts

```bash
make generate -- --spec-file examples/petstore/openapi_petstore.json --output-dir examples/petstore/mcp_server
make generate-petstore  # Pre-configured petstore example
make generate-splunk    # Pre-configured splunk example with agent
make test               # Run pytest suite
make lint               # Run ruff linting
```

### Testing Generated Servers

Generated servers include A2A (Agent-to-Agent) capabilities when using `--generate-agent`:

```bash
cd examples/petstore/mcp_server
cp .env.example .env    # Configure API credentials
make run-a2a           # Start A2A server
make run-a2a-client    # Launch Docker chat client
```

## Project-Specific Conventions

### Configuration Files

- Each example requires `config.yaml` with metadata (title, author, dependencies)
- Generated `pyproject.toml` includes MCP-specific dependencies
- `.env.example` templates include service-specific environment variables

### Code Generation Patterns

- Operation IDs become Python function names (snake_case conversion)
- OpenAPI parameters map to function arguments with type hints
- Generated tools follow pattern: `async def operation_id(params) -> Any`
- API client uses `httpx` with configurable base URLs and headers

### LLM Integration

- Optional docstring enhancement via `cnoe-agent-utils` LLMFactory
- Supports multiple LLM providers (OpenAI, Anthropic, Google Gemini)
- Uses LangChain for LLM interactions and prompt templating

## Integration Points

### External Dependencies

- **MCP Protocol**: Uses `mcp>=1.9.0` for FastMCP server implementation
- **uv Package Manager**: Required for dependency management and execution
- **Jinja2**: Template engine for code generation
- **Ruff**: Code formatting and linting (auto-applied to generated code)

### Generated Component Structure

```
mcp_<service>/
├── api/client.py          # HTTP client with auth headers
├── models/               # Pydantic models from OpenAPI schemas
├── tools/               # One module per OpenAPI path
├── server.py           # FastMCP server entry point
└── agent.py           # LangGraph wrapper (if --generate-agent)
```

## Key Files for Understanding

- `openapi_mcp_codegen/mcp_codegen.py`: Core generation logic and template rendering
- `openapi_mcp_codegen/templates/`: Template structure mirrors output structure
- `examples/petstore/`: Complete working example with OpenAPI spec and config
- `tests/test_mcp_codegen.py`: Integration tests showing expected generation flow

## Common Debugging Patterns

- Generated code includes extensive logging via Python's logging module
- Ruff auto-formatting applied to all generated Python files
- Template variables accessible via Jinja2 context in `render_template()`
- Use `--dry-run` flag to preview generation without writing files
