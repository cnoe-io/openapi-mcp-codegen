# Example environment variables for {{ mcp_name | capitalize }} agent

# URL of the backend service this MCP server will access
{{ mcp_name | upper }}_API_URL=https://api.example.com

# Authentication token / key for the service
{{ mcp_name | upper }}_TOKEN=PASTE_YOUR_TOKEN_HERE

# A2A Agent server configuration
A2A_HOST=0.0.0.0
A2A_PORT=8000

# MCP Server configuration (for local MCP server)
MCP_HOST=localhost
MCP_PORT=3000

# CORS configuration for A2A HTTP server
# CORS_ORIGINS=*                                   # Allow all origins (default, use with caution in production)
# CORS_ORIGINS=http://localhost:3000,http://localhost:8080  # Specific origins (comma-separated, recommended for production)
# CORS_METHODS=*                                   # Allow all methods (default)
# CORS_METHODS=GET,POST,PUT,DELETE                 # Specific methods (comma-separated)
# CORS_HEADERS=*                                   # Allow all headers (default)
# CORS_HEADERS=Content-Type,Authorization,X-Requested-With  # Specific headers (comma-separated)
# CORS_CREDENTIALS=false                           # Allow credentials (default: false)

# Langfuse (observability) configuration
LANGFUSE_PUBLIC_KEY=pk-lf-local
LANGFUSE_SECRET_KEY=sk-lf-local
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_TRACING_ENABLED=True
# Optional debug
# LANGFUSE_DEBUG=True
