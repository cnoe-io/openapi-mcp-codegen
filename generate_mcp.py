#!/usr/bin/env python3
"""
Script to generate an MCP server from an OpenAPI specification
"""

import os
import json
import yaml
from mcp_generator import MCPGenerator

def load_spec(spec_path):
    """Load the OpenAPI spec from either JSON or YAML file"""
    with open(spec_path, 'r') as f:
        if spec_path.endswith('.yaml') or spec_path.endswith('.yml'):
            return yaml.safe_load(f)
        else:
            return json.load(f)

def get_mcp_name(spec_path):
    """Get the MCP name from the OpenAPI spec"""
    spec = load_spec(spec_path)
    # Get the first word from the title and append _mcp
    title = spec.get('info', {}).get('title', 'generated')
    base_name = title.split()[0].lower()  # Take first word and convert to lowercase
    return f"{base_name}_mcp"

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the OpenAPI spec - can be either JSON or YAML
    spec_path = os.path.join(script_dir, 'openapi_backstage.yaml')
    
    # Get MCP name from spec
    mcp_name = get_mcp_name(spec_path)
    
    # Output directory for the generated MCP server
    output_dir = os.path.join(script_dir, mcp_name)    
    
    # Create the generator and generate the MCP server
    generator = MCPGenerator(spec_path, output_dir)
    generator.generate()
    
    print(f"Generated MCP server in {output_dir}")
    print("\nNext steps:")
    print(f"1. cd {mcp_name}")
    print("2. cp .env.example .env")
    print("3. Edit .env with your API credentials")
    print("4. poetry install")
    print("5. poetry run python -m server")

if __name__ == '__main__':
    main() 