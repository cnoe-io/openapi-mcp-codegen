# Basic Usage

Learn how to use OpenAPI MCP Codegen's two main generation modes: **MCP Server Generation** and **A2A Agent Generation**.

## Generation Modes Overview

OpenAPI MCP Codegen provides two distinct generation capabilities:

### 1. MCP Server Generation
Create self-contained MCP servers that expose API functionality directly through the MCP protocol.

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-mcp \
  --spec-file your-api-spec.json \
  --output-dir ./mcp_server
```

### 2. A2A Agent Generation
Create standalone agents that connect to external MCP servers (like those deployed via AgentGateway).

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-a2a-agent-with-remote-mcp \
  --spec-file your-api-spec.json \
  --agent-name "Your Agent" \
  --mcp-server-url "http://agentgateway:3000"
```

## Command-Specific Options

### generate-mcp Options

| Flag | Description | Default |
|------|-------------|---------|
| `--spec-file` | Path to OpenAPI specification (JSON/YAML) | Required |
| `--output-dir` | Output directory for generated MCP server | Auto-generated |
| `--generate-agent` | Create LangGraph agent wrapper | `false` |
| `--generate-eval` | Include evaluation framework | `false` |
| `--generate-system-prompt` | Generate AI system prompt using LLM | `false` |
| `--enhance-docstring-with-llm` | Enhance docstrings using LLM | `false` |
| `--with-a2a-proxy` | Generate WebSocket upstream server | `false` |
| `--enable-slim` | Enable SLIM transport support | `false` |
| `--dry-run` | Run without writing files | `false` |

### generate-a2a-agent-with-remote-mcp Options

| Flag | Description | Default |
|------|-------------|---------|
| `--spec-file` | Path to OpenAPI specification (JSON/YAML) | Required |
| `--agent-name` | Name of the agent (e.g., 'Argo Workflows') | Required |
| `--mcp-server-url` | URL of external MCP server | Required |
| `--output-dir` | Output directory for generated A2A agent | `./agent_<name>` |
| `--agent-description` | Description of the agent | Auto-generated |
| `--dry-run` | Run without writing files | `false` |

## Usage Patterns by Scenario

### 1. Basic MCP Server Generation

Create a self-contained MCP server for direct API integration:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-mcp \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir ./petstore_mcp
```

**Generated Output:**
- Complete MCP server package (`mcp_petstore/`)
- Type-safe API client with async support
- Tool modules for each API endpoint
- Configuration templates and documentation

**Use Case:** Direct integration where you control the MCP server deployment

### 2. Complete Agent System

Generate MCP server with full agent wrapper and intelligence features:

```bash
# Set LLM API key for system prompt generation
export OPENAI_API_KEY=your-key-here

uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-mcp \
  --spec-file examples/argo-workflows/openapi_argo_workflows.json \
  --output-dir ./argo_agent_system \
  --generate-agent \
  --generate-eval \
  --generate-system-prompt \
  --enhance-docstring-with-llm
```

**Generated Output:**
- MCP server package
- LangGraph agent wrapper with A2A bindings
- Evaluation framework for testing
- LLM-generated system prompt
- Enhanced function documentation
- Complete development tooling

**Use Case:** Full AI agent development with evaluation and intelligence enhancements

### 3. Standalone A2A Agent

Create an agent that connects to an external MCP server:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-a2a-agent-with-remote-mcp \
  --spec-file examples/argo-workflows/openapi_argo_workflows.json \
  --agent-name "Argo Workflows Expert" \
  --mcp-server-url "http://agentgateway:3000/argo-workflows" \
  --agent-description "Specialized AI agent for Argo Workflows management and operations"
```

**Generated Output:**
- Complete A2A agent package (`agent_argo_workflows_expert/`)
- Protocol bindings for external MCP server connection
- Agent card with capability definitions
- Skills-based architecture
- Client integration code

**Use Case:** Integration with existing MCP infrastructure like AgentGateway

### 4. Development and Testing

Use dry-run mode for testing generation without writing files:

```bash
# Test MCP server generation
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-mcp \
  --spec-file your-api.json \
  --dry-run

# Test A2A agent generation
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen generate-a2a-agent-with-remote-mcp \
  --spec-file your-api.json \
  --agent-name "Test Agent" \
  --mcp-server-url "http://localhost:3000" \
  --dry-run
```

**Benefits:**
- Validate configuration and OpenAPI specs
- Test generation logic without file system changes
- Preview generated structure and components

## Configuration Files

### config.yaml Structure

The configuration file defines generation parameters and metadata:

```yaml
# Package Identification (Required)
title: petstore                     # → mcp_petstore package name
description: Petstore API MCP Server
author: Your Name
email: you@example.com
version: 0.1.0
license: Apache-2.0

# API Configuration (MCP Server Generation)
headers:
  Authorization: Bearer {token}      # Runtime token placeholder
  Accept: application/json
  Content-Type: application/json

# A2A Agent Configuration (A2A Agent Generation)
skills:
  - name: "Pet Management"
    description: "Manage pet store inventory"
    examples:
      - "Find pets by status"
      - "Add new pets to store"
      - "Update pet information"

system_prompt: |
  You are a Petstore API expert assistant.
  Help users manage pet store operations including
  inventory, orders, and customer management.

# Python Dependencies (Optional)
poetry_dependencies: |
  python = ">=3.13,<4.0"
  httpx = ">=0.24.0"
  python-dotenv = ">=1.0.0"
  pydantic = ">=2.0.0"
  mcp = ">=1.9.0"
```

