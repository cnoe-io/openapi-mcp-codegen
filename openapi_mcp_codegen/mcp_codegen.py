#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
MCP Generator Tool

This tool generates a Model Context Protocol (MCP) server from an OpenAPI specification.
It follows the same structure as the PagerDuty MCP server.
"""

import json
import os
import logging
import yaml
import sys
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("mcp_generator")

class MCPGenerator:
    def __init__(self, openapi_spec_path: str, output_dir: str):
        self.openapi_spec_path = openapi_spec_path
        self.output_dir = output_dir
        self.spec = None
        self.base_path = None
        self.mcp_name = None

    def get_git_head_short_sha(self) -> str:
        """Get the current git HEAD short SHA of the package"""
        try:
            git_dir = os.path.join(self.output_dir, '.git')
            head_path = os.path.join(git_dir, 'HEAD')
            if not os.path.exists(head_path):
                logger.warning("No git repository found, using default SHA")
                return ""
            with open(head_path, 'r') as f:
                ref = f.read().strip()
            if ref.startswith('ref:'):
                ref_path = os.path.join(git_dir, ref.split(' ')[1])
                with open(ref_path, 'r') as f:
                    sha = f.read().strip()
            else:
                sha = ref
            return sha[:7]
        except Exception as e:
            logger.warning(f"Could not get git SHA: {str(e)}")
            return ""

    def load_spec(self):
        """Load and parse the OpenAPI specification"""
        try:
            with open(self.openapi_spec_path, 'r', encoding='utf-8') as f:
                if self.openapi_spec_path.endswith('.yaml') or self.openapi_spec_path.endswith('.yml'):
                    self.spec = yaml.safe_load(f)
                else:
                    self.spec = json.load(f)

            self.base_path = self.spec.get('servers', [{}])[0].get('url', '').rstrip('/')

            # Get the API title and convert to lowercase for the MCP name
            self.mcp_name = self.spec.get('info', {}).get('title', 'generated_mcp').lower().replace(' ', '_mcp')
            logger.info(f"Successfully loaded OpenAPI spec from {self.openapi_spec_path}")
            logger.info(f"Base URL: {self.base_path}")
            logger.info(f"MCP name: {self.mcp_name}")
        except FileNotFoundError:
            logger.error(f"OpenAPI spec file not found: {self.openapi_spec_path}")
            raise
        except (json.JSONDecodeError, yaml.YAMLError):
            logger.error(f"Invalid format in OpenAPI spec file: {self.openapi_spec_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading OpenAPI spec: {str(e)}")
            raise

    def create_directory_structure(self):
        """Create the MCP server directory structure"""
        try:
            dirs = [
                'api',
                'models',
                'tools',
                'utils'
            ]

            for dir_name in dirs:
                dir_path = os.path.join(self.output_dir, dir_name)
                os.makedirs(dir_path, exist_ok=True)
                logger.debug(f"Created directory: {dir_path}")

            logger.info("Created MCP server directory structure")
        except Exception as e:
            logger.error(f"Error creating directory structure: {str(e)}")
            raise

    def generate_models(self):
        """Generate model files based on OpenAPI schemas"""
        try:
            # Create base models file
            base_models = '''"""Base models for the API"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    """Base model for API responses"""
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None

class PaginationInfo(BaseModel):
    """Pagination information"""
    offset: int
    limit: int
    total: Optional[int] = None
    more: Optional[bool] = None

'''
            with open(os.path.join(self.output_dir, 'models', 'base.py'), 'w', encoding='utf-8') as f:
                f.write(base_models)
            logger.info("Generated base models")

            # Generate models from schemas
            schemas = self.spec.get('components', {}).get('schemas', {})
            for schema_name, schema in schemas.items():
                model_name = ''.join(word.capitalize() for word in schema_name.split('_'))
                model_code = f'''"""Model for {schema_name}"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

