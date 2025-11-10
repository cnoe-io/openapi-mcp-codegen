# Backstage Example

Backstage API integration for developer portal and catalog operations.

## Overview

- **API**: Backstage Developer Portal API
- **Features**: Catalog management, plugin architecture, entity operations
- **Use Cases**: Platform engineering, developer productivity

## Generation

```bash
cd examples/backstage
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file openapi.yaml \
  --output-dir mcp_server
```

*Example documentation in progress. See `examples/backstage/` directory for current implementation.*
