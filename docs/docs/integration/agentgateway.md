# AgentGateway Integration

AgentGateway provides HTTP proxy functionality for MCP servers, enabling web-based AI agent integration.

## What is AgentGateway?

AgentGateway is a high-performance proxy that exposes OpenAPI specifications as MCP endpoints, allowing AI agents to interact with REST APIs through a standardized interface.

## Auto-Generated Configuration

The generator creates AgentGateway configuration directly from `config.yaml`:

```yaml
# Generated agw.yaml
binds:
- port: 3000
  listeners:
  - routes:
    - policies:
        cors:
          allowOrigins: ["*"]
          allowHeaders: ["*"]
      backends:
      - mcp:
          targets:
          - name: openapi
            openapi:
              schema:
                file: enhanced_openapi.json
              host: localhost
              port: 2746
              path: /
```

## Deployment

```bash
# Generate AgentGateway config
make generate-agw-config

# Start AgentGateway
make run-agentgateway

# AgentGateway available at http://localhost:3000
```

## Benefits

- ✅ **Zero Configuration**: Auto-generated from existing settings
- ✅ **Instant Deployment**: Start serving MCP endpoints immediately
- ✅ **Validated Specs**: Only compliant OpenAPI 3.x specs are used
- ✅ **Production Ready**: CORS, error handling, and logging configured

*AgentGateway documentation in progress. See examples for working configurations.*
