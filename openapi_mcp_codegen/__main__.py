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
from openapi_mcp_codegen.a2a_agent_codegen import A2AAgentGenerator

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
      "--enable-slim",
      is_flag=True,
      default=False,
      help="Enable SLIM transport for the agent A2A server (requires agntcy_app_sdk).",
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
   enable_slim,
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
      enable_slim=enable_slim,
  )
  generator.generate()

  print(f"🎉 Generated MCP server in {output_dir}")
  print("\n🚀 See the README.md to continue")


@click.command(short_help="Generate A2A agent for remote MCP server")
@click.option(
  "--spec-file",
  type=click.Path(exists=True, dir_okay=False, readable=True),
  required=True,
  help="Path to the OpenAPI spec file (YAML or JSON) - used to understand API capabilities.",
)
@click.option(
  "--agent-name",
  type=str,
  required=True,
  help="Name of the agent (e.g., 'argo_workflows'). Will be sanitized for use as Python package name.",
)
@click.option(
  "--mcp-server-url",
  type=str,
  required=True,
  help="URL of the external MCP server (e.g., 'http://localhost:3000')",
)
@click.option(
  "--output-dir",
  type=click.Path(file_okay=False, writable=True),
  default=None,
  help="Directory to output the generated A2A agent (default: ./agent_<agent_name>).",
)
@click.option(
  "--agent-description",
  type=str,
  default=None,
  help="Description of the agent (default: auto-generated from agent name).",
)
@click.option(
  "--dry-run",
  is_flag=True,
  default=False,
  help="Run the generator in dry-run mode without writing files.",
)
def generate_a2a_agent_with_remote_mcp(
   spec_file,
   agent_name,
   mcp_server_url,
   output_dir,
   agent_description,
   dry_run,
):
  """Generate a standalone A2A agent that connects to an external MCP server."""

  # Load environment variables from .env file if present
  env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
  if os.path.exists(env_path):
    dotenv.load_dotenv(env_path)

  # Get the directory of this script
  script_dir = os.path.dirname(os.path.abspath(__file__))

  # Path to the OpenAPI spec
  spec_path = spec_file

  # Sanitize agent name
  sanitized_name = agent_name.lower().replace(' ', '_').replace('-', '_')

  # Output directory for the generated A2A agent
  if output_dir is None:
    output_dir = f"./agent_{sanitized_name}"

  # Check if config file exists for the spec
  spec_dir = os.path.dirname(spec_path)
  config_path = os.path.join(spec_dir, 'config.yaml')

  # Create a minimal config if it doesn't exist
  if not os.path.exists(config_path):
    print(f"Creating minimal config file: {config_path}")
    config_data = {
      'title': agent_name,
      'author': 'Generated User',
      'author_email': 'user@example.com',
      'timestamp': '2025-01-01T00:00:00Z'
    }
    os.makedirs(spec_dir, exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
      yaml.dump(config_data, f, default_flow_style=False)

  print(f"Using configuration file: {config_path}")

  # Create the A2A agent generator
  generator = A2AAgentGenerator(
      script_dir=script_dir,
      spec_path=spec_path,
      output_dir=output_dir,
      config_path=config_path,
      dry_run=dry_run,
  )

  # Generate the A2A agent
  agent_output_dir = generator.generate_a2a_agent(
      agent_name=agent_name,
      mcp_server_url=mcp_server_url,
      agent_description=agent_description
  )

  print(f"🎉 Generated A2A agent '{agent_name}' in {agent_output_dir}")
  print(f"🔗 Connects to MCP server: {mcp_server_url}")
  print(f"\n🚀 To run the agent:")
  print(f"   cd {agent_output_dir}")
  print(f"   make dev        # Setup environment")
  print(f"   make run-a2a    # Start the agent")


@click.command(short_help="Validate generated MCP functions")
@click.option(
  "--project-root",
  type=click.Path(exists=True, dir_okay=True, readable=True),
  default=None,
  help="Path to project root directory (default: auto-detected).",
)
@click.option(
  "--verbose", "-v",
  is_flag=True,
  default=False,
  help="Enable verbose logging for detailed validation output.",
)
def validate_functions(project_root, verbose):
    """Validate all generated MCP functions for compliance and quality."""
    
    try:
        from openapi_mcp_codegen.function_validator import FunctionValidator
        from pathlib import Path
        
        # Auto-detect project root if not provided
        if project_root is None:
            project_root = Path(__file__).parent.parent
        else:
            project_root = Path(project_root)
        
        if verbose:
            import logging
            logging.getLogger().setLevel(logging.DEBUG)
            
        print("🔍 Running function validation...")
        print(f"📋 Project root: {project_root}")
        
        validator = FunctionValidator(project_root)
        success = validator.validate_all_projects()
        
        if success:
            print("\n🎉 All function validations passed!")
        else:
            print("\n❌ Function validation failed!")
            print("💡 See details above for specific issues.")
            exit(1)
            
    except ImportError as e:
        print(f"❌ Function validator not available: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Validation error: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        exit(1)


# Create a multi-command CLI
@click.group()
def cli():
    """OpenAPI MCP Code Generator - Generate MCP servers and A2A agents from OpenAPI specs."""
    pass

# Add commands to the group
cli.add_command(main, name="generate-mcp")
cli.add_command(generate_a2a_agent_with_remote_mcp)
cli.add_command(validate_functions)

if __name__ == '__main__':
    # Check if this is being called as a direct command (backward compatibility)
    import sys

    # If first argument is not a subcommand, assume it's the original direct interface
    if len(sys.argv) > 1 and not sys.argv[1] in ['generate-mcp', 'generate-a2a-agent-with-remote-mcp', 'validate-functions']:
        # Call main directly for backward compatibility
        main()
    else:
        # Use the group interface for subcommands
        cli()