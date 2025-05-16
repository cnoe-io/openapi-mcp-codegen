#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
Script to generate an MCP server from an OpenAPI specification
"""

import os
import json
import yaml
import click
from openapi_mcp_codegen.mcp_codegen import MCPGenerator

def load_spec(spec_path):
    """Load the OpenAPI spec from either JSON or YAML file"""
    with open(spec_path, 'r', encoding='utf-8') as f:
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

@click.command(short_help="OpenAPI MCP Code Generator")
@click.option(
  "--spec-file",
  type=click.Path(exists=True, dir_okay=False, readable=True),
  required=True,
  help="Path to the OpenAPI spec file (YAML or JSON).",
)
@click.option(
  "--output-dir",
  type=click.Path(file_okay=False, writable=True),
  default=None,
  help="Directory to output the generated MCP server (default: <script_dir>/<mcp_name>).",
)
@click.option(
  "--dryrun",
  is_flag=True,
  default=False,
  help="Show what would be generated without writing files.",
)
@click.option(
    "--log-level",
    type=click.Choice(["critical", "error", "warning", "info", "debug"], case_sensitive=False),
    default="info",
    show_default=True,
    help="Set logging level.",
  )
def main(log_level, spec_file, output_dir, dryrun):
  # Get the directory of this script
  script_dir = os.path.dirname(os.path.abspath(__file__))

  # Path to the OpenAPI spec - can be either JSON or YAML
  spec_path = spec_file

  # Get MCP name from spec
  mcp_name = get_mcp_name(spec_path)

  # Output directory for the generated MCP server
  if output_dir is None:
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