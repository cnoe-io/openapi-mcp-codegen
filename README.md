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
- 🛠️ Tool modules for each API endpoint
- 🤖 API client code generation
- 📋 Logging & error handling setup
- ⚙️ Configuration files (`pyproject.toml`, `.env.example`)
- 📚 Comprehensive documentation generation
- 🚀 **--generate-agent** flag – additionally produces a LangGraph
  React agent (with A2A server, Makefile, README and .env.example)
  alongside the generated MCP server.
- 📊 **--generate-eval**: adds interactive eval mode and automated evaluation suite
- 🧠 **--generate-system-prompt**: generates a SYSTEM prompt for the agent using your configured LLM

## How It Works

- You provide an OpenAPI spec (JSON or YAML).
- The generator parses paths, operations, and schemas, then renders Jinja2 templates into a structured Python MCP server.
- Optionally, it generates an accompanying LangGraph agent and A2A server wrapper that can call the generated MCP tools.
- Also supports tracing and evaluation using [LangFuse](https://github.com/langfuse/langfuse)

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
  --generate-agent \
  --generate-eval
```

### Local Development Commands

```bash
# Setup venv
uv venv && source .venv/bin/activate

# Initial setup (requires uv CLI)
uv sync
```

## CLI Options

- **--generate-agent**
  - Produces a LangGraph React agent that wraps the generated MCP server
  - Includes A2A server, Makefile, README, and .env.example
- **--generate-eval**
  - Adds:
    - eval_mode.py (interactive dataset builder that stores traces in eval/dataset.yaml)
    - eval/evaluate_agent.py (LangFuse-powered evaluation using correctness, hallucination, and trajectory accuracy)
- **--generate-system-prompt**
  - Uses your configured LLM to create a SYSTEM prompt tailored to the generated tools
- **--enhance-docstring-with-llm**
  - Optionally rewrites tool docstrings using an LLM

## Example: Petstore MCP Server

1. Generate the agent + evals

```
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir examples/petstore \
  --generate-agent \
  --generate-eval
```

2. Configure your agent + LLM (see [LLM provider docs](https://cnoe-io.github.io/ai-platform-engineering/getting-started/docker-compose/configure-llms))
```
export LLM_PROVIDER=openai
export OPENAI_API_KEY=<your_openai_api_key>
export OPENAI_ENDPOINT=https://api.openai.com/v1
export OPENAI_MODEL_NAME=gpt-5

export PETSTORE_API_URL=http://0.0.0.0:10000
export PETSTORE_TOKEN=foo
```

3. Optionally, [deploy LangFuse](https://langfuse.com/self-hosting/docker-compose) and add the configuration
```
# Langfuse (observability) configuration
export LANGFUSE_PUBLIC_KEY=pk-lf-<public-key>
export LANGFUSE_SECRET_KEY=sk-lf-<secret-key>
export LANGFUSE_HOST=http://localhost:3000
export LANGFUSE_TRACING_ENABLED=True
```

4. Go to the agent directory and run the mock server.

```
cd examples/petstore
uv pip install "fastapi>=0.116"
uv run python petstore_mock_server.py
```

4. In a new terminal from the root of the git repo:

```
cd examples/petstore
make run-a2a
```

5. In a new terminal from the root of the git repo ([install Docker first](https://www.docker.com/get-started/)):
```
cd examples/petstore
make run-a2a-client
```

You now have an agent and client deployed, e.g. ask `List my available pets`. You can see tracing in LangFuse (http://localhost:3000) if enabled. Follow the next steps to evaluate your agent:

6. In a new terminal start the agent in eval mode. This will output the list of tools and prompt you to evaluate each one and build the dataset in `eval/dataset.yaml`

```
make run-a2a-eval-mode
```

7. Once you are done building the dataset, launch the evaluation:
```
make eval
```

This creates a new dataset in LangFuse and triggers an evaluation run.

### A2A Inspector Tool

The A2A Inspector is a utility for inspecting and debugging A2A servers. It provides a visual interface to explore agent cards and invoke the agent. Follow the instructions [on the project page](https://github.com/a2aproject/a2a-inspector) to build and run the inspector, which should be available at localhost:8080. You can then connect to the agent running on `localhost:8000/.well-known/agent.json`.

## Project-Specific Conventions

### Configuration Files

- Each example requires `config.yaml` with metadata such as authorization headers
- Generated `pyproject.toml` includes agent-specific dependencies
- `.env.example` templates include agent-specific environment variables

### Code Generation Patterns

- Operation IDs become Python function names (snake_case conversion)
- OpenAPI parameters map to function arguments with type hints
- Generated tools follow pattern: `async def operation_id(params) -> Any`
- API client uses `httpx` with configurable base URLs and headers

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

## Experimental

- --with-a2a-proxy (experimental)
  - Generates a minimal WebSocket upstream server intended to sit behind an external [a2a-proxy](https://github.com/artdroz/a2a-proxy).
  - Deploy the external a2a-proxy separately and configure it to connect to the WS upstream (ws://host:port). The proxy exposes an A2A HTTP API (e.g., /a2a/v1) for clients.
  - When combined with --generate-agent, a Makefile target may be provided (e.g. `make run-with-proxy`) to start the WS upstream locally.
  - This pathway is experimental and subject to change. Use for evaluation and prototyping only.

## Common Debugging Patterns

- Generated code includes extensive logging via Python's logging module
- Template variables accessible via Jinja2 context in `render_template()`
- Use `--dry-run` flag to preview generation without writing files
