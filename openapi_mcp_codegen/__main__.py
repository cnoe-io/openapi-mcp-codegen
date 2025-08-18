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
import dotenv
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
    "--log-level",
    type=click.Choice(["critical", "error", "warning", "info", "debug"], case_sensitive=False),
    default="info",
    show_default=True,
    help="Set logging level.",
  )
@click.option(
    "--generate-agent",
    is_flag=True,
    default=False,
    help="Generate a LangGraph React-agent wrapper that uses the produced MCP server.",
)
@click.option(
    "--generate-eval",
    is_flag=True,
    default=False,
    help="Generate a module that evaluates the generated agent given eval/dataset.yaml.",
)
@click.option(
    "--generate-system-prompt",
    is_flag=True,
    default=False,
    help="Generate the SYSTEM prompt for the agent using an LLM "
         "(requires LLM env vars such as OPENAI_API_KEY, ANTHROPIC_API_KEY, …).",
)
@click.option(
      "--with-a2a-proxy",
      is_flag=True,
      default=False,
      help="Also generate a minimal WebSocket upstream server; deploy the external a2a-proxy to expose an A2A HTTP API.",
  )
@click.option(
  "--dry-run",
  is_flag=True,
  default=False,
  help="Run the generator in dry-run mode without writing files.",
)
@click.option(
  "--enhance-docstring-with-llm",
  is_flag=True,
  default=False,
  help="Enhance generated docstrings using an LLM.",
)
@click.option(
  "--enhance-docstring-with-llm-openapi",
  is_flag=True,
  default=False,
  help="Enhance generated docstrings using an LLM and add OpenAPI spec to docstring.",
)
def main(
   log_level,
   spec_file,
   output_dir,
   dry_run,
   enhance_docstring_with_llm,
   enhance_docstring_with_llm_openapi,
   generate_agent,
   generate_eval,
   generate_system_prompt,
   with_a2a_proxy,
):
  # Load environment variables from .env file if present
  env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
  if os.path.exists(env_path):
    dotenv.load_dotenv(env_path)
  # Get the directory of this script
  script_dir = os.path.dirname(os.path.abspath(__file__))

  # Path to the OpenAPI spec - can be either JSON or YAML
  spec_path = spec_file

  # Get MCP name from spec
  mcp_name = get_mcp_name(spec_path)

  # Output directory for the generated MCP server
  if output_dir is None:
    output_dir = os.path.join(script_dir, mcp_name)

  spec_dir = os.path.dirname(spec_path)
  config_path = os.path.join(spec_dir, 'config.yaml')
  print(f"Using configuration file: {config_path}")
  if not os.path.exists(config_path):
    raise FileNotFoundError(f"Configuration file not found: {config_path}")
  # Create the generator and generate the MCP server
  generator = MCPGenerator(
      script_dir=script_dir,
      spec_path=spec_path,
      output_dir=output_dir,
      config_path=config_path,
      dry_run=dry_run,
      enhance_docstring_with_llm=enhance_docstring_with_llm,
      enhance_docstring_with_llm_openapi=enhance_docstring_with_llm_openapi,
      generate_agent=generate_agent,
      generate_eval=generate_eval,
      generate_system_prompt=generate_system_prompt,
      with_a2a_proxy=with_a2a_proxy,
  )
  generator.generate()

  print(f"🎉 Generated MCP server in {output_dir}")
  print("\n🚀 Next steps:")
  print(f"\n1️⃣ Navigate to the generated directory: `cd {mcp_name}`")
  print("\n2️⃣ Copy the example environment file: `cp .env.example .env`")
  print("\n3️⃣ ✏️ Edit `.env` with your API credentials")
  print("\n4️⃣ 📦 Install dependencies: `poetry install`")
  print("\n5️⃣ ▶️ Start the server: `poetry run python -m server`\n")

if __name__ == '__main__':
    main()
