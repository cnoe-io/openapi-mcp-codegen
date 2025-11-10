# OpenAPI Enhancement (Future Proposal)

OpenAPI MCP Codegen focuses on **MCP Server Generation** and **A2A Agent Generation**. OpenAPI enhancement capabilities are considered for future development.

## Current Focus: Core Generation

The tool's primary capabilities are:

### 1. MCP Server Generation
Transform OpenAPI specifications into production-ready MCP servers:
- Type-safe Python code with async/await support
- Smart parameter handling for complex schemas
- Generated tool modules for each API endpoint
- Optional LangGraph agent wrappers

### 2. A2A Agent Generation
Create standalone agents that connect to external MCP servers:
- Complete A2A-compatible agent packages
- Skills-based architecture with capability definitions
- Protocol bindings for different transports
- AgentGateway integration ready

## LLM Enhancement Features

Both generation modes support LLM-powered intelligence:
- **System Prompt Generation**: AI-optimized prompts for specific domains
- **Enhanced Docstrings**: Better function descriptions for AI agent comprehension
- **Evaluation Frameworks**: Testing suites for agent performance measurement

## Future Enhancement Proposal

OpenAPI specification enhancement using overlay specifications is documented as a future proposal in [ADR-008: OpenAPI Enhancement Proposal](../adr/ADR-008-openapi-enhancement-proposal.md).

This proposal includes:
- Non-destructive API enhancements using OpenAPI Overlay Specification 1.0.0
- LLM-powered description optimization
- Standards-compliant enhancement workflows
- Version-controlled enhancement specifications

## Getting Started with Core Features

To use the current core capabilities:

```bash
# Generate MCP server
uvx openapi_mcp_codegen generate-mcp \
  --spec-file your-api.json \
  --generate-agent \
  --generate-system-prompt

# Generate A2A agent
uvx openapi_mcp_codegen generate-a2a-agent-with-remote-mcp \
  --spec-file your-api.json \
  --agent-name "Your Agent" \
  --mcp-server-url "http://agentgateway:3000"
```

For detailed usage information:
- [Core Components](../core-components/)
- [Basic Usage](../getting-started/basic-usage.md)
- [CLI Commands](../cli/commands.md)
