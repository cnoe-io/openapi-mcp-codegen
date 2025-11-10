#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

import os
import re
import json
import yaml
import logging
import concurrent.futures
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
from pathlib import Path
import subprocess
import itertools

from cnoe_agent_utils import LLMFactory
from langchain_core.messages import SystemMessage
import textwrap

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp_codegen")

def camel_to_snake(name):
    if name.isupper():
        return "_".join(name).lower()
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    # Replace multiple underscores with a single underscore
    s3 = re.sub(r'_+', '_', s2)
    return s3


def truncate_function_name(name: str, http_method: str = "", used_names: set = None, target_length: int = 30, max_length: int = 64) -> str:
    """
    Truncate function names with consistent service abbreviations and aggressive length limits.
    Always applies service prefix abbreviations for consistency, then applies length-based truncation.
    Adds HTTP method prefix to ensure uniqueness when duplicates would occur.

    Args:
        name: Original function name
        http_method: HTTP method (GET, POST, etc.) to add as prefix if needed for uniqueness
        used_names: Set of already used function names to check for duplicates
        target_length: Target length to aim for (default: 30)
        max_length: Hard limit - anything over this MUST be truncated (default: 64)

    Always applies consistent abbreviations for known service patterns.
    Based on RULE-LLM-LIMITATION-1 from prompt.yaml.
    """
    if used_names is None:
        used_names = set()

    # Always apply consistent service prefix abbreviations first (regardless of length)
    abbreviated = name

    # Known service patterns that should always be abbreviated for consistency
    service_patterns = {
        'workflow_service_': 'wf_svc_',
        'event_source_service_': 'evt_src_svc_',
        'event_service_': 'evt_svc_',
        'sensor_service_': 'sns_svc_',
        'artifact_service_': 'art_svc_',
        'info_service_': 'info_svc_',
        'cluster_workflow_template_service_': 'clust_wf_tpl_svc_',
        'workflow_template_service_': 'wf_tpl_svc_',
        'cron_workflow_service_': 'cron_wf_svc_',
    }

    # Apply service pattern abbreviations
    for full_pattern, abbrev_pattern in service_patterns.items():
        if abbreviated.startswith(full_pattern):
            abbreviated = abbreviated.replace(full_pattern, abbrev_pattern, 1)
            break

    # Continue to HTTP prefix logic even for short names to ensure consistency

    # Log warning for names that will be truncated
    if len(name) > max_length:
        logger.warning(f"Function name '{name}' ({len(name)} chars) exceeds {max_length} hard limit, truncating...")
    else:
        logger.info(f"Function name '{name}' ({len(name)} chars) exceeds {target_length} target, applying abbreviations...")

    # Apply aggressive abbreviation rules for target length
    abbreviations = {
        # Service/System abbreviations
        'service': 'svc',
        'account': 'acct',
        'permissions': 'perms',
        'configuration': 'cfg',
        'template': 'tpl',
        'templates': 'tpls',
        'namespace': 'ns',
        'workflow': 'wf',
        'workflows': 'wfs',
        'archived': 'arch',
        'cluster': 'clust',
        'selector': 'sel',
        'metadata': 'meta',
        'artifact': 'art',
        'artifacts': 'arts',
        'event_source': 'evt_src',
        'event_sources': 'evt_srcs',
        'cron_workflow': 'cron_wf',
        'cron_workflows': 'cron_wfs',
        'sensor': 'sns',
        'sensors': 'snss',
        # Action abbreviations
        'retrieve': 'get',
        'terminate': 'term',
        'resubmit': 'resub',
        'suspend': 'susp',
        'resume': 'res',
        'delete': 'del',
        'create': 'new',
        'update': 'upd',
        'list': 'ls'
    }

    # Remove unnecessary connector words
    connectors_to_remove = ['_all_', '_by_', '_with_', '_and_', '_from_', '_using_']

    abbreviated = name

    # Apply abbreviations
    for full_word, abbrev in abbreviations.items():
        abbreviated = abbreviated.replace(full_word, abbrev)

    # Remove connector words
    for connector in connectors_to_remove:
        abbreviated = abbreviated.replace(connector, '_')

    # Clean up multiple underscores
    abbreviated = re.sub(r'_+', '_', abbreviated)
    abbreviated = abbreviated.strip('_')

    # Apply more aggressive truncation if still over target length
    if len(abbreviated) > target_length:
        parts = abbreviated.split('_')
        if len(parts) > 4:
            # For long functions, keep first part (action) + key middle part + last part
            abbreviated = '_'.join([parts[0], parts[1], parts[-1]])
        elif len(parts) > 3:
            # Keep first 2 and last part
            abbreviated = '_'.join(parts[:2] + parts[-1:])

    # Clean up multiple underscores again after aggressive truncation
    abbreviated = re.sub(r'_+', '_', abbreviated)
    abbreviated = abbreviated.strip('_')

    # ALWAYS add HTTP method prefix at the front for consistency
    final_name = abbreviated
    should_add_prefix = False

    # Check if the function name already starts with an HTTP verb
    starts_with_http_verb = any(final_name.startswith(verb + '_') for verb in [
        'get', 'post', 'put', 'patch', 'del', 'delete', 'head', 'opts', 'options'
    ])

    # Always add HTTP method prefix unless it already starts with one
    if http_method and not starts_with_http_verb:
        should_add_prefix = True
    elif http_method and final_name in used_names:
        # Always add prefix for duplicates even if already has HTTP verb
        should_add_prefix = True

    if should_add_prefix:
        # Add HTTP method prefix
        method_abbrev = {
            "GET": "get",
            "POST": "post",
            "PUT": "put",
            "PATCH": "patch",
            "DELETE": "del",
            "HEAD": "head",
            "OPTIONS": "opts"
        }
        prefix = method_abbrev.get(http_method.upper(), http_method.lower()[:3])

        # Reserve space for prefix + underscore, respecting max_length
        max_base_length = max_length - len(prefix) - 1
        if len(abbreviated) > max_base_length:
            abbreviated = abbreviated[:max_base_length].rstrip('_')

        final_name = f"{prefix}_{abbreviated}"

        if final_name != abbreviated:
            reason = "for consistency" if not (abbreviated in used_names) else "to avoid duplicate"
            logger.info(f"Added method prefix {reason}: '{abbreviated}' → '{final_name}'")

    # Hard limit enforcement - must not exceed max_length
    if len(final_name) > max_length:
        logger.warning(f"Applying hard truncation to enforce {max_length} char limit")
        final_name = final_name[:max_length].rstrip('_')

    # Add to used names set
    used_names.add(final_name)

    logger.info(f"Truncated '{name}' ({len(name)}) → '{final_name}' ({len(final_name)})")
    return final_name

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

  def __init__(
      self,
      script_dir: str,
      spec_path: str,
      output_dir: str,
      config_path: str,
      dry_run: bool = False,
      enhance_docstring_with_llm: bool = False,
      enhance_docstring_with_llm_openapi: bool = False,
      generate_agent: bool = False,
      generate_eval: bool = False,
      generate_system_prompt: bool = False,
      with_a2a_proxy: bool = False,
      enable_slim: bool = False):
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
    self.dry_run = dry_run
    self.should_enhance_docstring_with_llm = enhance_docstring_with_llm
    self.should_enhance_docstring_with_llm_openapi = enhance_docstring_with_llm_openapi
    self.env = Environment(loader=FileSystemLoader(os.path.join(script_dir, 'templates')))
    
    # Add custom filters for MCP compatibility
    def truncate_description(text, max_length=9000):
      """Truncate descriptions to prevent MCP tool registration failures (10024 char limit)"""
      if not text or len(text) <= max_length:
        return text
      # Find a good break point near the limit (end of sentence or paragraph)
      truncated = text[:max_length]
      # Look for sentence endings near the limit
      for break_char in ['. ', '.\n', '\n\n']:
        last_break = truncated.rfind(break_char)
        if last_break > max_length * 0.8:  # Within 80% of limit
          return truncated[:last_break + 1] + "\n\n[Description truncated for MCP compatibility]"
      # Fallback: hard truncate with ellipsis
      return truncated + "...\n\n[Description truncated for MCP compatibility]"
    
    self.env.filters['truncate_description'] = truncate_description
    
    with open(config_path, encoding='utf-8') as f:
      self.config = yaml.safe_load(f)
    self.spec = self._load_spec()
    # Get MCP name from config (title or mcp_name) or fall back to spec title
    raw_name = (
        self.config.get('title') or
        self.config.get('mcp_name') or
        self.spec.get('info', {}).get('title', 'generated_mcp')
    )
    # Sanitize: lowercase, replace spaces and hyphens with underscores
    self.mcp_name = raw_name.lower().replace(' ', '_').replace('-', '_')
    self.src_output_dir = os.path.join(self.output_dir, f'mcp_{self.mcp_name}')
    os.makedirs(self.src_output_dir, exist_ok=True)
    self.tools_map = {}
    self.generate_agent_flag = generate_agent
    self.generate_eval = generate_eval
    self.generate_system_prompt = generate_system_prompt
    self.with_a2a_proxy = with_a2a_proxy
    self.enable_slim = enable_slim
    self.used_function_names = set()  # Track function names to avoid duplicates
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
    with open(output_path, 'w+', encoding='utf-8') as f:
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
    # Resolve component references so nested / referenced enums are visible
    if "$ref" in prop:
        prop = self._resolve_ref(prop["$ref"]) or {}
    # Enumerations -------------------------------------------------------
    if prop.get("enum"):
        enum_vals = prop["enum"]
        # Produce Literal["opt1", "opt2"]  (or ints, bools, …)
        literal_items = ", ".join(repr(v) for v in enum_vals)
        return f"Literal[{literal_items}]"
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
    logger.info(f"Running Ruff format on {input_file}")
    subprocess.run(
      [
      "ruff",
      "format",
      "--line-length",
      "140",
      input_file
      ],
      check=True,
    )
    logger.info(f"Running Ruff lint on {input_file}")
    subprocess.run(
      [
      "ruff",
      "check",
      "--fix",
      "--ignore",
      "E402,E501",
      input_file
      ],
      check=True,
    )
    logger.info("Ruff linting completed")

  def enhance_docstring_with_llm(self, input_path: str, output_path: str, dry_run: bool = False) -> None:
      """
      Enhance Python function docstrings using Azure OpenAI LLM in OpenAPI-style format.

      Args:
        input_path (str): Path to the input Python file.
        output_path (str): Path where the modified file will be saved.
        dry_run (bool): If True, only log the changes; do not write to disk.
      """
      import ast
      import re
      from cnoe_agent_utils import LLMFactory
      from langchain_core.messages import SystemMessage, HumanMessage

      logger.info(f"Starting LLM docstring enhancement for file: {input_path}")

      llm = LLMFactory().get_llm()

      def get_openapi_docstring(func_name, args, original_doc, func_code):
          if getattr(self, "should_enhance_docstring_with_llm_openapi", False):
              openapi_prompt = (
                  "Include an 'OpenAPI Specification:' section in the docstring and provide OpenAPI YAML under it if applicable. "
              )
          else:
              openapi_prompt = ""

          system_msg = SystemMessage(
              content=(
                  "You are a senior API engineer. Your task is to generate Python docstrings in Google-style format for async and sync functions used in platform engineering tools. "
                  "Use this format: \"\"\" Summary line. Args: arg1 (type): Description. arg2 (type, optional): Description. Defaults to None. Returns: ReturnType: Description. Raises: ExceptionType: Description. \"\"\". "
                  + openapi_prompt +
                  "Do not include any extra commentary or markdown formatting. Return only the complete docstring, enclosed in triple quotes."
              )
          )
          user_prompt = (
              f"Function Name: {func_name}\n"
              f"Arguments: {', '.join(args)}\n"
              f"Original Docstring:\n{original_doc or 'None'}\n"
              f"Function Code:\n{func_code}\n\n"
              f"Rewrite or generate a detailed OpenAPI-style Python docstring. Return only the full docstring including both opening and closing triple quotes (''' or \"\"\")."
          )
          response = llm.invoke([system_msg, HumanMessage(content=user_prompt)])

          def clean_docstring(content: str) -> str:
              # Remove markdown-style code blocks
              cleaned = re.sub(r"^```(?:python)?\n([\s\S]*?)\n```$", r"\1", content.strip(), flags=re.MULTILINE)
              # Remove leading/trailing triple quotes of either type, if present
              cleaned = re.sub(r"^([\"']{3,})", '', cleaned)
              cleaned = re.sub(r"([\"']{3,})$", '', cleaned)
              cleaned = cleaned.strip()
              # Always wrap in triple single quotes for safety
              return "'''\n" + cleaned + "\n'''"
          return clean_docstring(response.content)

      if not os.path.exists(input_path):
          raise FileNotFoundError(f"Input file '{input_path}' not found.")

      with open(input_path, 'r', encoding='utf-8') as f:
          source_code = f.read()
      source_lines = source_code.splitlines()

      try:
          tree = ast.parse(source_code)
      except SyntaxError as e:
          raise SyntaxError(f"Input file '{input_path}' contains invalid Python syntax: {e}")

      # Collect changes as tuples: (start_line, end_line, new_docstring_lines)
      docstring_replacements = []

      for node in ast.walk(tree):
          if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
              func_name = node.name
              args = [arg.arg for arg in node.args.args]
              doc = ast.get_docstring(node, clean=False)
              if doc is not None and len(node.body) > 0:
                  doc_node = node.body[0]
                  if isinstance(doc_node, ast.Expr) and isinstance(doc_node.value, ast.Constant):
                      doc_start = doc_node.lineno - 1
                      doc_end = doc_start + len(doc.splitlines())
                      func_source_lines = source_lines[node.lineno - 1:node.end_lineno]
                      func_source = "\n".join(func_source_lines)
                      try:
                          new_doc = get_openapi_docstring(func_name, args, doc, func_source)
                      except Exception as enhance_error:
                          logger.error(f"LLM enhancement failed for function '{func_name}': {enhance_error}. Raising error.")
                          raise RuntimeError(f"LLM enhancement failed for function '{func_name}': {enhance_error}") from enhance_error
                      indent = re.match(r'^(\s*)', source_lines[doc_start]).group(1)
                      new_doc_lines = [(indent + line if line.strip() else line) for line in new_doc.splitlines()]
                      docstring_replacements.append((doc_start, doc_end, new_doc_lines))

      # Apply replacements in reverse order (bottom-up) to avoid messing up line numbers
      for doc_start, doc_end, new_doc_lines in sorted(docstring_replacements, reverse=True):
          source_lines[doc_start:doc_end] = new_doc_lines

      if dry_run:
          logger.info(f"[Dry Run] Enhanced content for: {input_path}\n" + "\n".join(source_lines))
      else:
          with open(output_path, 'w', encoding='utf-8') as f:
              f.write("\n".join(source_lines))
          logger.info(f"Enhanced file written to: {output_path}")

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
      model_name = ''.join(word.capitalize() for word in re.split(r'[_\-]+', schema_name)).replace('.', '')
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
      model_path = os.path.join(self.src_output_dir, 'models', f'{camel_to_snake(schema_name)}.py')
      kwargs = self.get_file_header_kwargs()
      kwargs.update({
        'description': schema.get('description', ''),
        'fields': fields,
      })
      self.render_template('models/schema_model.tpl', model_path.lower(), model_name=model_name, **kwargs)
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
    enhancement_futures = []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    for path, ops in self.spec.get('paths', {}).items():
      logger.debug(f"Ops: {ops}")
      module_name = path.strip('/').replace('/', '_').replace('-', '_').replace('.', '_') or "root"
      module_name = module_name.replace("{", "").replace("}", "")
      functions = []
      for method, op in ops.items():
        if method.upper() not in ["GET", "POST", "PUT", "DELETE"]:
          continue
        # Merge path-item level parameters with operation-level parameters
        path_level_params = ops.get("parameters", [])  # may be absent
        op_level_params   = op.get("parameters", [])   # may be absent
        all_params: list = list(
            itertools.chain(path_level_params, op_level_params)
        )
        params = []
        # Holds parameter details for documentation
        params_infos = []
        for p in all_params:
          # Resolve parameter reference if the parameter itself is a $ref
          if "$ref" in p:
              p = self._resolve_ref(p["$ref"])

          # Skip header parameters; process path and query separately
          if p.get("in") == "header":
              continue

          if p.get("in") == "path":
              # Prepend "path_" to the parameter name
              pname = "path_" + p.get("name", "param").replace('.', '_')
              schema = p.get("schema", {})
              if "$ref" in schema:
                  schema = self._resolve_ref(schema["$ref"])
              ptype = self._get_python_type(schema)
              # For path parameters, assume they are required
              params.append(f"{pname}: {ptype}")
              params_infos.append({
                  "name": pname,
                  "type": ptype,
                  "description": p.get("description", "")
              })
          elif p.get("in") == "query":
              # Apply snake_case conversion for better Python compliance
              param_name = p.get("name", "param").replace('.', '_')
              pname = "param_" + camel_to_snake(param_name)
              # If the schema is not defined, use the parameter object itself
              schema = p.get("schema") or p
              if "$ref" in schema:
                  schema = self._resolve_ref(schema["$ref"])
              ptype = self._get_python_type(schema)
              desc = p.get("description", "")
              if p.get("required"):
                  params.append(f"{pname}: {ptype}")
              else:
                  if ptype == "bool":
                      params.append(f"{pname}: {ptype} = False")
                  else:
                      params.append(f"{pname}: {ptype} = None")
              params_infos.append({
                  "name": pname,
                  "type": ptype,
                  "description": desc
              })
          elif p.get("in") == "body":
              schema = p.get("schema", {})
              body_params = self._extract_body_params(schema, prefix="body")
              for sig, info in body_params:
                  params.append(sig)
                  params_infos.append(info)
        if "requestBody" in op:
            request_body = op["requestBody"]
            # Resolve component-level requestBodies references
            if isinstance(request_body, dict) and "$ref" in request_body:
                request_body = self._resolve_ref(request_body["$ref"]) or {}

            # At this point request_body must be the expanded object with “content”
            content = request_body.get("content", {})
            # Prefer JSON but fall back to the first available media type
            media = (
                content.get("application/json")
                or next(iter(content.values()), {})
            )
            schema = media.get("schema", {})
            if schema:
                body_params = self._extract_body_params(schema, prefix="body")
                for sig, info in body_params:
                    params.append(sig)
                    params_infos.append(info)
        # Reorder parameters: all non-default parameters first, then default parameters
        non_default_params = [p for p in params if "=" not in p]
        default_params = [p for p in params if "=" in p]
        params = non_default_params + default_params

        # Compute formatted_path by replacing each path placeholder with one that uses the resolved ref name prefixed with "path_"
        formatted_path = path
        for p in all_params:
            # Resolve the parameter if it uses a $ref
            if "$ref" in p:
                p = self._resolve_ref(p["$ref"])
            if p.get("in") == "path":
                orig_name = p.get("name", "param")
                fixed_name = "path_" + orig_name.replace(".", "_")
                # Replace placeholder {orig_name} with {fixed_name}
                formatted_path = formatted_path.replace("{" + orig_name + "}", "{" + fixed_name + "}")

        raw_operation_id = camel_to_snake(op.get("operationId", f"{method}_{module_name}").replace(" ", "_"))
        # Remove any curly braces from the operation id
        clean_operation_id = raw_operation_id.replace("{", "").replace("}", "")
        # Apply 30-character target with intelligent truncation and duplicate handling
        operation_id = truncate_function_name(clean_operation_id, method.upper(), self.used_function_names)

        logger.debug(f"Generating function for operation: {operation_id}, method: {method.upper()}, module: {module_name}, path: {path}")

        functions.append({
          "operation_id": operation_id,
          "summary": op.get("summary", ""),
          "description": op.get("description", ""),
          "method": method.upper(),
          "params": params,  # (used for signature)
          "params_info": params_infos,  # <-- NEW: list of dicts with name, type, and description
          "path": path,  # original path (optional, for reference)
          "formatted_path": formatted_path
        })
      if functions:
        output_path = os.path.join(tools_dir, f"{module_name.lower()}.py")
        mcp_server_base_package = self.config.get('mcp_server_base_package', '')
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
        if self.should_enhance_docstring_with_llm or self.should_enhance_docstring_with_llm_openapi:
          print("Submitting docstring enhancement for:", output_path)
          future = executor.submit(self.enhance_docstring_with_llm, input_path=output_path, output_path=output_path)
          enhancement_futures.append(future)

    self.render_template(
      "tools/init.tpl",
      os.path.join(tools_dir, '__init__.py'),
      **file_header_kwargs
      )

    if enhancement_futures:
        concurrent.futures.wait(enhancement_futures)
        errors_found = []
        for future in enhancement_futures:
            try:
                future.result()
            except Exception as e:
                logger.error(f"Error during parallel LLM docstring enhancement: {e}")
                errors_found.append(e)
        executor.shutdown(wait=True)
        if errors_found:
            raise RuntimeError("One or more errors occurred during LLM docstring enhancement.") from errors_found[0]

  def generate_server(self):
    """
    Generate the server file.
    """
    logger.info("Generating server")
    file_header_kwargs = self.get_file_header_kwargs()
    mcp_package = self.config.get('mcp_server_base_package', '')
    self.render_template(
      'server.tpl',
      os.path.join(self.src_output_dir, 'server.py'),
      mcp_name=self.mcp_name,
      mcp_package=mcp_package,
      modules=self.tools_map.keys(),
      registrations=self.tools_map,
      **file_header_kwargs)
    self.run_ruff_lint(os.path.join(self.src_output_dir, 'server.py'))

  def generate_agent(self):
      logger.info("Generating agent wrapper")
      agent_dir = self.output_dir            # render directly into target dir
      logger.debug(f"Agent directory (output dir): {agent_dir}")
      os.makedirs(agent_dir, exist_ok=True)
      server_pkg = os.path.basename(self.src_output_dir) # e.g. "mcp_komodor"

      from pathlib import Path  # add at top of file if not already imported
      _ = Path(self.output_dir).resolve().as_uri()              # absolute file URI of MCP project

      file_header_kwargs = self.get_file_header_kwargs()

      # Pass the generate_eval flag to all agent-level templates
      generate_eval = self.generate_eval

      # ------------------------- build SYSTEM prompt
      tool_docs = []
      for path, ops in self.spec.get("paths", {}).items():
          for method, op in ops.items():
              if method.upper() not in {"GET", "POST", "PUT", "DELETE"}:
                  continue
              t_name = camel_to_snake(op.get("operationId") or f"{method}_{path.strip('/')}")
              desc   = (op.get("description") or op.get("summary") or "").strip()
              tool_docs.append(f"- {t_name}: {desc}")

      tools_text = "\n".join(tool_docs) if tool_docs else "<no tools>"

      fallback_prompt = textwrap.dedent(
          f"""\
          You are an expert assistant for the {self.mcp_name} API.
          You can call the following tools:
          {tools_text}

          When a tool is appropriate, reply ONLY with the JSON payload;
          otherwise, answer normally."""
      ).strip()

      # Check if system_prompt is defined in config.yaml first
      config_system_prompt = self.config.get("system_prompt")
      if config_system_prompt:
          system_prompt = config_system_prompt.strip()
          logger.info("Using system prompt from config.yaml")
      elif self.generate_system_prompt:
          try:
              llm = LLMFactory().get_llm()
              sys_req = SystemMessage(
                  content=(
                      f"Write the SYSTEM prompt for a {self.mcp_name} assistant that "
                      f"can call the following tools:\n{tools_text}\n\n"
                      "Explain the general capabilities of the agent. "
                      "Keep the prompt concise and actionable."
                  )
              )
              system_prompt = llm.invoke([sys_req]).content.strip()
              logger.info("Generated system prompt using LLM")
          except Exception as e:  # noqa: BLE001
              logger.warning("LLM failed to generate system prompt: %s – using stub.", e)
              system_prompt = fallback_prompt
      else:
          system_prompt = fallback_prompt

      # Build two dependency blocks and concatenate conditionally
      base_deps = """
    "a2a-sdk>=0.2",
    "httpx>=0.28",
    "agntcy-acp>=1.3.2",
    "click>=8.2.0",
    "langchain-anthropic>=0.3.13",
    "langchain-core>=0.3.60",
    "langchain-google-genai>=2.1.4",
    "langchain-mcp-adapters>=0.1.9",
    "langchain-openai>=0.3.17",
    "langfuse>=3.2.0",
    "langchain>=0.3.27",
    "langgraph>=0.4.5",
    "uv",
    "rich (>=14.0.0,<15.0.0)",
    "sseclient (>=0.0.27,<0.0.28)",
    "cnoe-agent-utils>=0.3",
    "fastmcp>=2.11.1",
      """

      eval_deps = """
    "pytest>=8.3.5",
    "openevals>=0.0.6",
    "agentevals>=0.0.7",
    "langsmith>=0.3.32",
    "tabulate>=0.9.0",
      """

      agent_dependencies = base_deps + (eval_deps if self.generate_eval else "")
      if self.enable_slim:
          agent_dependencies += '    "agntcy-app-sdk>=0.1.0",\n'
      if self.with_a2a_proxy:
          agent_dependencies += '\n    "websockets>=12.0",\n'

      logger.info("Rendering agent/agent.py template")
      self.render_template(
          "agent/agent.tpl",
          os.path.join(agent_dir, "agent.py"),
          mcp_name=self.mcp_name,          # keep for env-var prefixes
          server_pkg=server_pkg,           # ← NEW
          generate_eval=generate_eval,
          system_prompt=system_prompt,     # << NEW
          **file_header_kwargs,
      )

      # Render Makefile into the agent root
      logger.info("Rendering agent/Makefile")
      self.render_template(
          "agent/Makefile.tpl",
          os.path.join(agent_dir, "Makefile"),
          mcp_name=self.mcp_name,
          generate_eval=generate_eval,
          a2a_proxy=self.with_a2a_proxy,
          enable_slim=self.enable_slim,
          **file_header_kwargs,
      )

      # Render README.md so Hatchling's readme field resolves
      logger.info("Rendering agent/README.md")
      self.render_template(
          "agent/README.tpl",
          os.path.join(agent_dir, "README.md"),
          mcp_name=self.mcp_name,
          generate_eval=generate_eval,
          a2a_proxy=self.with_a2a_proxy,
          **file_header_kwargs,
      )

      # Render Dockerfile for containerized runs
      logger.info("Rendering agent/Dockerfile")
      self.render_template(
          "agent/Dockerfile.tpl",
          os.path.join(agent_dir, "Dockerfile"),
          mcp_name=self.mcp_name,
          enable_slim=self.enable_slim,
          **file_header_kwargs,
      )

      # -------------------- docker-compose (only when SLIM enabled)
      if self.enable_slim:
          logger.info("Rendering agent/docker-compose.yml")
          self.render_template(
              "agent/docker-compose.tpl",
              os.path.join(agent_dir, "docker-compose.yml"),
              mcp_name=self.mcp_name,
          )
          logger.info("Rendering agent/slim-config.yaml")
          self.render_template(
              "agent/slim-config.yaml.tpl",
              os.path.join(agent_dir, "slim-config.yaml"),
              mcp_name=self.mcp_name,
          )


      if self.generate_eval:
          # Render eval_mode.py
          logger.info("Rendering agent/eval_mode.py")
          self.render_template(
              "agent/eval_mode.tpl",
              os.path.join(agent_dir, "eval_mode.py"),
              mcp_name=self.mcp_name,
              **file_header_kwargs,
          )
          self.run_ruff_lint(os.path.join(agent_dir, "eval_mode.py"))

      # Render .env.example for the agent
      logger.info("Rendering agent/.env.example")
      self.render_template(
          "agent/env.tpl",
          os.path.join(agent_dir, ".env.example"),
          mcp_name=self.mcp_name,
          **file_header_kwargs,
      )
      logger.info("Formatting agent/agent.py with Ruff")
      self.run_ruff_lint(os.path.join(agent_dir, "agent.py"))

      # ---------------------------------------------------------------- pyproject.toml
      logger.info("Rendering agent/pyproject.toml")
      self.render_template(
          "agent/pyproject.tpl",
          os.path.join(agent_dir, "pyproject.toml"),
          mcp_name=self.mcp_name,
          version=self.config.get("version", "0.1.0"),
          description=self.config.get(
              "agent_description",
              f"LangGraph agent for {self.mcp_name} MCP tools",
          ),
          author=self.config.get("author", "CNOE Contributors"),
          email=self.config.get("email", "auto@example.com"),
          license=self.config.get("license", "Apache-2.0"),
          poetry_dependencies=agent_dependencies,
          generate_eval=generate_eval,
          a2a_proxy=self.with_a2a_proxy,
          **file_header_kwargs,
      )

      # generate server (A2A or WebSocket proxy)
      if self.with_a2a_proxy:
          self._generate_ws_proxy(agent_dir)
      else:
          self._generate_a2a_server(agent_dir)

      # If generate_eval is True, build the eval directory here
      if self.generate_eval:
          logger.info("Generating evaluation code inside agent eval dir")
          eval_dir = os.path.join(agent_dir, "eval")
          os.makedirs(eval_dir, exist_ok=True)
          self.render_template(
              "agent/evaluate_agent.tpl",
              os.path.join(eval_dir, "evaluate_agent.py"),
              mcp_name=self.mcp_name,
          )

      logger.info("Agent wrapper generation completed")

  # ------------------------------------------------------------------ A2A
  def _generate_a2a_server(self, agent_dir: str) -> None:
      logger.info("Generating A2A server scaffolding")
      a2a_dir = os.path.join(agent_dir, "protocol_bindings", "a2a_server")
      os.makedirs(a2a_dir, exist_ok=True)
      logger.debug(f"A2A server directory: {a2a_dir}")

      fh = self.get_file_header_kwargs()

      # Extract skills from config.yaml if available, otherwise fallback to OpenAPI spec
      skills = []
      skill_examples = []

      # Try to get skills from config first
      config_skills = self.config.get("skills", [])
      if config_skills:
          # Use skills from config.yaml
          skills = config_skills
          # For backward compatibility, also create a flattened list of examples for simple template usage
          for skill in config_skills:
              skill_examples.extend([f"'{example}'" for example in skill.get("examples", [])])
      else:
          # Fallback to extracting from OpenAPI spec (original behavior)
          for path, ops in self.spec.get("paths", {}).items():
              for method, op in ops.items():
                  if method.upper() not in {"GET", "POST", "PUT", "DELETE"}:
                      continue
                  operation_desc = op.get("summary") or op.get("description", "")
                  if operation_desc:
                      skill_examples.append(f"'{operation_desc.strip()}'")

          # Limit to reasonable number of examples
          skill_examples = skill_examples[:5]

      # Get system prompt from config if available
      config_system_prompt = self.config.get("system_prompt")
      if config_system_prompt:
          system_prompt = config_system_prompt.strip()
      else:
          # Fallback system prompt
          system_prompt = f"""You are a {self.mcp_name.replace('_', ' ').title()} expert assistant. You help users manage and interact with {self.mcp_name.replace('_', ' ').title()} services.

Your capabilities include:
- Managing {self.mcp_name.replace('_', ' ').title()} resources and configurations
- Monitoring service status and performance
- Handling API operations and data retrieval
- Troubleshooting issues and providing solutions
- Providing best practices and recommendations

Always provide clear, actionable responses and include relevant resource names, status information, and next steps when available."""

      proto_dir = os.path.join(agent_dir, "protocol_bindings")
      os.makedirs(proto_dir, exist_ok=True)
      logger.info("Rendering protocol_bindings/__init__.py")
      self.render_template("init_empty.tpl", os.path.join(proto_dir, "__init__.py"), **fh)
      self.run_ruff_lint(os.path.join(proto_dir, "__init__.py"))

      logger.info("Rendering a2a_server/__init__.py")
      self.render_template("init_empty.tpl", os.path.join(a2a_dir, "__init__.py"), **fh)

      logger.info("Rendering state.py")
      self.render_template("agent/a2a_server/state.tpl", os.path.join(a2a_dir, "state.py"), **fh)

      logger.info("Rendering helpers.py")
      self.render_template("agent/a2a_server/helpers.tpl", os.path.join(a2a_dir, "helpers.py"), **fh)

      # Note: base_agent.py and base_agent_executor.py are no longer generated
      # since we now use cnoe_agent_utils.agents.BaseLangGraphAgent and BaseLangGraphAgentExecutor

      logger.info("Rendering agent.py")
      self.render_template("agent/a2a_server/agent.tpl", os.path.join(a2a_dir, "agent.py"),
                          mcp_name=self.mcp_name, system_prompt=system_prompt, **fh)

      logger.info("Rendering agent_executor.py")
      self.render_template("agent/a2a_server/agent_executor.tpl", os.path.join(a2a_dir, "agent_executor.py"), mcp_name=self.mcp_name, **fh)

      logger.info("Rendering __main__.py")
      self.render_template(
          "agent/a2a_server/__main__.tpl",
          os.path.join(a2a_dir, "__main__.py"),
          mcp_name=self.mcp_name,
          enable_slim=self.enable_slim,
          skills=skills,
          skill_examples=skill_examples,
          system_prompt=system_prompt,
          **fh,
      )

      # Ruff format
      for file in ["state.py", "helpers.py", "agent.py", "agent_executor.py", "__main__.py"]:
          logger.debug(f"Formatting {file} with Ruff")
          self.run_ruff_lint(os.path.join(a2a_dir, file))

      logger.info("A2A server scaffolding generation completed")


  def generate_pyproject(self):
    """
    Generate the pyproject.toml file.
    """
    logger.info("Generating pyproject.toml")
    output_path = os.path.join(self.output_dir, 'pyproject.toml')
    python_dependencies = """
      python = ">=3.13,<4.0"
      httpx = ">=0.24.0"
      python-dotenv = ">=1.0.0"
      pydantic = ">=2.0.0"
      mcp = ">=1.9.0"
    """
    self.render_template(
      'pyproject.tpl',
      output_path,
      name=f"mcp_{self.mcp_name}",
      description=self.config.get('description', f'Generated {self.mcp_name} MCP server'),
      version=self.config.get('version', '0.1.0'),
      license=self.config.get('license', 'Apache-2.0'),
      author=self.config.get('author', 'Unspecified'),
      email=self.config.get('email','auto@example.com'),
      python_version=self.config.get('python_version', '3.13'),
      mcp_name=self.mcp_name,
      poetry_dependencies=self.config.get('poetry_dependencies', python_dependencies),
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
      a2a_proxy=self.with_a2a_proxy,
    )

  def generate_init_files(self):
    """
    Generate __init__.py files for all directories.
    """
    logger.info("Generating __init__.py files")
    file_header_kwargs = self.get_file_header_kwargs()
    self.render_template(
       'init_empty.tpl',
       os.path.join(self.output_dir, '__init__.py'),

       **file_header_kwargs)
    self.render_template(
       'init_empty.tpl',
       os.path.join(self.src_output_dir, '__init__.py'),
       version=self.config.get('version', '0.1.0'),
       **file_header_kwargs)
    for subdir in ['api', 'models', 'tools']:
      path = os.path.join(self.src_output_dir, subdir)
      os.makedirs(path, exist_ok=True)
      self.render_template('init_empty.tpl', os.path.join(path, '__init__.py'), **file_header_kwargs)

  def _resolve_ref(self, ref: str) -> Dict[str, Any]:
      """
      Resolve a JSON reference from the OpenAPI spec.
      Assumes refs are of the form "#/components/schemas/ModelName".
      """
      parts = ref.lstrip("#/").split("/")
      resolved = self.spec
      for part in parts:
          resolved = resolved.get(part)
          if resolved is None:
              break
      return resolved if resolved is not None else {}

  def _count_nested_params(self, schema: Dict[str, Any]) -> int:
      """
      Count total number of nested parameters in a schema.

      Args:
          schema: OpenAPI schema

      Returns:
          Total parameter count
      """
      if not isinstance(schema, dict):
          return 0

      if "$ref" in schema:
          schema = self._resolve_ref(schema["$ref"])

      count = 0
      if schema.get("type") == "object" and "properties" in schema:
          properties = schema.get("properties", {})
          for prop_name, prop in properties.items():
              count += 1  # Count this property
              if prop.get("type") == "object" and "properties" in prop:
                  # Recursively count nested properties
                  count += self._count_nested_params(prop)

      return count

  def _extract_body_params(self, schema: Dict[str, Any], prefix: str = "body", max_params: int = 10) -> list:
      """
      Recursively extract parameters from a request body schema.
      Each parameter name is prefixed so that nested properties are flattened.
      If schema has > max_params nested properties, returns a single Dict parameter.
      Returns a list of tuples: (signature_string, {name, type, description})
      """
      if "$ref" in schema:
          schema = self._resolve_ref(schema["$ref"])

      # Check if schema is too complex - use dict mode if so
      param_count = self._count_nested_params(schema)
      if param_count > max_params:
          logger.info(f"Body schema has {param_count} nested params (limit: {max_params}), using dict mode for {prefix}")
          sig = f"{prefix}: Dict[str, Any] = None"
          desc = schema.get("description", "")
          if not desc:
              desc = f"Request body as dictionary. Contains {param_count} nested properties. See OpenAPI schema for detailed structure."
          info = {
              "name": prefix,
              "type": "Dict[str, Any]",
              "description": desc
          }
          return [(sig, info)]

      # Handle JSON-Schema composition keywords ---------------------------------
      for key in ("allOf", "oneOf", "anyOf"):
          if key in schema:
              # First, count total params across all subschemas to check if we should use dict mode
              total_count = 0
              for subschema in schema[key]:
                  if "$ref" in subschema:
                      subschema = self._resolve_ref(subschema["$ref"])
                  total_count += self._count_nested_params(subschema)

              # If total exceeds limit, use dict mode
              if total_count > max_params:
                  logger.info(f"Composition schema ({key}) has {total_count} total nested params (limit: {max_params}), using dict mode for {prefix}")
                  sig = f"{prefix}: Dict[str, Any] = None"
                  desc = schema.get("description", "")
                  if not desc:
                      desc = f"Request body as dictionary. Contains {total_count} nested properties across {len(schema[key])} {key} branches. See OpenAPI schema for detailed structure."
                  info = {
                      "name": prefix,
                      "type": "Dict[str, Any]",
                      "description": desc
                  }
                  return [(sig, info)]

              # Otherwise, extract params normally
              merged: list[tuple[str, dict]] = []
              for subschema in schema[key]:
                  if "$ref" in subschema:
                      subschema = self._resolve_ref(subschema["$ref"])
                  merged.extend(self._extract_body_params(subschema, prefix=prefix, max_params=max_params))
              # Deduplicate identical signatures that may occur when the same
              # property appears in multiple branches
              seen: set[str] = set()
              unique: list[tuple[str, dict]] = []
              for sig, info in merged:
                  if sig not in seen:
                      unique.append((sig, info))
                      seen.add(sig)
              return unique
      params = []
      if schema.get("type") == "object" and "properties" in schema:
          required_fields = schema.get("required", [])
          params_info = []
          for prop_name, prop in schema["properties"].items():
              # Use single "_" for consistent parameter naming
              # Improved from argocon-na-2025-b: single underscore for all nesting
              delim = "_"
              param_name = f"{prefix}{delim}{camel_to_snake(prop_name)}"
              if "$ref" in prop:
                  resolved_prop = self._resolve_ref(prop["$ref"])
                  # Use single "_" for consistent parameter naming
                  # Improved from argocon-na-2025-b: single underscore for all nesting
                  delim = "_"
                  param_name = f"{prefix}{delim}{camel_to_snake(prop_name)}"
                  if resolved_prop.get("type") == "object" and "properties" in resolved_prop:
                      sub_params = self._extract_body_params(resolved_prop, prefix=param_name)
                      for sig, info in sub_params:
                          params.append(sig)
                          params_info.append(info)
                      continue
                  else:
                      prop = resolved_prop
              if prop.get("type") == "object" and "properties" in prop:
                  sub_params = self._extract_body_params(prop, prefix=param_name)
                  for sig, info in sub_params:
                      params.append(sig)
                      params_info.append(info)
              else:
                  if "$ref" in prop:
                      prop = self._resolve_ref(prop["$ref"])
                  py_type = self._get_python_type(prop)
                  if prop_name in required_fields:
                      sig = f"{param_name}: {py_type}"
                  else:
                      sig = f"{param_name}: {py_type} = None"
                  params.append(sig)
                  params_info.append({
                      "name": param_name,
                      "type": py_type,
                      "description": prop.get("description", "")
                  })
          return list(zip(params, params_info))
      elif schema.get("type") == "array":
          items = schema.get("items", {})
          # If the items are objects with properties, set type to a list of dicts.
          if items.get("type") == "object" and "properties" in items:
              py_type = "List[Dict[str, Any]]"
          else:
              py_type = self._get_python_type(schema)
          sig = f"{prefix}: {py_type}"
          info = {"name": prefix, "type": py_type, "description": schema.get("description", "")}
          return [(sig, info)]
      else:
          if "$ref" in schema:
              schema = self._resolve_ref(schema["$ref"])
          py_type = self._get_python_type(schema)
          sig = f"{prefix}: {py_type}"
          info = {"name": prefix, "type": py_type, "description": schema.get("description", "")}
          return [(sig, info)]


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
    self.generate_pyproject()
    if self.generate_agent_flag:
        self.generate_agent()
    self.generate_init_files()
    if not self.generate_agent_flag:
        self.generate_env()
    if not self.generate_agent_flag:
        self.generate_readme()
        logger.info("MCP code generation completed")

        # Run function validation
        self._run_function_validation()

  def _run_function_validation(self):
    """Run function validation on the generated code."""
    try:
        from .function_validator import FunctionValidator

        logger.info("🔍 Running function validation on generated code...")

        # Create validator for the current project
        project_root = Path(self.output_dir).parent.parent  # Go up to project root
        validator = FunctionValidator(project_root)

        # Validate the current project
        current_project_path = Path(self.src_output_dir)
        result = validator.validate_project(current_project_path)

        if result.passed:
            logger.info("✅ Function validation passed!")
            logger.info(f"   ✨ {result.total_functions} functions validated")
            logger.info(f"   ✨ No duplicates or critical issues found")

            if result.warnings:
                logger.info(f"   ⚠️  {len(result.warnings)} minor warnings (see details above)")
        else:
            logger.error("❌ Function validation failed!")
            logger.error(f"   🔧 {result.total_functions} functions checked")
            logger.error(f"   ❌ {len(result.errors)} critical errors found")

            # Print specific errors
            for error in result.errors:
                logger.error(f"      • {error}")

            # Print duplicates if any
            if result.duplicates:
                logger.error("   📋 Duplicate functions found:")
                for name, paths in result.duplicates.items():
                    logger.error(f"      • '{name}' appears in {len(paths)} files")

            # Print length violations
            if result.length_violations:
                logger.error("   📏 Function name length violations:")
                for func in result.length_violations:
                    logger.error(f"      • '{func.name}' ({func.length} chars > {validator.max_length} limit)")

            logger.error("   💡 Run with --verbose for detailed analysis")

    except ImportError:
        logger.warning("⚠️  Function validator not available, skipping validation")
    except Exception as e:
        logger.warning(f"⚠️  Function validation failed: {e}")

  # ---------------------------------------------------------------- WebSocket proxy
  def _generate_ws_proxy(self, agent_dir: str) -> None:
      logger.info("Generating WebSocket proxy server")
      ws_dir = os.path.join(agent_dir, "protocol_bindings", "ws_proxy")
      os.makedirs(ws_dir, exist_ok=True)
      fh = self.get_file_header_kwargs()

      # __init__.py
      self.render_template("init_empty.tpl", os.path.join(ws_dir, "__init__.py"), **fh)
      self.run_ruff_lint(os.path.join(ws_dir, "__init__.py"))

      # server.py
      self.render_template(
          "agent/ws_proxy/server.tpl",
          os.path.join(ws_dir, "server.py"),
          mcp_name=self.mcp_name,
          **fh,
      )
      self.run_ruff_lint(os.path.join(ws_dir, "server.py"))

      # __main__.py
      self.render_template(
          "agent/ws_proxy/__main__.tpl",
          os.path.join(ws_dir, "__main__.py"),
          mcp_name=self.mcp_name,
          **fh,
      )
      self.run_ruff_lint(os.path.join(ws_dir, "__main__.py"))

      logger.info("WebSocket proxy generation completed")