'''

                # Add model class
                model_code += f'class {model_name}(BaseModel):\n'
                model_code += f'    """{schema.get("description", f"{model_name} model")}"""\n\n'

                # Add properties
                properties = schema.get('properties', {})
                required = schema.get('required', [])

                for prop_name, prop in properties.items():
                    prop_type = self._get_python_type(prop)
                    if prop_name in required:
                        model_code += f'    {prop_name}: {prop_type}\n'
                    else:
                        model_code += f'    {prop_name}: Optional[{prop_type}] = None\n'

                    if prop.get('description'):
                        model_code += f'    """{prop["description"]}"""\n'

                # Add response model
                model_code += f'\nclass {model_name}Response(APIResponse):\n'
                model_code += f'    """Response model for {model_name}"""\n'
                model_code += f'    data: Optional[{model_name}] = None\n'

                # Add list response model
                model_code += f'\nclass {model_name}ListResponse(APIResponse):\n'
                model_code += f'    """List response model for {model_name}"""\n'
                model_code += f'    data: List[{model_name}] = Field(default_factory=list)\n'
                model_code += '    pagination: Optional[PaginationInfo] = None\n'

                # Write model file
                model_path = os.path.join(self.output_dir, 'models', f'{schema_name}.py')
                with open(model_path, 'w', encoding='utf-8') as f:
                    f.write(model_code)
                logger.info(f"Generated model for {schema_name}")

        except Exception as e:
            logger.error(f"Error generating models: {str(e)}")
            raise

    def _get_python_type(self, schema: Dict[str, Any]) -> str:
        """Convert OpenAPI type to Python type"""
        schema_type = schema.get('type')
        if schema_type == 'integer':
            return 'int'
        elif schema_type == 'number':
            return 'float'
        elif schema_type == 'boolean':
            return 'bool'
        elif schema_type == 'array':
            items = schema.get('items', {})
            item_type = self._get_python_type(items)
            return f'List[{item_type}]'
        elif schema_type == 'object':
            return 'Dict'
        else:
            return 'str'

    def generate_api_client(self):
        """Generate the API client module"""
        try:
            client_code = '''"""API client for making requests to the service"""

import logging
from typing import Optional, Dict, Tuple, Any
import httpx

# Constants
API_URL = "https://api.pagerduty.com"
DEFAULT_TOKEN = "your_api_key_here"

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_api")

# Log token presence but not the token itself
if DEFAULT_TOKEN:
    logger.info("Default token is hardcoded and present.")
else:
    logger.warning("No default token is set.")

