# AI Agent Integration

Guide for integrating generated MCP servers with various AI agents and platforms.

## MCP Protocol Support

Generated MCP servers are compatible with any MCP-enabled AI agent:

- **Claude Desktop**: Direct MCP server integration
- **Custom Agents**: LangGraph, LangChain, or custom implementations
- **Platform Integration**: Backstage plugins, VS Code extensions

## OpenAI Function Calling

Generated tools are optimized for OpenAI function calling:

```python
import openai
from mcp_petstore.server import get_tool_definitions

# Get OpenAI-compatible tool definitions
tools = get_tool_definitions()

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "List available pets"}],
    functions=tools,
    function_call="auto"
)
```

## LangGraph Integration

The generated agents use LangGraph React patterns for robust tool orchestration and error handling.

*Integration documentation in progress. See examples for working implementations.*
