# Examples

## Available Examples

### Petstore API
- **Location**: `examples/petstore/`
- **Description**: Simple REST API for pet store operations
- **Features**: Basic CRUD operations, straightforward schema

### Argo Workflows
- **Location**: `examples/argo-workflows/`
- **Description**: Complex Kubernetes-native workflow engine API
- **Features**: 255 operations, complex nested schemas, production usage

### Splunk API
- **Location**: `examples/splunk/`
- **Description**: Enterprise observability and analytics platform
- **Features**: Large API surface, authentication patterns

### Backstage API
- **Location**: `examples/backstage/`
- **Description**: Developer portal and platform engineering tool
- **Features**: Plugin architecture, catalog operations

## Running Examples

Each example includes a complete setup:

```bash
cd examples/petstore
make generate-enhanced
make validate
make run-mcp-server
```

For detailed walkthroughs, see the individual example documentation.
