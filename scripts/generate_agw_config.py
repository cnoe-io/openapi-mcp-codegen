#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
Generate AgentGateway configuration from MCP config.yaml

This script reads the agentgateway section from config.yaml and generates
a properly formatted agw.yaml configuration file for AgentGateway.

Usage:
    python generate_agw_config.py <config.yaml> <output.yaml>
"""

import sys
import yaml
from pathlib import Path


def generate_agw_config(config_path: str, output_path: str):
    """
    Generate AgentGateway configuration from config.yaml

    Args:
        config_path: Path to config.yaml
        output_path: Path to output agw.yaml
    """
    # Load config.yaml
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Get agentgateway configuration
    agw_config = config.get('agentgateway', {})

    # Default values
    port = agw_config.get('port', 3000)
    backend = agw_config.get('backend', {})
    backend_host = backend.get('host', 'localhost')
    backend_port = backend.get('port', 2746)
    backend_path = backend.get('path', '/')

    cors_config = agw_config.get('cors', {})
    cors_enabled = cors_config.get('enabled', True)
    allow_origins = cors_config.get('allow_origins', ['*'])
    allow_methods = cors_config.get('allow_methods', ['GET', 'POST', 'OPTIONS'])
    allow_headers = cors_config.get('allow_headers', ['*'])
    expose_headers = cors_config.get('expose_headers', ['mcp-protocol-version', 'Content-Type', 'cache-control'])
    # maxAge must be a duration string (e.g., "3600s", "1h")
    max_age_raw = cors_config.get('max_age', 3600)
    if isinstance(max_age_raw, int):
        max_age = f"{max_age_raw}s"  # Convert integer to duration string
    else:
        max_age = str(max_age_raw)

    # Determine OpenAPI spec file to use
    # Prefer enhanced_openapi.json if it exists, otherwise use the original
    config_dir = Path(config_path).parent
    if (config_dir / 'enhanced_openapi.json').exists():
        openapi_file = 'enhanced_openapi.json'
    elif (config_dir / 'openapi.json').exists():
        openapi_file = 'openapi.json'
    else:
        # Try to find any OpenAPI file
        openapi_files = list(config_dir.glob('*openapi*.json'))
        if openapi_files:
            openapi_file = openapi_files[0].name
        else:
            openapi_file = 'openapi.json'  # Default
            print(f"Warning: No OpenAPI spec file found, using default: {openapi_file}", file=sys.stderr)

    # Build AgentGateway configuration
    agw_yaml = {
        'binds': [
            {
                'port': port,
                'listeners': [
                    {
                        'routes': [
                            {
                                'policies': {},
                                'backends': [
                                    {
                                        'mcp': {
                                            'targets': [
                                                {
                                                    'name': 'openapi',
                                                    'openapi': {
                                                        'schema': {
                                                            'file': openapi_file
                                                        },
                                                        'host': backend_host,
                                                        'port': backend_port,
                                                        'path': backend_path
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    # Add CORS if enabled
    if cors_enabled:
        agw_yaml['binds'][0]['listeners'][0]['routes'][0]['policies']['cors'] = {
            'allowOrigins': allow_origins,
            'allowMethods': allow_methods,
            'allowHeaders': allow_headers,
            'exposeHeaders': expose_headers,
            'maxAge': max_age
        }

    # Write output
    with open(output_path, 'w') as f:
        yaml.dump(agw_yaml, f, default_flow_style=False, sort_keys=False)

    print(f"Generated AgentGateway config: {output_path}")
    print(f"  Port: {port}")
    print(f"  Backend: {backend_host}:{backend_port}{backend_path}")
    print(f"  OpenAPI spec: {openapi_file}")
    print(f"  CORS enabled: {cors_enabled}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_agw_config.py <config.yaml> <output.yaml>")
        sys.exit(1)

    config_path = sys.argv[1]
    output_path = sys.argv[2]

    if not Path(config_path).exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    try:
        generate_agw_config(config_path, output_path)
    except Exception as e:
        print(f"Error generating AgentGateway config: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

