# Splunk Example

Splunk API integration example demonstrating enterprise-scale API handling.

## Overview

- **API**: Splunk Enterprise REST API
- **Scale**: Large enterprise API surface
- **Features**: Authentication patterns, search operations, data management

## Generation

```bash
cd examples/splunk
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file openapi.json \
  --output-dir mcp_server \
  --generate-agent
```

*Example documentation in progress. See `examples/splunk/` directory for current implementation.*
