# {{ agent_display_name }} A2A Agent

{{ agent_description }}

## Overview

This is a standalone Agent-to-Agent (A2A) compatible agent that connects to an external MCP server to provide {{ agent_display_name }} functionality. The agent follows the A2A protocol and can be integrated with other A2A-compatible systems.

## Architecture

This is a **remote A2A agent** that connects to an external MCP server (AgentGateway) to access {{ agent_display_name }} functionality. The architecture follows this flow:

```mermaid
graph LR
    A[Agent Chat CLI] -->|A2A Protocol| B[{{ agent_display_name }} A2A Agent]
    B -->|HTTP/JSON| C[MCP Server<br/>AgentGateway]
    C -->|OpenAPI Tools| D[{{ agent_display_name }} API]

    A1[User Query] --> A
    A --> A2[Streaming Response]
    B --> B1[Agent Logic<br/>Response Formatting]
    C --> C1[Tool Translation<br/>API Calls]
    D --> D1[{{ agent_display_name }}<br/>Operations]

    style A fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    style B fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    style C fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    style D fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
```

### Component Details

- **Agent Chat CLI**: Interactive client that communicates with the agent via A2A protocol
- **{{ agent_display_name }} A2A Agent**: This agent implementation that processes requests and formats responses
- **MCP Server (AgentGateway)**: External server that exposes {{ agent_display_name }} functionality as MCP tools
- **{{ agent_display_name }} API**: The actual target API that performs the operations

### Agent Structure

- **Agent Core**: Main agent logic in `agent_{{ agent_name }}/`
- **Protocol Bindings**: A2A server implementation in `protocol_bindings/a2a_server/`
- **Client Integration**: A2A client wrapper in `clients/a2a/`
- **Utils**: Local dependencies and helper functions in `utils/`

## Configuration

The agent connects to the MCP server at:
```
{{ mcp_server_url }}
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `A2A_HOST` | `localhost` | Host for the A2A agent server |
| `A2A_PORT` | `10000` | Port for the A2A agent server |
| `A2A_TRANSPORT` | `p2p` | Transport mode (`p2p` or `slim`) |
| `SLIM_ENDPOINT` | `http://slim-dataplane:46357` | SLIM endpoint (if using SLIM transport) |
| `MCP_SERVER_URL` | `{{ mcp_server_url }}` | MCP server endpoint |

**Service-Specific Configuration**:
| Variable | Default | Description |
|----------|---------|-------------|
| `{{ mcp_name.upper() }}_VERIFY_SSL` | `true` | Enable/disable SSL certificate verification. Falls back to `VERIFY_SSL` if not set. |
| `{{ mcp_name.upper() }}_CA_BUNDLE` | | Path to custom CA bundle for SSL verification |

**Legacy Environment Variables** (for compatibility):
| Variable | Default | Description |
|----------|---------|-------------|
| `{{ agent_name.upper() }}_AGENT_HOST` | `localhost` | Legacy host setting |
| `{{ agent_name.upper() }}_AGENT_PORT` | `8000` | Legacy port setting |

## Installation

### Prerequisites

- Python 3.13+
- `uv` package manager

### Setup

1. Clone/extract the agent code
2. Setup environment and dependencies:
   ```bash
   make dev  # Sets up venv, .env, dependencies, and formatting
   ```

   Or step by step:
   ```bash
   make setup-venv  # Create virtual environment
   make setup-env   # Create .env from .env.example
   make uv-sync     # Install dependencies
   ```

3. Configure your environment:
   ```bash
   # Edit .env file with your API keys and settings
   vi .env
   ```

## Usage

### Running the Agent

```bash
# Run with default settings (localhost:10000)
make run-a2a

# Run with custom host/port via environment variables
A2A_HOST=0.0.0.0 A2A_PORT=8080 make run-a2a

# Or directly with uv
uv run python -m agent_{{ agent_name }}

# With custom host/port via command line
uv run python -m agent_{{ agent_name }} --host 0.0.0.0 --port 8080

# View help for all options
uv run python -m agent_{{ agent_name }} --help
```

### Integration with Other A2A Agents

The agent can be used from other A2A systems:

```python
from agent_{{ agent_name }}.clients.a2a.agent import a2a_remote_agent

# Use the agent tool in your A2A application
result = a2a_remote_agent.invoke({"query": "Your request here"})
```

## Agent Capabilities

The {{ agent_display_name }} agent provides the following capabilities:

{% for example in skill_examples %}
- {{ example }}
{% endfor %}

## Development

### Available Make Targets

```bash
make help          # Show available commands
make setup-venv    # Create virtual environment
make setup-env     # Create .env from .env.example
make dev           # Complete development setup (venv + env + deps + format + lint)
make run-a2a       # Run the A2A agent
make test          # Run tests
make format        # Format code with ruff
make lint          # Lint code with ruff
make clean         # Clean up generated files and venv
```

### Testing

```bash
make test
```

### Code Formatting

```bash
make format
make lint
```

## Transport Modes

The agent supports two transport modes:

### P2P Mode (Default)

Direct peer-to-peer communication:
```bash
export A2A_TRANSPORT=p2p
make run-a2a
```

### SLIM Mode

Integration with SLIM transport layer:
```bash
export A2A_TRANSPORT=slim
export SLIM_ENDPOINT=http://your-slim-endpoint:46357
make run-a2a
```

## API Integration

This agent connects to the {{ agent_display_name }} MCP server to provide access to:

- API operations exposed through the MCP protocol
- Real-time communication with {{ agent_display_name }} services
- Type-safe parameter validation
- Structured response handling

## Contributing

1. Follow the existing code structure
2. Run tests before submitting changes
3. Use `make format` and `make lint` to ensure code quality
4. Update documentation as needed

## License

Apache-2.0 License

## Generated Configuration

This agent was generated using the OpenAPI MCP Codegen tool with the following configuration:

- **Agent Name**: {{ agent_name }}
- **MCP Server URL**: {{ mcp_server_url }}
- **Generated**: {{ timestamp }}

For more information about the OpenAPI MCP Codegen tool, see: https://github.com/cnoe-io/openapi-mcp-codegen
