# 🚀 OpenAPI to MCP Server Code Generator

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Conventional Commits](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/conventional_commits.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/conventional_commits.yml)
[![Ruff Linter](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/ruff.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/ruff.yml)
[![Super Linter](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/superlinter.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/superlinter.yml)
[![Unit Tests](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/unittest.yaml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/unittest.yaml)
[![Dependabot Updates](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/dependabot/dependabot-updates)

## Overview

This tool generates **Model Context Protocol (MCP) servers** from OpenAPI specifications, creating Python packages that can be used by AI assistants to interact with APIs. The core architecture transforms OpenAPI specs into structured MCP servers with tools, models, and client code.

## Quick Start

- Install uv
- Generate server (and optionally agent/eval):
  ```bash
  uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
    --spec-file examples/petstore/openapi_petstore.json \
    --output-dir examples/petstore/mcp_server \
    --generate-agent \
    --generate-eval \
    --generate-system-prompt
  ```

## ✨ Features

- ⚡ Automatic MCP server generation from OpenAPI specs
- 📝 Supports JSON and YAML formats
- 🔍 Auto-detects spec file type (`.json`, `.yaml`, `.yml`)
- 🛠️ Tool modules for each API endpoint
- 🤖 API client code generation
- 📋 Logging & error handling setup
- ⚙️ Configuration files (`pyproject.toml`, `.env.example`)
- 📚 Comprehensive documentation generation
- 🚀 --generate-agent flag – additionally produces a LangGraph
  React agent (with A2A server, Makefile, README and .env.example)
  alongside the generated MCP server.
- 📊 --generate-eval: adds interactive eval mode and automated evaluation suite
- 🧠 --generate-system-prompt: generates a SYSTEM prompt for the agent using your configured LLM

## How It Works

- You provide an OpenAPI spec (JSON or YAML).
- The generator parses paths, operations, and schemas, then renders Jinja2 templates into a structured Python MCP server.
- Optionally, it generates an accompanying LangGraph agent and A2A server wrapper that can call the generated MCP tools.
- With evaluation enabled, it scaffolds interactive dataset building and a LangSmith-powered evaluation suite.

## Generated Structure

```
mcp_<service>/
├── api/client.py
├── models/
├── tools/
└── server.py

# When --generate-agent is used (rendered into <output-dir>):
protocol_bindings/a2a_server/
├── __main__.py
├── agent.py
├── agent_executor.py
├── helpers.py
└── state.py
Makefile
README.md               # agent README
agent.py                # agent creation code
.env.example

# When --generate-eval is also used:
eval/
├── evaluate_agent.py
eval_mode.py
```

## Development

### Requirements

- 🐍 Python 3.13+
- ⚡ uv (https://docs.astral.sh/uv/getting-started/installation/)

Note: Install uv first: https://docs.astral.sh/uv/getting-started/installation/

### Run without cloning the repo

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir examples/petstore/mcp_server \
  --generate-agent
```

### Local Development Commands

```bash
# Setup venv
uv venv && source .venv/bin/activate

# Initial setup (requires uv CLI)
uv sync
```

#### Run without options

```
# Generate MCP server from spec
uv run openapi_mcp_codegen --spec-file <spec.json> --output-dir <output>
```

## CLI Options

- --generate-agent
  - Produces a LangGraph React agent that wraps the generated MCP server
  - Includes A2A server, Makefile, README, and .env.example
- --generate-eval
  - Adds:
    - eval_mode.py (interactive dataset builder that stores traces in eval/dataset.yaml)
    - eval/evaluate_agent.py (LangSmith-powered evaluation using correctness, hallucination, and trajectory accuracy)
- --generate-system-prompt
  - Uses your configured LLM to create a SYSTEM prompt tailored to the generated tools
  - Falls back to a concise default if LLM fails/unavailable
- --enhance-docstring-with-llm, --enhance-docstring-with-llm-openapi
  - Optionally rewrites tool docstrings using an LLM (the latter also embeds OpenAPI snippets)

## Evaluation

End-to-end workflow:

1. Generate with --generate-agent and --generate-eval (optionally add --generate-system-prompt)
   ```bash
   cd <output-dir>
   ```
2. Build a dataset:
   ```bash
   make run-a2a-eval-mode
   # … interactively exercise the tools …
   ```
   This produces / updates `eval/dataset.yaml`.

3. Run the evaluation suite:
   ```bash
   make eval
   ```
   Results appear in your LangSmith dashboard (set `LANGCHAIN_API_KEY` etc.).

## Example: Petstore MCP Server

#### Start Petstore Mockserver

```
cd examples/petstore
```

```
uv run python petstore_mock_server.py
```

In a new terminal from the root of the git repo:

```
cd examples/petstore/mcp_server
```

```
export PETSTORE_API_URL=http://0.0.0.0:10000
export PETSTORE_TOKEN=foo
export MCP_MODE=http
export MCP_HOST=localhost
export MCP_PORT=8000
``

```
uv run python mcp_petstore/server.py
```

### MCP Inspector Tool

The MCP Inspector is a utility for inspecting and debugging MCP servers. It provides a visual interface to explore generated tools, models, and APIs.

#### Installation

```bash
npx @modelcontextprotocol/inspector
```

#### Usage

Run the inspector in your project directory to analyze the generated MCP server:

```bash
npx @modelcontextprotocol/inspector
```

This will launch a web-based interface where you can:

- Explore available tools and their operations
- Inspect generated models and their schemas
- Test API endpoints directly from the interface

For more details, visit the MCP Inspector Documentation:
https://modelcontextprotocol.io/legacy/tools/inspector

## Example: Generated Agent (A2A)

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

- --generate-system-prompt will use your configured LLM to craft a SYSTEM prompt.
- --enhance-docstring-with-llm and --enhance-docstring-with-llm-openapi optionally rewrite tool docstrings with richer content.
- Ensure appropriate LLM credentials are exported (e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY, or provider-specific keys).

## Integration Points

### External Dependencies

- MCP Protocol: Uses `mcp>=1.9.0` for FastMCP server implementation
- uv Package Manager: Required for dependency management and execution
- Jinja2: Template engine for code generation
- Ruff: Code formatting and linting (auto-applied to generated code)

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
