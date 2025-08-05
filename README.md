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


## ✨ Features

- ⚡ **Automatic MCP server generation** from OpenAPI specs
- 📝 Supports **JSON** and **YAML** formats
- 🔍 **Auto-detects** spec file type (`.json`, `.yaml`, `.yml`)
- 🛠️ **Tool modules** for each API endpoint
- 🤖 **API client code** generation
- 📋 **Logging** & **error handling** setup
- ⚙️ **Configuration files** (`pyproject.toml`, `.env.example`)
- 📚 **Comprehensive documentation** generation
- 🤖 **Enhanced Docstrings via LLM** integration
- 🚀 **`--generate-agent` flag** – additionally produces a LangGraph
  React agent (with A2A server, Makefile, README and .env.example)
  alongside the generated MCP server.

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

### 📦 Requirements

- 🐍 Python **3.13+**
- ⚡ [uv](https://docs.astral.sh/uv/getting-started/installation/)

**Note:** Install uv first: https://docs.astral.sh/uv/getting-started/installation/

### Run without cloning repo


#### Run from a stable tag


```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git@stable openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir examples/petstore/mcp_server \
  --generate-agent
```

#### 📌 Optional: Run from main branch

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

#### Run with option to enhance docstring using LLMs

```
# Generate with LLM-enhanced docstrings (requires LLM env vars)
uv run openapi_mcp_codegen --spec-file <spec.json> --output-dir <output> --enhance-docstring-with-llm
```

#### Run with option to generate a2a agent

```
# Generate with agent wrapper (creates LangGraph React agent + A2A server)
uv run openapi_mcp_codegen --spec-file <spec.json> --output-dir <output> --generate-agent
```

#### ▶️  Generate agent **with evaluation scaffolding**

```bash
uv run openapi_mcp_codegen \
  --spec-file <spec.json> \
  --output-dir <output-dir> \
  --generate-agent \
  --generate-eval          # ← NEW
```

The extra flag adds:

1. `eval_mode.py` – an interactive script that lets you chat with each tool, mark tests as _done_ or _skipped_ and stores the traces in `eval/dataset.yaml`.
2. `eval/evaluate_agent.py` – a LangSmith-powered benchmark that replays the dataset and uploads the scores (trajectory-accuracy, correctness, hallucination).

End-to-end workflow:

1. **Generate** the agent with `--generate-eval`
2. **Build a dataset:**

   ```bash
   cd <output-dir>
   uv run python eval_mode.py
   # … interactively exercise the tools …
   ```

   This produces / updates `eval/dataset.yaml`.

3. **Run the evaluation suite:**

   ```bash
   uv run python eval/evaluate_agent.py
   ```

   Results appear in your LangSmith dashboard (set `LANGCHAIN_API_KEY` etc.).

### Makefile Shortcuts

```bash
make generate -- --spec-file examples/petstore/openapi_petstore.json --output-dir examples/petstore/mcp_server
make generate-petstore  # Pre-configured petstore example
make generate-splunk    # Pre-configured splunk example with agent
make test               # Run pytest suite
make lint               # Run ruff linting
```

### Testing Generated Petstore MCP Server

#### Start Petstore Mockserver

```
cd examples/petstore
```

```
uv run python petstore_mock_server.py
```

_In a new terminal from the root of the git repo_

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

#### MCP Inspector Tool

The **MCP Inspector** is a utility for inspecting and debugging MCP servers. It provides a visual interface to explore generated tools, models, and APIs.

##### Installation

To install the MCP Inspector, use the following command:

```bash
npx @modelcontextprotocol/inspector
```

##### Usage

Run the inspector in your project directory to analyze the generated MCP server:

```bash
npx @modelcontextprotocol/inspector
```

This will launch a web-based interface where you can:

- Explore available tools and their operations
- Inspect generated models and their schemas
- Test API endpoints directly from the interface

For more details, visit the [MCP Inspector Documentation](https://modelcontextprotocol.io/legacy/tools/inspector).


### Testing Generated Agent
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
