{% if file_headers %}
# {{ file_headers_copyright }}
# {{ file_headers_license }}
# {{ file_headers_message }}
{% endif %}
#!/usr/bin/env python3
"""
{{ title }} MCP Server

This server provides a Model Context Protocol (MCP) interface to the {{ title }},
allowing large language models and AI assistants to interact with the service.
"""
import logging
import os
from dotenv import load_dotenv
from fastmcp import FastMCP

{% for module in modules %}
from {{ mcp_package }}mcp_{{ mcp_name }}.tools import {{ module }}
{% endfor %}

def main():
    # Load environment variables
    load_dotenv()

    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    # Get MCP configuration from environment variables
    MCP_MODE = os.getenv("MCP_MODE", "stdio").lower()

    # Get host and port for server
    MCP_HOST = os.getenv("MCP_HOST", "localhost")
    MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

    logging.info(f"Starting MCP server in {MCP_MODE} mode on {MCP_HOST}:{MCP_PORT}")

    # Get agent name from environment variables
    AGENT_NAME = os.getenv("AGENT_NAME", "{{ mcp_name | upper }} Agent")
    logging.info(f"Agent name: {AGENT_NAME}")

    # Create server instance
    if MCP_MODE in ["SSE", "HTTP"]:
      mcp = FastMCP(f"{AGENT_NAME} MCP Server", host=MCP_HOST, port=MCP_PORT)
    else:
      mcp = FastMCP("{{ mcp_name | upper }} MCP Server")

{% for module, ops in registrations.items() %}
    # Register {{ module }} tools
{% for op in ops %}
    mcp.tool()({{ module }}.{{ op | replace('{', '') | replace('}', '') }})
{% endfor %}{% endfor %}

    # Run the MCP server
    mcp.run(transport=MCP_MODE)

if __name__ == "__main__":
    main()
