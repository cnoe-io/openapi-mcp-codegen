# LLM Integration

OpenAPI MCP Codegen integrates with leading LLM providers to generate AI-optimized API documentation.

## Supported Providers

### OpenAI
- **Models**: GPT-4, GPT-4o, GPT-3.5-turbo
- **Configuration**: Set `OPENAI_API_KEY` environment variable
- **Endpoint**: Configurable via `OPENAI_ENDPOINT`

### Anthropic
- **Models**: Claude-3-5-Sonnet, Claude-3-Haiku
- **Configuration**: Set `ANTHROPIC_API_KEY` environment variable
- **Provider**: Set `LLM_PROVIDER=anthropic`

## Enhancement Features

- **Contextual Descriptions**: Generate "Use when:" patterns for better AI comprehension
- **OpenAI Compatibility**: Descriptions under 300 characters for function calling
- **Plain Text Format**: No markdown or special formatting
- **Fallback Support**: Rule-based enhancement when LLM unavailable

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