async def make_api_request(
    path: str,
    method: str = "GET",
    token: Optional[str] = None,
    params: Dict[str, Any] = {},
    data: Dict[str, Any] = {},
    timeout: int = 30,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Make a request to the API

    Args:
        path: API path to request (without base URL)
        method: HTTP method (default: GET)
        token: API token (defaults to DEFAULT_TOKEN)
        params: Query parameters for the request (optional)
        data: JSON data for POST/PATCH/PUT requests (optional)
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Tuple of (success, data) where data is either the response JSON or an error dict
    """
    logger.debug(f"Making {method} request to {path}")

    if not token:
        logger.debug("No token provided, using default token")
        token = DEFAULT_TOKEN

    if not token:
        logger.error("No token available - neither provided nor found in environment")
        return (
            False,
            {"error": "Token is required. Please set the API_KEY environment variable."},
        )

    try:
        headers = {
            "Authorization": f"Token token={token}",
            "Accept": "application/vnd.pagerduty+json;version=2",
            "Content-Type": "application/json",
        }
        logger.debug(f"Request headers prepared (Authorization header masked)")
        logger.debug(f"Request parameters: {params}")
        if data:
            logger.debug(f"Request data: {data}")

        async with httpx.AsyncClient(timeout=timeout) as client:
            url = f"{API_URL}/{path}"
            logger.debug(f"Full request URL: {url}")

            # Map HTTP methods to client methods
            method_map = {
                "GET": client.get,
                "POST": client.post,
                "PUT": client.put,
                "PATCH": client.patch,
                "DELETE": client.delete,
            }

            if method not in method_map:
                logger.error(f"Unsupported HTTP method: {method}")
                return (False, {"error": f"Unsupported method: {method}"})

            # Make the request
            logger.debug(f"Executing {method} request")
            # Only include json parameter for methods that use request body
            request_kwargs = {
                "headers": headers,
                "params": params,
            }
            if method in ["POST", "PUT", "PATCH"]:
                request_kwargs["json"] = data
            response = await method_map[method](
                url,
                **request_kwargs
            )
            logger.debug(f"Response status code: {response.status_code}")

            # Handle different response codes
            if response.status_code in [200, 201, 202, 204]:
                if response.status_code == 204:  # No content
                    logger.debug("Request successful (204 No Content)")
                    return (True, {"status": "success"})
                try:
                    response_data = response.json()
                    logger.debug("Request successful, parsed JSON response")
                    return (True, response_data)
                except ValueError:
                    logger.warning("Request successful but could not parse JSON response")
                    return (True, {"status": "success", "raw_response": response.text})
            else:
                error_message = f"API request failed: {response.status_code}"
                logger.error(error_message)
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_message = f"{error_message} - {error_data['error']}"
                    elif "message" in error_data:
                        error_message = f"{error_message} - {error_data['message']}"
                    logger.error(f"Error details: {error_data}")
                    return (False, {"error": error_message, "details": error_data})
                except ValueError:
                    error_text = response.text[:200] if response.text else ""
                    logger.error(f"Error response (not JSON): {error_text}")
                    return (False, {"error": f"{error_message} - {error_text}"})
    except httpx.TimeoutException:
        logger.error(f"Request timed out after {timeout} seconds")
        return (False, {"error": f"Request timed out after {timeout} seconds"})
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code} - {str(e)}")
        return (False, {"error": f"HTTP error: {e.response.status_code} - {str(e)}"})
    except httpx.RequestError as e:
        error_message = str(e)
        if token and token in error_message:
            error_message = error_message.replace(token, "[REDACTED]")
        logger.error(f"Request error: {error_message}")
        return (False, {"error": f"Request error: {error_message}"})
    except Exception as e:
        # Ensure no sensitive data is included in error messages
        error_message = str(e)
        if token and token in error_messaged:
            error_message = error_message.replace(token, "[REDACTED]")
        logger.error(f"Unexpected error: {error_message}")
        return (False, {"error": f"Unexpected error: {error_message}"})
'''
            client_path = os.path.join(self.output_dir, 'api', 'client.py')
            with open(client_path, 'w', encoding='utf-8') as f:
                f.write(client_code)
            logger.info(f"Generated API client at {client_path}")
        except Exception as e:
            logger.error(f"Error generating API client: {str(e)}")
            raise

    def generate_tool_module(self, path: str, operations: Dict[str, Any]):
        """Generate a tool module for a specific API path, skip if path has '{'"""
        try:
            if '{' in path:
                return  # Skip endpoints with path parameters
            module_name = path.strip('/').replace('/', '_')
            tool_code = f'''"""Tools for {path} operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from mcp_{self.mcp_name}.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")

'''
            # Generate tool functions for each operation
            for method, operation in operations.items():
                if method.lower() not in ['get', 'post', 'put', 'delete']:
                    continue
                operation_id = operation.get('operationId', f'{method}_{module_name}')
                summary = operation.get('summary', '')
                description = operation.get('description', '')
                # Generate parameters (skip path parameters)
                params = []
                if 'parameters' in operation:
                    for param in operation['parameters']:
                        if param.get('in') == 'path':
                            continue  # Skip path parameters
                        if 'name' not in param:
                            logger.warning(f"Skipping parameter without name in {path} {method}")
                            continue
                        param_name = param['name']
                        param_type = 'str'  # Default type
                        schema = param.get('schema', {})
                        if schema.get('type') == 'integer':
                            param_type = 'int'
                        elif schema.get('type') == 'boolean':
                            param_type = 'bool'
                        elif schema.get('type') == 'array':
                            param_type = 'List[str]'
                        if param.get('required', False):
                            params.append(f"{param_name}: {param_type}")
                        else:
                            params.append(f"{param_name}: Optional[{param_type}] = None")
                # Generate function
                func_code = f'''
async def {operation_id}({', '.join(params)}) -> Dict[str, Any]:
    """
    {summary}

    {description}

    Returns:
        API response data
    """
    logger.debug(f"Making {method.upper()} request to {path}")
    params = {{}}
    data = None
    # Add parameters to request
    {self._generate_param_assignments([p for p in operation.get('parameters', []) if p.get('in') != 'path'])}
    success, response = await make_api_request(
        "{path}",
        method="{method.upper()}",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {{response.get('error')}}")
        return {{"error": response.get('error', 'Request failed')}}
    return response
'''
                tool_code += func_code
            # Write the tool module
            tool_path = os.path.join(self.output_dir, 'tools', f'{module_name}.py')
            with open(tool_path, 'w', encoding='utf-8') as f:
                f.write(tool_code)
            logger.info(f"Generated tool module at {tool_path}")
        except Exception as e:
            logger.error(f"Error generating tool module for {path}: {str(e)}")
            raise

    def _generate_param_assignments(self, parameters: List[Dict[str, Any]]) -> str:
        """Generate parameter assignment code"""
        try:
            code = []
            for param in parameters:
                # Skip parameters without a name
                if 'name' not in param:
                    continue

                name = param['name']
                if param.get('in') == 'query':
                    code.append(f'if {name} is not None:\n        params["{name}"] = {name}')
                elif param.get('in') == 'path':
                    code.append(f'if {name} is not None:\n        path = path.replace("{{{name}}}", str({name}))')
                elif param.get('in') == 'body':
                    code.append(f'if {name} is not None:\n        data = {name}')
            return '\n'.join(code)
        except Exception as e:
            logger.error(f"Error generating parameter assignments: {str(e)}")
            raise

    def generate_server(self):
        """Generate the main server file"""
        try:
            # Collect all tool modules and their operationIds (skip any with '{' in the path)
            tool_modules = {}
            for path, path_item in self.spec.get('paths', {}).items():
                if '{' in path:
                    continue  # Skip endpoints with path parameters
                module_name = path.strip('/').replace('/', '_')
                if module_name not in tool_modules:
                    tool_modules[module_name] = set()
                for method, operation in path_item.items():
                    if method.lower() not in ['get', 'post', 'put', 'delete']:
                        continue
                    operation_id = operation.get('operationId')
                    if operation_id:
                        tool_modules[module_name].add(operation_id)
            # Get the base name from the MCP name (remove _mcp suffix)
            base_name = self.mcp_name.replace('_mcp', '')
            server_code = f'''#!/usr/bin/env python3\n"""\n{self.spec.get('info', {}).get('title', 'Generated')} MCP Server\n\nThis server provides a Model Context Protocol (MCP) interface to the {self.spec.get('info', {}).get('title', 'API')},\nallowing large language models and AI assistants to interact with the service.\n"""\nimport logging\nimport os\nfrom dotenv import load_dotenv\nfrom mcp.server.fastmcp import FastMCP\n\n# Import tools\n'''
            # Add individual tool imports
            for module in tool_modules:
                server_code += f'from mcp_{base_name}.tools import {module}\n'
            server_code += '''\n# Load environment variables\nload_dotenv()\n\n# Configure logging\nlogging.basicConfig(level=logging.DEBUG)\n\n# Create server instance\n'''
            # Use the API title for the server name
            server_code += f'mcp = FastMCP("{self.spec.get("info", {}).get("title", "Generated")} MCP Server")\n\n'
            server_code += '''# Register tools\n'''
            # Register the actual function names from operationId
            for module, operation_ids in tool_modules.items():
                server_code += f'# Register {module} tools\n'
                for op_id in operation_ids:
                    server_code += f'mcp.tool()({module}.{op_id})\n'
                server_code += '\n'
            server_code += '''\n# Start server when run directly\nif __name__ == "__main__":\n    mcp.run()\n'''
            server_path = os.path.join(self.output_dir, 'server.py')
            with open(server_path, 'w', encoding='utf-8') as f:
                f.write(server_code)
            logger.info(f"Generated server at {server_path}")
        except Exception as e:
            logger.error(f"Error generating server: {str(e)}")
            raise

    def generate_init_files(self):
        """Generate __init__.py files"""
        try:
            # Root init
            root_init = '''"""Generated MCP package."""

__version__ = "0.1.0"
'''
            root_init_path = os.path.join(self.output_dir, '__init__.py')
            with open(root_init_path, 'w', encoding='utf-8') as f:
                f.write(root_init)
            logger.debug(f"Generated {root_init_path}")

            # Tools init
            tools_init = '''"""Tools package."""

from . import *
'''
            tools_init_path = os.path.join(self.output_dir, 'tools', '__init__.py')
            with open(tools_init_path, 'w', encoding='utf-8') as f:
                f.write(tools_init)
            logger.debug(f"Generated {tools_init_path}")

            # Other init files
            init_content = '''"""Package module."""\n'''
            for dir_name in ['api', 'models', 'utils']:
                init_path = os.path.join(self.output_dir, dir_name, '__init__.py')
                with open(init_path, 'w', encoding='utf-8') as f:
                    f.write(init_content)
                logger.debug(f"Generated {init_path}")

            logger.info("Generated all __init__.py files")
        except Exception as e:
            logger.error(f"Error generating init files: {str(e)}")
            raise

    def generate_pyproject(self):
        """Generate pyproject.toml"""
        try:
            pyproject = f'''[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "mcp_{self.mcp_name}"
version = "0.1.0"
description = "Generated MCP server for {self.spec.get('info', {}).get('title', 'API')}"
authors = ["Your Name <your.email@example.com>"]
packages = [
    {{ include = "*.py" }},
]

[tool.poetry.dependencies]
python = ">=3.8.1,<4.0"
httpx = "^0.24.0"
python-dotenv = "^1.0.0"
pydantic = "^2.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0"
black = "^23.0"
isort = "^5.0"
flake8 = "^6.0"
'''

            pyproject_path = os.path.join(self.output_dir, 'pyproject.toml')
            with open(pyproject_path, 'w', encoding='utf-8') as f:
                f.write(pyproject)
            logger.info(f"Generated pyproject.toml at {pyproject_path}")
        except Exception as e:
            logger.error(f"Error generating pyproject.toml: {str(e)}")
            raise

    def generate(self):
        """Generate the complete MCP server"""
        try:
            logger.info("Starting MCP server generation")
            self.load_spec()
            self.create_directory_structure()
            self.generate_models()  # Generate models first
            self.generate_api_client()

            # Generate tool modules for each path
            for path, path_item in self.spec.get('paths', {}).items():
                self.generate_tool_module(path, path_item)

            self.generate_server()
            self.generate_init_files()
            self.generate_pyproject()

            # Create .env.example
            env_example = '''MCP_API_URL=https://example.com/api/v1
MCP_API_KEY=your_api_key_here
'''
            env_path = os.path.join(self.output_dir, '.env.example')
            with open(env_path, 'w', encoding='utf-8') as f:
                f.write(env_example)
            logger.info(f"Generated .env.example at {env_path}")

            # Create README.md
            readme = '''# Generated MCP Server

This is an automatically generated Model Context Protocol (MCP) server based on an OpenAPI specification.

## Prerequisites

- Python 3.8 or higher
- [Install Poetry](https://python-poetry.org/docs/#installation)
- Setup a virtual environment
```
poetry config virtualenvs.in-project true
poetry install
```


## Setup

1. Copy `.env.example` to `.env` and fill in your API credentials:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
poetry install
```

3. Run the server:

```bash
poetry run python -m server
```

## Available Tools

The following tools are available through the MCP server:

'''

            # Add tool documentation
            for path, path_item in self.spec.get('paths', {}).items():
                for method, operation in path_item.items():
                    if method.lower() in ['get', 'post', 'put', 'delete']:
                        summary = operation.get('summary', '')
                        description = operation.get('description', '')
                        readme += f'\n### {method.upper()} {path}\n'
                        readme += f'{summary}\n\n'
                        if description:
                            readme += f'{description}\n\n'

            readme_path = os.path.join(self.output_dir, 'README.md')
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme)
            logger.info(f"Generated README.md at {readme_path}")

            logger.info("MCP server generation completed successfully")
        except Exception as e:
            logger.error(f"Error generating MCP server: {str(e)}")
            raise

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate an MCP server from an OpenAPI specification')
    parser.add_argument('spec_path', help='Path to the OpenAPI specification JSON file')
    parser.add_argument('output_dir', help='Directory to generate the MCP server in')

    args = parser.parse_args()

    try:
        generator = MCPGenerator(args.spec_path, args.output_dir)
        generator.generate()
    except Exception as e:
        logger.error(f"Failed to generate MCP server: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()