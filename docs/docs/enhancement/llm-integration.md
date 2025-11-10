# LLM Integration

OpenAPI MCP Codegen integrates with leading LLM providers to enhance both MCP server and A2A agent generation with AI-powered intelligence.

## Core LLM Features

### 1. System Prompt Generation
Generate domain-specific AI prompts optimized for API interactions:

```bash
uvx openapi_mcp_codegen generate-mcp \
  --spec-file api.json \
  --generate-system-prompt
```

### 2. Enhanced Docstring Generation
Improve function documentation for better AI agent comprehension:

```bash
uvx openapi_mcp_codegen generate-mcp \
  --spec-file api.json \
  --enhance-docstring-with-llm
```

### 3. A2A Agent Intelligence
Generate intelligent agent configurations with skills and capabilities:
- **Skills Definition**: AI-generated capability descriptions
- **Agent Prompts**: Domain-specific system prompts for A2A agents
- **Example Generation**: Contextual usage examples

## Supported LLM Providers

### OpenAI
- **Models**: GPT-4, GPT-4o, GPT-3.5-turbo
- **Configuration**: Set `OPENAI_API_KEY` environment variable
- **Endpoint**: Configurable via `OPENAI_ENDPOINT`

### Anthropic
- **Models**: Claude-3-5-Sonnet, Claude-3-Haiku
- **Configuration**: Set `ANTHROPIC_API_KEY` environment variable
- **Provider**: Set `LLM_PROVIDER=anthropic`

## LLM Enhancement Benefits

- **Better Tool Selection**: AI-optimized descriptions improve agent tool discovery
- **Contextual Intelligence**: Generated prompts understand specific API domains
- **Production Ready**: All enhancements maintain code quality and type safety
- **Fallback Support**: Graceful degradation when LLM services unavailable

## Configuration

```bash
# OpenAI
export OPENAI_API_KEY=sk-...
export LLM_PROVIDER=openai
export OPENAI_MODEL_NAME=gpt-4o

# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...
export LLM_PROVIDER=anthropic
export ANTHROPIC_MODEL_NAME=claude-3-5-sonnet-20241022
```

*Documentation in progress. See [prompt configuration](./prompt-configuration.md) for detailed prompt engineering.*
