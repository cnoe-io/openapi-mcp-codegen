# Argo Workflows - MCP Server + A2A Agent

This directory contains both components for the Argo Workflows integration:

## Components

### 1. `mcp_argo_workflows/` - MCP Server
- **Purpose**: Streamable HTTP MCP server that wraps Argo Workflows API
- **Protocol**: Model Context Protocol (MCP) over HTTP
- **Generated from**: `argo-workflows-openapi-unedited.json`

### 2. `agent_argo_workflows/` - A2A Agent
- **Purpose**: Agent-to-Agent (A2A) protocol agent
- **Uses**: `cnoe-agent-utils` base classes (LangGraph + A2A integration)
- **Connects to**: MCP server via streamable_http
- **Protocol**: A2A over WebSocket/HTTP

## Architecture

```
┌─────────────────┐    HTTP/MCP     ┌─────────────────┐    HTTP API   ┌─────────────────┐
│  A2A Agent      │ ──────────────> │  MCP Server     │ ─────────────> │ Argo Workflows │
│ agent_argo_     │                 │ mcp_argo_       │               │ API Server      │
│ workflows       │                 │ workflows       │               │                 │
└─────────────────┘                 └─────────────────┘               └─────────────────┘
```

## Generation Commands

### Generate MCP Server
```bash
cd /path/to/openapi-mcp-codegen
python -m openapi_mcp_codegen generate-mcp \
  --spec-file examples/argo-workflows.bk/argo-workflows-openapi-unedited.json \
  --output-dir examples/argo-workflows/mcp_argo_workflows
```

### Generate A2A Agent
```bash
python -m openapi_mcp_codegen generate-a2a-agent \
  --spec-file examples/argo-workflows.bk/argo-workflows-openapi-unedited.json \
  --agent-name argo_workflows \
  --mcp-server-url http://localhost:3000 \
  --output-dir examples/argo-workflows/agent_argo_workflows
```

## Usage

1. **Start MCP Server**: `cd mcp_argo_workflows && make run`
2. **Start A2A Agent**: `cd agent_argo_workflows && make run-a2a`

The A2A agent will connect to the MCP server via HTTP and expose an A2A WebSocket interface.