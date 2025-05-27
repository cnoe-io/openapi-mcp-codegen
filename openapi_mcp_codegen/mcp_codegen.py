#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

import os
import json
import yaml
import logging
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any, List
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp_codegen")

class MCPGenerator:
    def __init__(self, script_dir: str, spec_path: str, output_dir: str, config_path: str):
        self.script_dir = script_dir
        self.spec_path = spec_path
        self.output_dir = output_dir
        self.env = Environment(loader=FileSystemLoader(os.path.join(script_dir, 'templates')))
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.spec = self._load_spec()
        self.mcp_name = self.spec.get('info', {}).get('title', 'generated_mcp').lower().replace(' ', '_mcp')
        self.src_output_dir = os.path.join(self.output_dir, f'mcp_{self.mcp_name}')
        os.makedirs(self.src_output_dir, exist_ok=True)

    def _load_spec(self):
        with open(self.spec_path, 'r', encoding='utf-8') as f:
            if self.spec_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            return json.load(f)

    def render_template(self, template_name: str, output_path: str, **kwargs):
        logger.info(f"Rendering template: {template_name} to {output_path}")
        template = self.env.get_template(template_name)
        logger.info(f"Template: {template}")
        rendered = template.render(**kwargs)
        with open(output_path, 'w') as f:
            f.write(rendered)
        logger.info(f"Generated: {output_path}")

    def _get_python_type(self, prop: Dict[str, Any]) -> str:
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
      logger.info(f"Running ruff lint with --fix and two-space indentation on {input_file}")
      # ruff_config_path = os.path.join(self.output_dir, '.ruff.toml')
      # with open(ruff_config_path, 'w') as f:
      #   f.write("line-length = 120\n")
      #   f.write("indent-width = 2\n")
      #   f.write("[format]\n")
      #   f.write("indent-style = 'space'\n")
      subprocess.run(["ruff", "check", "--fix", "--ignore", "E402", input_file], check=True)
      logger.info("Ruff linting completed")

    def get_file_header_kwargs(self):
      file_headers_config = self.config.get("file_headers", {})
      kwargs = None
      if file_headers_config is not None:
          kwargs = {
            "file_headers": True,
            "file_headers_copyright": file_headers_config.get("copyright", ""),
            "file_headers_license": file_headers_config.get("license", ""),
            "file_headers_message": file_headers_config.get("message", "")
          }
      else:
          kwargs = {
            "file_headers": False,
            "file_headers_copyright": "",
            "file_headers_license": "",
            "file_headers_message": ""
          }
      return kwargs

    def generate_model_base(self):
        path = os.path.join(self.src_output_dir, 'models')
        os.makedirs(path, exist_ok=True)
        file_header_kwargs = self.get_file_header_kwargs()
        self.render_template('models/base_model.tpl', os.path.join(path, 'base.py'), **file_header_kwargs)
        self.run_ruff_lint(os.path.join(path, 'base.py'))

    def generate_models(self):
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
            kwargs = self.get_file_header_kwargs()
            kwargs.update({
                'description': schema.get('description', ''),
                'fields': fields,
            })

            self.render_template(
                '/models/schema_model.tpl',
                model_path,
                model_name=model_name,
                **kwargs
            )
            self.run_ruff_lint(model_path)

    def generate_api_client(self):
        api_dir = os.path.join(self.src_output_dir, 'api')
        os.makedirs(api_dir, exist_ok=True)
        kwargs = self.get_file_header_kwargs()
        kwargs.update({
          'api_url': "https://api.example.com",
          'api_token': "your_api_key_here",
          'api_headers': self.config.get('headers', {}),
        })
        self.render_template(
            'api/client.tpl',
            os.path.join(api_dir, 'client.py'),
            mcp_name=self.mcp_name,
            **kwargs
        )
        self.run_ruff_lint(os.path.join(api_dir, 'client.py'))
        self.render_template('init_empty.tpl', os.path.join(api_dir, '__init__.py'))

    def generate_tool_modules(self):
        tools_dir = os.path.join(self.src_output_dir, 'tools')
        file_header_kwargs = self.get_file_header_kwargs()
        os.makedirs(tools_dir, exist_ok=True)
        for path, ops in self.spec.get('paths', {}).items():
            if '{' in path:
                continue  # skip path params for now
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
                mcp_server_base_package = ""
                mcp_server_base_package = self.config.get('mcp_package', {}).get('mcp_server_base_package', '')
                self.render_template(
                    "tools/tool.tpl",
                    output_path,
                    path=path,
                    import_path=f"mcp_{self.mcp_name}.api.client",
                    mcp_name=self.mcp_name,
                    mcp_server_base_package = mcp_server_base_package,
                    functions=functions,
                    **file_header_kwargs
                )
                self.run_ruff_lint(output_path)
        self.render_template("tools/init.tpl", os.path.join(tools_dir, '__init__.py'), **file_header_kwargs)

    def generate_pyproject(self):
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
        output_path = os.path.join(self.output_dir, '.env.example')
        self.render_template('env.tpl', output_path)

    def generate_readme(self):
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
        file_headers_copyright = self.config.get('file_headers', {}).get('copyright', '')
        file_headers_license = self.config.get('file_headers', {}).get('license', '')
        file_headers_message = self.config.get('file_headers', {}).get('message', '')

        self.render_template(
            'init_empty.tpl',
            os.path.join(self.src_output_dir, '__init__.py'),
            file_headers = self.config.get('file_headers', {}),
            file_headers_copyright = file_headers_copyright,
            file_headers_license = file_headers_license,
            file_headers_message = file_headers_message,
        )

        print(f"\nfile_headers_copyright: {file_headers_copyright}")
        print(f"\nfile_headers_license: {file_headers_license}")
        print(f"\nfile_headers_message: {file_headers_message}")
        for subdir in ['models', 'api', 'utils']:
            path = os.path.join(self.src_output_dir, subdir)
            os.makedirs(path, exist_ok=True)
            self.render_template(
              'init_empty.tpl',
              os.path.join(path, '__init__.py'),
              file_headers = self.config.get('file_headers', {}),
              file_headers_copyright = file_headers_copyright,
              file_headers_license = file_headers_license,
              file_headers_message = file_headers_message,
            )

    def generate(self):
        logger.info("Starting MCP codegen with templates")
        self.generate_api_client()
        self.generate_model_base()
        self.generate_models()
        self.generate_tool_modules()
        self.generate_init_files()
        self.generate_pyproject()
        self.generate_env()
        self.generate_readme()
        logger.info("Template-based MCP codegen completed")