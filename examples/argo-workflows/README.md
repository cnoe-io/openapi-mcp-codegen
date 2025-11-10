# Argo Workflows Example

This example demonstrates OpenAPI MCP Codegen with the Argo Workflows API, showcasing complex API handling and LLM enhancement capabilities.

## Quick Start

1. **Generate Enhanced MCP Server**:
   ```bash
   # Set your LLM API key for enhancements
   export OPENAI_API_KEY=your-key-here

   # Generate with LLM enhancements
   python -m openapi_mcp_codegen.enhance_and_generate \
       argo-openapi.json \
       mcp_server \
       config.yaml \
       --save-overlay overlay.yaml \
       --save-enhanced-spec enhanced_openapi.json
   ```

2. **Test AgentGateway Integration**:
   ```bash
   # Generate AgentGateway config
   python -m openapi_mcp_codegen.generate_agw_config \
       config.yaml argo-agentgateway.yaml

   # Start AgentGateway
   agentgateway -f argo-agentgateway.yaml
   ```

## Files

- `argo-openapi.json` - Original Argo Workflows OpenAPI specification (771KB, 255 operations)
- `config.yaml` - Configuration for package generation and enhancements
- `argo-agentgateway.yaml` - Pre-generated AgentGateway configuration

## Features Demonstrated

- **Complex API Handling**: 255 operations with nested Kubernetes-style schemas
- **Smart Parameter Handling**: Automatic detection and consolidation of complex parameters
- **LLM Enhancement**: AI-generated descriptions optimized for function calling
- **AgentGateway Integration**: HTTP proxy configuration for web-based AI agents

## Performance Metrics

- **98.6% code size reduction** for complex operations
- **99.3% parameter count reduction** while maintaining functionality
- **OpenAI-compatible descriptions** under 300 characters
- **Production usage** at Cisco's Jarvis platform

## Setup Argo Workflows

To test with a real Argo Workflows instance, see the [Argo Workflows Setup Guide](../../docs/docs/argocon/setup.md) for installation instructions.

## Documentation

For detailed documentation, see the [Argo Workflows example guide](../../docs/docs/examples/argo-workflows.md).
