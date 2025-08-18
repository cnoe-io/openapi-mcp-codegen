# Example environment variables for {{ mcp_name | capitalize }} agent

# URL of the backend service this MCP server will access
{{ mcp_name | upper }}_API_URL=https://api.example.com

# Authentication token / key for the service
{{ mcp_name | upper }}_TOKEN=PASTE_YOUR_TOKEN_HERE

# Langfuse (observability) configuration
LANGFUSE_PUBLIC_KEY=pk-lf-local
LANGFUSE_SECRET_KEY=sk-lf-local
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_TRACING_ENABLED=True
# Optional debug
# LANGFUSE_DEBUG=True
