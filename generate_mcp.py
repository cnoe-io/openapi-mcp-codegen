#!/usr/bin/env python3
"""
Script to generate an MCP server from an OpenAPI specification
"""

import os
from mcp_generator import MCPGenerator

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the OpenAPI spec
    spec_path = os.path.join(script_dir, 'openapi.json')
    
    # Output directory for the generated MCP server
    output_dir = os.path.join(script_dir, 'generated_mcp')
    
    # Create the generator and generate the MCP server
    generator = MCPGenerator(spec_path, output_dir)
    generator.generate()
    
    print(f"Generated MCP server in {output_dir}")
    print("\nNext steps:")
    print("1. cd generated_mcp")
    print("2. cp .env.example .env")
    print("3. Edit .env with your API credentials")
    print("4. poetry install")
    print("5. poetry run python -m server")

if __name__ == '__main__':
    main() 