### Environment Variables

Runtime configuration for generated MCP servers and A2A agents:

```bash
# API Configuration (Required for MCP servers)
API_URL=https://api.example.com
API_TOKEN=your-api-token

# A2A Agent Configuration (Required for A2A agents)
AGENT_NAME=your_agent
MCP_SERVER_URL=http://agentgateway:3000

# LLM Configuration (Optional, for system prompt & docstring generation)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Tracing and Evaluation (Optional)
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
```

## Generated Code Patterns

### MCP Server Tool Functions

Generated MCP server tools follow consistent patterns:

```python
async def pet_service_find_pets_by_status(
    param_status: str = None
) -> Any:
    """
    Find pets by status

    Args:
        param_status (str): Pet status filter (available, pending, sold)

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

### A2A Agent Structure

Generated A2A agents include capability definitions:

```python
# agentcard.py
class AgentCard:
    name: str = "petstore_agent"
    display_name: str = "Petstore Expert"
    description: str = "AI agent for pet store management"

    skills: List[Dict[str, Any]] = [
        {
            "name": "Pet Management",
            "description": "Manage pet inventory and information",
            "examples": ["Find pets by status", "Add new pets"]
        }
    ]

    system_prompt: str = "You are a Petstore API expert..."
    mcp_server_url: str = "http://agentgateway:3000/petstore"
```

### Smart Parameter Handling

For complex schemas (>10 nested parameters), the generator automatically uses dictionary mode:

```python
# Instead of 1000+ individual parameters
async def complex_kubernetes_operation(
    body_metadata: Dict[str, Any] = None,
    body_spec: Dict[str, Any] = None
) -> Any:
    """
    Clean interface for complex Kubernetes-style schemas

    Args:
        body_metadata: Kubernetes metadata dictionary
        body_spec: Kubernetes spec dictionary
    """
```

## Development Workflows

### MCP Server Development

**1. Generate and Setup:**
```bash
# Generate MCP server
uvx openapi_mcp_codegen generate-mcp --spec-file api.json --output-dir ./mcp_server

# Setup environment
cd mcp_server/
uv venv && source .venv/bin/activate
uv sync
```

**2. Configure and Test:**
```bash
# Configure API access
cp .env.example .env
# Edit .env with API credentials

# Test MCP server
uv run python -m mcp_server.server

# Test with agent-chat-cli
uvx agent-chat-cli --mcp-server stdio --server-command "uv run python -m mcp_server.server"
```

### A2A Agent Development

**1. Generate and Setup:**
```bash
# Generate A2A agent
uvx openapi_mcp_codegen generate-a2a-agent-with-remote-mcp \
  --spec-file api.json \
  --agent-name "API Expert" \
  --mcp-server-url "http://agentgateway:3000"

# Setup environment
cd agent_api_expert/
make dev
```

**2. Configure and Test:**
```bash
# Configure environment
cp .env.example .env
# Edit .env with MCP server URL and credentials

# Start A2A server
make run-a2a

# Test with A2A client
make run-a2a-client
```

## Best Practices

### Configuration Management
- Store `config.yaml` in version control with OpenAPI specs
- Use environment variables for secrets (API keys, tokens, URLs)
- Provide comprehensive `.env.example` templates
- Document required environment variables in generated README

### Development
- Use descriptive names for agents and MCP server packages
- Test with mock servers during development
- Validate with real API endpoints before production deployment
- Use `--dry-run` to preview generation before writing files

### MCP Server Best Practices
- Configure appropriate API timeouts and retry logic
- Monitor API rate limits and implement backoff strategies
- Use generated evaluation frameworks to test tool accuracy
- Deploy behind AgentGateway for A2A protocol exposure

### A2A Agent Best Practices
- Define clear, focused skills and capabilities in config
- Test connectivity to external MCP servers before deployment
- Monitor agent performance with tracing and evaluation
- Use meaningful agent names and descriptions for discoverability

### Production Deployment
- Use container deployments for consistency and scaling
- Implement health checks for both MCP servers and A2A agents
- Configure appropriate resource limits and monitoring
- Plan for horizontal scaling based on usage patterns

## Choosing Between MCP Server and A2A Agent

### Use MCP Server Generation When:
- You need direct control over the MCP server deployment
- Building new API integrations from scratch
- Want self-contained, standalone MCP servers
- Deploying in environments without existing MCP infrastructure

### Use A2A Agent Generation When:
- Integrating with existing MCP server infrastructure (AgentGateway)
- Building agents for distributed, multi-agent systems
- Want to leverage existing MCP server deployments
- Need agents that can connect to remote MCP services

## Next Steps

- [Explore detailed CLI commands](../cli/commands.md)
- [Learn about core components](../core-components/)
- [Review configuration options](./configuration.md)
- [See practical examples](./examples.md)
