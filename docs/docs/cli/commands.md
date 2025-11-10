# CLI Commands

OpenAPI MCP Codegen provides two main commands through its CLI interface:

## Primary Commands

### generate-mcp

Generate MCP servers with optional agent wrappers, evaluation frameworks, and system prompt generation:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-mcp \
  --spec-file INPUT_SPEC \
  --output-dir OUTPUT_DIR \
  [OPTIONS]
```

**Core Features:**
- Transforms OpenAPI specs into production-ready MCP servers
- Optional LangGraph agent wrapper generation
- System prompt generation using LLMs
- Evaluation framework creation
- LLM-enhanced docstring generation

### generate-a2a-agent-with-remote-mcp

Generate standalone A2A agents that connect to external MCP servers:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-a2a-agent-with-remote-mcp \
  --spec-file INPUT_SPEC \
  --agent-name AGENT_NAME \
  --mcp-server-url SERVER_URL \
  [OPTIONS]
```

**Core Features:**
- Creates complete A2A-compatible agent packages
- Connects to external MCP servers (like AgentGateway)
- Skills-based architecture with configurable capabilities
- Protocol bindings for different transport mechanisms

## generate-mcp Options

| Option | Description | Default |
|--------|-------------|---------|
| `--spec-file` | Path to OpenAPI specification (JSON/YAML) | Required |
| `--output-dir` | Directory for generated MCP server | `<script_dir>/<mcp_name>` |
| `--generate-agent` | Create LangGraph agent wrapper | `false` |
| `--generate-eval` | Include evaluation framework | `false` |
| `--generate-system-prompt` | Generate AI system prompt using LLM | `false` |
| `--enhance-docstring-with-llm` | Enhance docstrings using LLM | `false` |
| `--enhance-docstring-with-llm-openapi` | Include OpenAPI spec in enhanced docstrings | `false` |
| `--with-a2a-proxy` | Generate WebSocket upstream server | `false` |
| `--enable-slim` | Enable SLIM transport support | `false` |
| `--dry-run` | Run without writing files | `false` |
| `--log-level` | Set logging level (debug, info, warning, error) | `info` |

## generate-a2a-agent-with-remote-mcp Options

| Option | Description | Default |
|--------|-------------|---------|
| `--spec-file` | Path to OpenAPI specification (JSON/YAML) | Required |
| `--agent-name` | Name of the agent (e.g., 'argo_workflows') | Required |
| `--mcp-server-url` | URL of the external MCP server | Required |
| `--output-dir` | Directory for generated A2A agent | `./agent_<agent_name>` |
| `--agent-description` | Description of the agent | Auto-generated |
| `--dry-run` | Run without writing files | `false` |

## Usage Examples

### Basic MCP Server Generation

```bash
# Generate basic MCP server
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-mcp \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir ./petstore_mcp
```

### Complete Agent System

```bash
# Generate MCP server with agent wrapper and evaluation
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-mcp \
  --spec-file examples/argo-workflows/openapi_argo_workflows.json \
  --output-dir ./argo_workflows \
  --generate-agent \
  --generate-eval \
  --generate-system-prompt \
  --enhance-docstring-with-llm
```

### Standalone A2A Agent

```bash
# Generate A2A agent for external MCP server
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-a2a-agent-with-remote-mcp \
  --spec-file examples/argo-workflows/openapi_argo_workflows.json \
  --agent-name "Argo Workflows" \
  --mcp-server-url "http://localhost:3000" \
  --agent-description "AI agent for Argo Workflows management"
```

For complete option reference, run with `--help`.
