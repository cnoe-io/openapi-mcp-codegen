# Enhancement Pipeline

The enhancement pipeline transforms raw OpenAPI specifications into AI-optimized MCP servers using LLM-powered documentation enhancement.

## Pipeline Stages

1. **Analysis**: Parse OpenAPI specification and identify enhancement opportunities
2. **LLM Enhancement**: Generate contextual, AI-friendly descriptions
3. **Overlay Generation**: Create standards-compliant OpenAPI overlay
4. **Application**: Apply enhancements non-destructively to original specification

## Key Features

- OpenAI-compatible descriptions (&lt;300 characters)
- "Use when:" context patterns
- Plain text formatting (no markdown)
- Smart parameter inference for missing schemas

For detailed technical implementation, see [ADR-001: Architecture Overview](../adr/ADR-001-openapi-mcp-architecture.md).
