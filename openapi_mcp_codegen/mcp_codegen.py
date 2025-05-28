#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

import os
import json
import yaml
import logging
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
import subprocess
from pprint import pprint

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp_codegen")

class MCPGenerator:
  """
  MCPGenerator is a class responsible for generating Python code based on OpenAPI specifications.
  It utilizes Jinja2 templates to create various components such as models, API clients, tools,
  and server files. The generated code is structured and organized to facilitate the development
  of Microservice Control Plane (MCP) applications.

  Attributes:
    script_dir (str): Directory containing Jinja2 templates used for code generation.
    spec_path (str): Path to the OpenAPI specification file (YAML or JSON format).
    output_dir (str): Directory where the generated code will be stored.
    config_path (str): Path to the configuration file containing metadata and settings.
    env (Environment): Jinja2 environment for loading and rendering templates.
    config (dict): Configuration data loaded from the configuration file.
    spec (dict): Parsed OpenAPI specification loaded from the spec file.
    mcp_name (str): Name of the MCP derived from the OpenAPI specification title.
    src_output_dir (str): Directory for storing the generated MCP source code.

  Methods:
    __init__(script_dir, spec_path, output_dir, config_path):
      Initializes the MCPGenerator instance with paths and configuration data.

    _load_spec():
      Loads and parses the OpenAPI specification file into a dictionary.

    render_template(template_name, output_path, **kwargs):
      Renders a Jinja2 template and writes the output to a specified file.

    _get_python_type(prop):
      Maps OpenAPI property types to corresponding Python types.

    run_ruff_lint(input_file):
      Runs Ruff linting with auto-fix enabled on a specified file.

    get_file_header_kwargs():
      Retrieves file header configuration from the configuration file.

    generate_model_base():
      Generates the base model file for the MCP application.

    generate_models():
      Generates Python model files based on OpenAPI schemas.

    generate_api_client():
      Generates the API client file for interacting with the MCP server.

    generate_tool_modules():
      Generates tool modules based on OpenAPI paths and operations.

    generate_server():
      Generates the server file for the MCP application.

    generate_pyproject():
      Generates the pyproject.toml file for the MCP application.

    generate_env():
      Generates the .env.example file for environment variable configuration.

    generate_readme():
      Generates the README.md file for the MCP application.

    generate_init_files():
      Generates __init__.py files for all directories in the MCP application.

    generate():
      Executes the entire code generation process, creating all components based on the OpenAPI specification and templates.

  Usage:
    The MCPGenerator class is designed to be instantiated with the required paths and configuration file.
    Once initialized, the `generate()` method can be called to produce all necessary components for the MCP application.
  """

  def __init__(self, script_dir: str, spec_path: str, output_dir: str, config_path: str):
    """
    Initialize the MCPGenerator with paths and configuration.

    Args:
      script_dir (str): Directory containing the templates.
      spec_path (str): Path to the OpenAPI specification file.
      output_dir (str): Directory where generated code will be stored.
      config_path (str): Path to the configuration file.
    """
    logger.info("Initializing MCPGenerator")
    self.script_dir = script_dir
    self.spec_path = spec_path
    self.output_dir = output_dir
    self.env = Environment(loader=FileSystemLoader(os.path.join(script_dir, 'templates')))
    with open(config_path, encoding='utf-8') as f:
      self.config = yaml.safe_load(f)
    self.spec = self._load_spec()
    self.mcp_name = self.spec.get('info', {}).get('title', 'generated_mcp').lower().replace(' ', '_mcp')
    self.src_output_dir = os.path.join(self.output_dir, f'mcp_{self.mcp_name}')
    os.makedirs(self.src_output_dir, exist_ok=True)
    self.tools_map = {}
    logger.debug(f"Initialized MCPGenerator with MCP name: {self.mcp_name}")

  def _load_spec(self) -> Dict[str, Any]:
    """
    Load the OpenAPI specification file.

    Returns:
      dict: Parsed OpenAPI specification.
    """
    logger.info(f"Loading OpenAPI specification from {self.spec_path}")
    with open(self.spec_path, 'r', encoding='utf-8') as f:
      if self.spec_path.endswith(('.yaml', '.yml')):
        spec = yaml.safe_load(f)
      else:
        spec = json.load(f)
    logger.debug(f"Loaded OpenAPI specification: {spec}")
    return spec

  def render_template(self, template_name: str, output_path: str, **kwargs):
    """
    Render a Jinja2 template and write the output to a file.

    Args:
      template_name (str): Name of the template file.
      output_path (str): Path to the output file.
      **kwargs: Additional context variables for the template.
    """
    logger.info(f"Rendering template: {template_name} to {output_path}")
    template = self.env.get_template(template_name)
    logger.debug(f"Template context: {kwargs}")
    rendered = template.render(**kwargs)
    with open(output_path, 'w', encoding='utf-8') as f:
      f.write(rendered)
    logger.info(f"Generated file: {output_path}")

  def _get_python_type(self, prop: Dict[str, Any]) -> str:
    """
    Map OpenAPI property types to Python types.

    Args:
      prop (dict): OpenAPI property definition.

    Returns:
      str: Corresponding Python type.
    """
    t = prop.get("type", "string")
    if t == "integer":
      return "int"
    elif t == "number":
      return "float"
    elif t == "boolean":
      return "bool"
    elif t == "array":
      return f"List[{self._get_python_type(prop.get('items', {}))}]"
    elif t == "object":
      return "Dict[str, Any]"
    return "str"

  def run_ruff_lint(self, input_file: str):
    """
    Run Ruff linting on a file with auto-fix enabled.

    Args:
      input_file (str): Path to the file to lint.
    """
    logger.info(f"Running Ruff lint on {input_file}")
    subprocess.run(["ruff", "check", "--fix", "--ignore", "E402", input_file], check=True)
    logger.info("Ruff linting completed")

  def get_file_header_kwargs(self) -> Dict[str, Any]:
    """
    Retrieve file header configuration from the config file.

    Returns:
      dict: File header configuration.
    """
    file_headers_config = self.config.get("file_headers", {})
    kwargs = {
      "file_headers": bool(file_headers_config),
      "file_headers_copyright": file_headers_config.get("copyright", ""),
      "file_headers_license": file_headers_config.get("license", ""),
      "file_headers_message": file_headers_config.get("message", "")
    }
    logger.debug(f"File header kwargs: {kwargs}")
    return kwargs

  def generate_model_base(self):
    """
    Generate the base model file.
    """
    logger.info("Generating base model")
    path = os.path.join(self.src_output_dir, 'models')
    os.makedirs(path, exist_ok=True)
    file_header_kwargs = self.get_file_header_kwargs()
    self.render_template('models/base_model.tpl', os.path.join(path, 'base.py'), **file_header_kwargs)
    self.run_ruff_lint(os.path.join(path, 'base.py'))

  def generate_models(self):
    """
    Generate model files based on OpenAPI schemas.
    """
    logger.info("Generating models")
    schemas = self.spec.get('components', {}).get('schemas', {})
    for schema_name, schema in schemas.items():
      model_name = ''.join(word.capitalize() for word in schema_name.split('_'))
      fields = []
      required_fields = schema.get('required', [])
      for prop_name, prop in schema.get('properties', {}).items():
        field_type = self._get_python_type(prop)
        fields.append({
          'name': prop_name.replace('.', '_'),
          'type': field_type,
          'description': prop.get('description', ''),
          'required': prop_name in required_fields
        })
      model_path = os.path.join(self.src_output_dir, 'models', f'{schema_name}.py')
      kwargs = self.get_file_header_kwargs()
      kwargs.update({
        'description': schema.get('description', ''),
        'fields': fields,
      })
      self.render_template('models/schema_model.tpl', model_path, model_name=model_name, **kwargs)
      self.run_ruff_lint(model_path)

  def generate_api_client(self):
    """
    Generate the API client file.
    """
    logger.info("Generating API client")
    api_dir = os.path.join(self.src_output_dir, 'api')
    os.makedirs(api_dir, exist_ok=True)
    kwargs = self.get_file_header_kwargs()
    kwargs.update({
      'api_url': "https://api.example.com",
      'api_token': "your_api_key_here",
      'api_headers': self.config.get('headers', {}),
    })
    self.render_template('api/client.tpl', os.path.join(api_dir, 'client.py'), mcp_name=self.mcp_name, **kwargs)
    self.run_ruff_lint(os.path.join(api_dir, 'client.py'))
    self.render_template('init_empty.tpl', os.path.join(api_dir, '__init__.py'))

  def generate_tool_modules(self):
    """
    Generate tool modules based on OpenAPI paths.
    """
    logger.info("Generating tool modules")
    tools_dir = os.path.join(self.src_output_dir, 'tools')
    file_header_kwargs = self.get_file_header_kwargs()
    os.makedirs(tools_dir, exist_ok=True)
    for path, ops in self.spec.get('paths', {}).items():
      if '{' in path:
        continue  # Skip path params for now
      module_name = path.strip('/').replace('/', '_').replace('-', '_') or "root"
      functions = []
      for method, op in ops.items():
        if method.upper() not in ["GET", "POST", "PUT", "DELETE"]:
          continue
        params = []
        for p in op.get("parameters", []):
          if p.get("in") in ["path", "header"]:
            continue
          pname = p.get("name", "param").replace('.', '_')
          ptype = self._get_python_type(p.get("schema", {}))
          if p.get("required"):
            params.append(f"{pname}: {ptype}")
          else:
            params.append(f"{pname}: {ptype} = None")
        functions.append({
          "operation_id": op.get("operationId", f"{method}_{module_name}"),
          "summary": op.get("summary", ""),
          "method": method.upper(),
          "params": params,
          "path": path
        })
      if functions:
        output_path = os.path.join(tools_dir, f"{module_name}.py")
        mcp_server_base_package = self.config.get('mcp_package', {}).get('mcp_server_base_package', '')
        self.render_template(
          "tools/tool.tpl",
          output_path,
          path=path,
          import_path=f"mcp_{self.mcp_name}.api.client",
          mcp_name=self.mcp_name,
          mcp_server_base_package=mcp_server_base_package,
          functions=functions,
          **file_header_kwargs
        )
        self.run_ruff_lint(output_path)
        for function in functions:
          # Get the module name without .py
          stripped_module_name = output_path.split("/")[-1].split(".py")[0]
          # Map the operation_id to the output path
          if stripped_module_name in self.tools_map:
            self.tools_map[stripped_module_name].append(function["operation_id"])
          else:
            self.tools_map[stripped_module_name] = [function["operation_id"]]
    self.render_template(
      "tools/init.tpl",
      os.path.join(tools_dir, '__init__.py'),
      **file_header_kwargs
      )

  def generate_server(self):
    """
    Generate the server file.
    """
    logger.info("Generating server")
    file_header_kwargs = self.get_file_header_kwargs()
    pprint(self.tools_map)
    self.render_template(
      'server.tpl',
      os.path.join(self.src_output_dir, 'server.py'),
      mcp_name=self.mcp_name,
      modules=self.tools_map.keys(),
      registrations=self.tools_map,
      **file_header_kwargs)
    # self.run_ruff_lint(os.path.join(self.src_output_dir, 'server.py'))

  def generate_pyproject(self):
    """
    Generate the pyproject.toml file.
    """
    logger.info("Generating pyproject.toml")
    output_path = os.path.join(self.output_dir, 'pyproject.toml')
    self.render_template(
      'pyproject.tpl',
      output_path,
      name=f"mcp_{self.mcp_name}",
      description=f"Generated MCP server for {self.spec.get('info', {}).get('title', 'API')} from OpenAPI specification",
      author=self.config['author'],
      python_version=self.config['defaults']['python_version'],
      pydantic_version=self.config['defaults']['pydantic_version'],
      mcp_dependency_version=self.config['defaults']['mcp_dependency_version']
    )

  def generate_env(self):
    """
    Generate the .env.example file.
    """
    logger.info("Generating .env.example")
    output_path = os.path.join(self.output_dir, '.env.example')
    self.render_template('env.tpl', output_path)

  def generate_readme(self):
    """
    Generate the README.md file.
    """
    logger.info("Generating README.md")
    output_path = os.path.join(self.output_dir, 'README.md')
    self.render_template(
      'readme.tpl',
      output_path,
      mcp_name=self.mcp_name,
      mcp_description=self.config.get('description', 'Generated MCP server'),
      mcp_version=self.config.get('version', '1.0.0'),
      mcp_author=self.config.get('author', 'CNOE Contributors'),
    )

  def generate_init_files(self):
    """
    Generate __init__.py files for all directories.
    """
    logger.info("Generating __init__.py files")
    file_header_kwargs = self.get_file_header_kwargs()
    self.render_template('init_empty.tpl', os.path.join(self.output_dir, '__init__.py'), **file_header_kwargs)
    self.render_template('init_empty.tpl', os.path.join(self.src_output_dir, '__init__.py'), **file_header_kwargs)
    for subdir in ['api', 'models', 'tools']:
      path = os.path.join(self.src_output_dir, subdir)
      os.makedirs(path, exist_ok=True)
      self.render_template('init_empty.tpl', os.path.join(path, '__init__.py'), **file_header_kwargs)

  def generate(self):
    """
    Generate all components based on the OpenAPI specification and templates.
    """
    logger.info("Starting MCP code generation")
    self.generate_api_client()
    self.generate_model_base()
    self.generate_models()
    self.generate_tool_modules()
    self.generate_server()
    self.generate_init_files()
    self.generate_pyproject()
    self.generate_env()
    self.generate_readme()
    logger.info("MCP code generation completed")