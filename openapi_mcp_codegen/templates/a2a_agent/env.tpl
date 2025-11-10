# {{ agent_display_name }} A2A Agent Environment Configuration
# Generated: {{ timestamp }}

# =============================================================================
# A2A AGENT CONFIGURATION
# =============================================================================

# A2A Server host and port
# These can be overridden via command line: --host <host> --port <port>
A2A_HOST=localhost
A2A_PORT=10000

# Legacy agent-specific host and port (kept for compatibility)
{{ agent_name.upper() }}_AGENT_HOST=localhost
{{ agent_name.upper() }}_AGENT_PORT=8000

# A2A Transport Configuration
# Options: p2p, slim
A2A_TRANSPORT=p2p

# SLIM endpoint (only needed if A2A_TRANSPORT=slim)
SLIM_ENDPOINT=http://slim-dataplane:46357

# CORS configuration for A2A HTTP server
# CORS_ORIGINS=*                                   # Allow all origins (default, use with caution in production)
# CORS_ORIGINS=http://localhost:3000,http://localhost:8080  # Specific origins (comma-separated, recommended for production)
# CORS_METHODS=*                                   # Allow all methods (default)
# CORS_METHODS=GET,POST,PUT,DELETE                 # Specific methods (comma-separated)
# CORS_HEADERS=*                                   # Allow all headers (default)
# CORS_HEADERS=Content-Type,Authorization,X-Requested-With  # Specific headers (comma-separated)
# CORS_CREDENTIALS=false                           # Allow credentials (default: false)

# =============================================================================
# MCP SERVER CONFIGURATION
# =============================================================================

# MCP Server URL (AgentGateway or other MCP server)
MCP_SERVER_URL={{ mcp_server_url }}

# MCP Server host and port (for running MCP server locally)
MCP_HOST=localhost
MCP_PORT=3000

# =============================================================================
# LLM PROVIDER CONFIGURATION
# =============================================================================

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o

# Anthropic Configuration
ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Google AI Configuration
GOOGLE_AI_API_KEY=your-google-ai-api-key-here
GOOGLE_AI_MODEL=gemini-1.5-pro

# Azure OpenAI Configuration (alternative to OpenAI)
# AZURE_OPENAI_API_KEY=your-azure-openai-key
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_VERSION=2024-02-15-preview
# AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# =============================================================================
# LOGGING & DEBUGGING
# =============================================================================

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Enable debug mode
DEBUG=false

# =============================================================================
# DEVELOPMENT SETTINGS
# =============================================================================

# Development mode
DEVELOPMENT=true

# Disable SSL verification (for development only)
SSL_VERIFY=true

# =============================================================================
# AGENT-SPECIFIC CONFIGURATION
# =============================================================================

# {{ agent_display_name }} specific settings
# Add any service-specific environment variables here

# SSL Configuration for {{ agent_display_name }} API
{{ mcp_name.upper() }}_VERIFY_SSL=true
# {{ mcp_name.upper() }}_CA_BUNDLE=/path/to/ca-bundle.pem

# Example: API timeouts
API_TIMEOUT=30

# Example: Request retries
MAX_RETRIES=3

# Example: Custom headers or authentication
# SERVICE_API_KEY=your-service-api-key
# CUSTOM_HEADER_VALUE=your-custom-value
