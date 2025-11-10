# Argo Workflows Example

The Argo Workflows example showcases complex API handling with LLM enhancements and demonstrates production-ready capabilities.

## Overview

- **API**: Argo Workflows v3.5+ (255 operations)
- **Size**: 771KB OpenAPI specification
- **Complexity**: Kubernetes-style nested schemas
- **Features**: Smart parameter handling, LLM enhancement, AgentGateway integration

## Enhanced Generation

```bash
cd examples/argo-workflows
export OPENAI_API_KEY=your-key-here

# Generate with LLM enhancements
make generate-enhanced

# Validate specification
make validate

# Generate AgentGateway config
make generate-agw-config
```

## Key Demonstrations

### Smart Parameter Handling
- **Before**: 5,735-line function with 1,000+ parameters
- **After**: 82-line function with 7 clean parameters
- **Result**: 98.6% code size reduction

### LLM Enhancement
- **511 overlay actions** generated automatically
- **OpenAI-compatible descriptions** under 300 characters
- **"Use when:" patterns** for better AI comprehension

### Production Features
- **AgentGateway integration** for HTTP proxy
- **Comprehensive validation** and error handling
- **Zero-touch maintenance** via GitHub Actions

## Architecture Impact

This example validates the core architecture decisions documented in [ADR-001](../adr/ADR-001-openapi-mcp-architecture.md) with real-world metrics and production usage at Cisco's Jarvis platform.

For complete setup instructions, see `examples/argo-workflows/README.md`.
