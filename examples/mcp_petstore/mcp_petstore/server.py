# AUTO-GENERATED CODE - DO NOT MODIFY
# Generated on May 16th using openai_mcp_generator package

#!/usr/bin/env python3
"""
Petstore MCP Server

This server provides a Model Context Protocol (MCP) interface to the Petstore,
allowing large language models and AI assistants to interact with the service.
"""
import logging
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import tools
from mcp_petstore.tools import pet
from mcp_petstore.tools import pet_findByStatus
from mcp_petstore.tools import pet_findByTags
from mcp_petstore.tools import store_inventory
from mcp_petstore.tools import store_order
from mcp_petstore.tools import user
from mcp_petstore.tools import user_createWithList
from mcp_petstore.tools import user_login
from mcp_petstore.tools import user_logout

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create server instance
mcp = FastMCP("Petstore MCP Server")

# Register tools
# Register pet tools
mcp.tool()(pet.updatePet)
mcp.tool()(pet.addPet)

# Register pet_findByStatus tools
mcp.tool()(pet_findByStatus.findPetsByStatus)

# Register pet_findByTags tools
mcp.tool()(pet_findByTags.findPetsByTags)

# Register store_inventory tools
mcp.tool()(store_inventory.getInventory)

# Register store_order tools
mcp.tool()(store_order.placeOrder)

# Register user tools
mcp.tool()(user.createUser)

# Register user_createWithList tools
mcp.tool()(user_createWithList.createUsersWithListInput)

# Register user_login tools
mcp.tool()(user_login.loginUser)

# Register user_logout tools
mcp.tool()(user_logout.logoutUser)


# Start server when run directly
def main():
    mcp.run()

if __name__ == "__main__":
    main()
