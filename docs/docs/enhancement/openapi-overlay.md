# OpenAPI Overlay Specification

OpenAPI MCP Codegen uses the industry-standard OpenAPI Overlay Specification 1.0.0 for non-destructive API enhancements.

## What is OpenAPI Overlay?

The OpenAPI Overlay Specification provides a way to update or extend OpenAPI documents without modifying the original specification.

## Benefits

- **Non-destructive**: Original specification remains unchanged
- **Version-controlled**: Overlays can be tracked, reviewed, and collaborated on
- **Reusable**: Same overlay works across different toolchains
- **Standards-compliant**: Industry-standard approach

## Overlay Structure

```yaml
overlay: 1.0.0
info:
  title: API Enhancements
  version: 1.0.0

actions:
  - target: $.paths['/api/v1/pets'].get.description
    update: "Enhanced description with AI context"
```

## Generated Overlays

Our LLM enhancement pipeline automatically generates overlays with:
- AI-optimized operation descriptions
- Enhanced parameter documentation
- OpenAI-compatible formatting
- Use case context patterns

For specification details, see the [official OpenAPI Overlay Specification](https://github.com/OAI/Overlay-Specification).
