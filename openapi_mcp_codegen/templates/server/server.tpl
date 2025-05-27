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
from mcp.server.fastmcp import FastMCP

{% for module in modules %}
from mcp_{{ base_name }}.tools import {{ module }}
{% endfor %}

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

mcp = FastMCP("{{ title }} MCP Server")

{% for module, ops in registrations.items() %}
# Register {{ module }} tools
{% for op in ops %}
mcp.tool()({{ module }}.{{ op }})
{% endfor %}
{% endfor %}

def main():
    mcp.run()

if __name__ == "__main__":
    main()
