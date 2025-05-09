#!/usr/bin/env python3
"""
MCP Generator Tool

This tool generates a Model Context Protocol (MCP) server from an OpenAPI specification.
It follows the same structure as the PagerDuty MCP server.
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import shutil

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
        
    def load_spec(self):
        """Load and parse the OpenAPI specification"""
        try:
            with open(self.openapi_spec_path, 'r') as f:
                self.spec = json.load(f)
            self.base_path = self.spec.get('servers', [{}])[0].get('url', '').rstrip('/')
            logger.info(f"Successfully loaded OpenAPI spec from {self.openapi_spec_path}")
            logger.info(f"Base URL: {self.base_path}")
        except FileNotFoundError:
            logger.error(f"OpenAPI spec file not found: {self.openapi_spec_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in OpenAPI spec file: {self.openapi_spec_path}")
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
            
    def generate_api_client(self):
        """Generate the API client module"""
        try:
            base_url = self.base_path or "https://api.example.com"
            client_code = f'''"""API client for making requests to the service"""

import logging
import os
from typing import Dict, Any, Tuple
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_api")

async def make_api_request(
    endpoint: str,
    method: str = "GET",
    params: Dict[str, Any] = None,
    data: Dict[str, Any] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    Make an API request to the service
    
    Args:
        endpoint: API endpoint to call
        method: HTTP method (GET, POST, PUT, DELETE)
        params: Query parameters
        data: Request body data
        
    Returns:
        Tuple of (success, response_data)
    """
    base_url = os.getenv("API_BASE_URL", "{base_url}")
    api_key = os.getenv("API_KEY")
    
    # Log environment variable status
    if api_key:
        logger.info("API_KEY found in environment variables")
    else:
        logger.error("API_KEY environment variable not set")
        return False, {{"error": "API key not configured"}}
        
    if base_url:
        logger.info(f"Using API base URL: {{base_url}}")
    else:
        logger.warning("API_BASE_URL not set, using default")
    
    headers = {{
        "Authorization": f"Bearer {{api_key}}",
        "Content-Type": "application/json"
    }}
    
    url = f"{{base_url}}/{{endpoint.lstrip('/')}}"
    logger.debug(f"Making request to: {{url}}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url,
                params=params,
                json=data,
                headers=headers
            ) as response:
                if response.status >= 400:
                    error_data = await response.json()
                    logger.error(f"API request failed: {{error_data}}")
                    return False, error_data
                    
                data = await response.json()
                return True, data
                
    except Exception as e:
        logger.error(f"API request failed: {{str(e)}}")
        return False, {{"error": str(e)}}
'''
            
            client_path = os.path.join(self.output_dir, 'api', 'client.py')
            with open(client_path, 'w') as f:
                f.write(client_code)
            logger.info(f"Generated API client at {client_path}")
        except Exception as e:
            logger.error(f"Error generating API client: {str(e)}")
            raise
            
    def generate_tool_module(self, path: str, operations: Dict[str, Any]):
        """Generate a tool module for a specific API path"""
        try:
            module_name = path.strip('/').replace('/', '_')
            tool_code = f'''"""Tools for {path} operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

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
                
                # Generate parameters
                params = []
                if 'parameters' in operation:
                    for param in operation['parameters']:
                        # Skip parameters without a name
                        if 'name' not in param:
                            logger.warning(f"Skipping parameter without name in {path} {method}")
                            continue
                            
                        param_name = param['name']
                        param_type = 'str'  # Default type
                        
                        # Get parameter type from schema
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
    {self._generate_param_assignments(operation.get('parameters', []))}
    
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
            with open(tool_path, 'w') as f:
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
                    code.append(f'if {name} is not None:\n    params["{name}"] = {name}')
                elif param.get('in') == 'path':
                    code.append(f'if {name} is not None:\n    path = path.replace("{{{name}}}", str({name}))')
                elif param.get('in') == 'body':
                    code.append(f'if {name} is not None:\n    data = {name}')
            return '\n'.join(code)
        except Exception as e:
            logger.error(f"Error generating parameter assignments: {str(e)}")
            raise
            
    def generate_server(self):
        """Generate the main server file"""
        try:
            # Collect all tool modules
            tool_modules = []
            for path, path_item in self.spec.get('paths', {}).items():
                module_name = path.strip('/').replace('/', '_')
                tool_modules.append(module_name)
                
            server_code = '''#!/usr/bin/env python3
"""
Generated MCP Server

This server provides a Model Context Protocol (MCP) interface to the API,
allowing large language models and AI assistants to interact with the service.
"""
import logging
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import tools
'''
            
            # Add imports
            for module in tool_modules:
                server_code += f'from .tools import {module}\n'
                
            server_code += '''
# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create server instance
mcp = FastMCP("Generated MCP Server")

# Register tools
'''
            
            # Add tool registrations
            for module in tool_modules:
                server_code += f'mcp.tool()({module}.{module})\n'
                
            server_code += '''
# Start server when run directly
if __name__ == "__main__":
    mcp.run()
'''
            
            server_path = os.path.join(self.output_dir, 'server.py')
            with open(server_path, 'w') as f:
                f.write(server_code)
            logger.info(f"Generated server at {server_path}")
        except Exception as e:
            logger.error(f"Error generating server: {str(e)}")
            raise
            
    def generate_init_files(self):
        """Generate __init__.py files"""
        try:
            init_content = '''"""Generated MCP package"""\n'''
            
            for dir_name in ['api', 'models', 'tools', 'utils']:
                init_path = os.path.join(self.output_dir, dir_name, '__init__.py')
                with open(init_path, 'w') as f:
                    f.write(init_content)
                logger.debug(f"Generated {init_path}")
                
            root_init_path = os.path.join(self.output_dir, '__init__.py')
            with open(root_init_path, 'w') as f:
                f.write(init_content)
            logger.info("Generated all __init__.py files")
        except Exception as e:
            logger.error(f"Error generating init files: {str(e)}")
            raise
            
    def generate_pyproject(self):
        """Generate pyproject.toml"""
        try:
            pyproject = '''[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "generated-mcp"
version = "0.1.0"
description = "Generated MCP server"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
fastmcp = "^0.1.0"
aiohttp = "^3.8.0"
python-dotenv = "^0.19.0"
pydantic = "^1.8.0"

[tool.poetry.group.dev.dependencies]
pytest = "^6.0"
black = "^21.0"
isort = "^5.0"
flake8 = "^3.9"
'''
            
            pyproject_path = os.path.join(self.output_dir, 'pyproject.toml')
            with open(pyproject_path, 'w') as f:
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
            self.generate_api_client()
            
            # Generate tool modules for each path
            for path, path_item in self.spec.get('paths', {}).items():
                self.generate_tool_module(path, path_item)
                
            self.generate_server()
            self.generate_init_files()
            self.generate_pyproject()
            
            # Create .env.example
            env_example = '''API_BASE_URL=https://api.example.com
API_KEY=your_api_key_here
'''
            env_path = os.path.join(self.output_dir, '.env.example')
            with open(env_path, 'w') as f:
                f.write(env_example)
            logger.info(f"Generated .env.example at {env_path}")
            
            # Create README.md
            readme = '''# Generated MCP Server

This is an automatically generated Model Context Protocol (MCP) server based on an OpenAPI specification.

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
            with open(readme_path, 'w') as f:
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