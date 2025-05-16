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
from tools import pet
from tools import pet_findByStatus
from tools import pet_findByTags
from tools import store_inventory
from tools import store_order
from tools import user
from tools import user_createWithList
from tools import user_login
from tools import user_logout

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
if __name__ == "__main__":
    mcp.run()
