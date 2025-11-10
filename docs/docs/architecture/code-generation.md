# Code Generation

The code generation engine transforms enhanced OpenAPI specifications into production-ready Python MCP servers.

## Template System

- **Jinja2-based**: Flexible template rendering with full Python integration
- **Type Mapping**: OpenAPI types to Python type hints
- **Modular Structure**: Separate templates for tools, clients, and documentation

## Generated Components

- **MCP Server**: FastMCP-based server implementation
- **API Client**: httpx-based async HTTP client
- **Tool Modules**: Individual modules for each API endpoint
- **Type Definitions**: Comprehensive type hints and validation

## Code Quality

- **Ruff Formatting**: Automatically formatted and linted code
- **Error Handling**: Comprehensive error handling and logging
- **Documentation**: Auto-generated docstrings and README files

For implementation details, see the templates in `openapi_mcp_codegen/templates/`.
