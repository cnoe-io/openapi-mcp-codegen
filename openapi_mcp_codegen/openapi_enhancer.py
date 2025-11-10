#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
OpenAPI MCP Enhancer

A unified enhancement pipeline that combines overlay generation, overlay application,
and MCP code generation for OpenAPI specifications. This module provides comprehensive
support for:

1. Generating AI-optimized overlays with LLM enhancement
2. Applying overlays to OpenAPI specifications
3. Converting Swagger 2.0 to OpenAPI 3.x with intelligent fixes
4. Generating production-ready MCP server code

Usage:
    python openapi_enhancer.py enhance <spec_path> <output_dir> <config_path> [options]
    python openapi_enhancer.py generate-overlay <spec_path> <overlay_path> [options]
    python openapi_enhancer.py apply-overlay <spec_path> <overlay_path> <output_path> [options]
"""

import argparse
import json
import logging
import tempfile
from ruamel.yaml import YAML
from pathlib import Path
import sys
import os
import re
from typing import Dict, Any, List, Optional, Union

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openapi_mcp_codegen.mcp_codegen import MCPGenerator
from openapi_mcp_codegen.validators import OpenAPIValidator, load_spec_file
from jinja2 import Environment, FileSystemLoader
import jsonpath_ng
from jsonpath_ng.ext import parse as jsonpath_parse

try:
    from cnoe_agent_utils import LLMFactory
    from langchain_core.messages import SystemMessage
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("openapi_enhancer")


class OpenAPIOverlayGenerator:
    """
    Generates OpenAPI Overlay specifications to enhance API documentation
    for better AI agent understanding and MCP server code generation.
    """

    def __init__(self, spec_path: str, use_llm: bool = False, llm_config: Optional[Dict] = None, overlay_config: Optional[Dict] = None):
        """
        Initialize the overlay generator.

        Args:
            spec_path: Path to the OpenAPI specification file
            use_llm: Whether to use LLM for generating enhanced descriptions
            llm_config: Configuration for LLM (if use_llm is True)
            overlay_config: Configuration for overlay enhancements from config.yaml
        """
        self.spec_path = spec_path
        self.spec = self._load_spec()
        self.prompts = self._load_prompts()  # Load declarative prompts

        # Load overlay configuration
        self.overlay_config = overlay_config or {}
        self.max_description_length = self.overlay_config.get('max_description_length', 300)
        self.enhance_crud = self.overlay_config.get('enhance_crud_operations', True)
        self.add_use_cases = self.overlay_config.get('add_use_cases', True)
        self.enhance_params = self.overlay_config.get('enhance_parameters', True)
        self.add_param_guidance = self.overlay_config.get('add_parameter_guidance', True)
        self.agentic_focus = self.overlay_config.get('agentic_focus', True)

        # Determine if LLM should be used - prefer LLM when available
        use_llm_from_config = self.overlay_config.get('use_llm', True)  # Default to True
        self.use_llm = (use_llm or use_llm_from_config) and LLM_AVAILABLE
        self.llm_config = llm_config or {}
        self.overlay_actions = []
        self.llm = None

        if self.use_llm:
            if not LLM_AVAILABLE:
                logger.warning("LLM enhancement requested but cnoe_agent_utils not available")
                self.use_llm = False
            else:
                try:
                    self.llm = LLMFactory().get_llm()
                    logger.info("LLM initialized for enhanced description generation")
                except Exception as e:
                    logger.warning(f"Failed to initialize LLM: {e}, falling back to rule-based generation")
                    self.use_llm = False

    def _load_spec(self) -> Dict[str, Any]:
        """Load the OpenAPI specification from file."""
        with open(self.spec_path, 'r') as f:
            if self.spec_path.endswith('.json'):
                return json.load(f)
            else:
                yaml = YAML(typ='safe', pure=True)
                return yaml.load(f)

    def _load_prompts(self) -> Dict[str, Any]:
        """Load prompt templates from prompt.yaml"""
        prompt_file = Path(__file__).parent / 'prompt.yaml'
        try:
            with open(prompt_file, 'r') as f:
                yaml = YAML(typ='safe', pure=True)
                return yaml.load(f)
        except Exception as e:
            logger.warning(f"Failed to load prompt.yaml: {e}, using defaults")
            return {}

    def _get_operation_purpose(self, method: str, path: str, operation: Dict[str, Any]) -> str:
        """
        Determine the purpose of an API operation based on its method, path, and metadata.

        Args:
            method: HTTP method (get, post, put, delete, etc.)
            path: API path
            operation: Operation object from OpenAPI spec

        Returns:
            A human-readable purpose description
        """
        operation_id = operation.get('operationId', '')
        summary = operation.get('summary', '')

        # Extract resource from path
        path_parts = [p for p in path.split('/') if p and not p.startswith('{')]
        resource = path_parts[-1] if path_parts else 'resource'

        # Determine action based on HTTP method and operation ID
        method_lower = method.lower()
        op_id_lower = operation_id.lower()

        if method_lower == 'get':
            if '{' in path and path.count('{') == 1:
                return f"Retrieve details of a specific {resource}"
            elif 'list' in op_id_lower or not '{' in path:
                return f"List or query {resource}"
            else:
                return f"Retrieve {resource} information"

        elif method_lower == 'post':
            if 'create' in op_id_lower:
                return f"Create a new {resource}"
            elif 'search' in op_id_lower or 'query' in op_id_lower:
                return f"Search or query {resource}"
            else:
                return f"Perform an operation on {resource}"

        elif method_lower == 'put':
            return f"Update or replace a {resource}"

        elif method_lower == 'patch':
            return f"Partially update a {resource}"

        elif method_lower == 'delete':
            return f"Delete a {resource}"

        return summary or f"Perform {method.upper()} operation on {path}"

    def _create_enhanced_description_with_llm(self, method: str, path: str, operation: Dict[str, Any], validator: Optional['OpenAPIValidator'] = None) -> str:
        """
        Create an enhanced description using LLM with declarative prompts from prompt.yaml.

        Args:
            method: HTTP method
            path: API path
            operation: Operation object

        Returns:
            LLM-generated enhanced description
        """
        if not self.llm:
            return self._create_enhanced_description(method, path, operation)

        try:
            # Get prompts from declarative configuration
            op_desc_prompts = self.prompts.get('operation_description', {})
            system_prompt = op_desc_prompts.get('system_prompt', '')
            user_template = op_desc_prompts.get('user_prompt_template', '')

            # Fallback to default if prompts not loaded
            if not system_prompt:
                logger.warning("No system prompt loaded from prompt.yaml, using fallback")
                return self._create_enhanced_description(method, path, operation)

            # Extract operation details
            original_desc = operation.get('description', '')
            summary = operation.get('summary', '')
            operation_id = operation.get('operationId', '')
            parameters = operation.get('parameters', [])
            has_body = 'requestBody' in operation

            # Separate path and query parameters
            path_params = [p.get('name') for p in parameters if p.get('in') == 'path']
            query_params = [p.get('name') for p in parameters if p.get('in') == 'query']

            # Format user prompt with template variables
            user_prompt = user_template.format(
                method=method.upper(),
                path=path,
                operation_id=operation_id or 'None',
                summary=summary or 'None',
                description=original_desc[:200] if original_desc else 'None',
                path_params=', '.join(path_params) if path_params else 'None',
                query_params=', '.join(query_params) if query_params else 'None',
                has_body='Yes' if has_body else 'No'
            )

            # Call LLM
            system_msg = SystemMessage(content=system_prompt.strip())
            user_msg = SystemMessage(content=user_prompt.strip())
            response = self.llm.invoke([system_msg, user_msg])
            enhanced_desc = response.content.strip()

            # Track token usage if validator is provided
            if validator:
                input_tokens, output_tokens = validator.extract_token_usage(response)
                validator.add_generation_tokens(input_tokens, output_tokens)
                logger.debug(f"LLM tokens used: {input_tokens} input, {output_tokens} output")

            # Note: We preserve full LLM-enhanced descriptions for AI agents
            # No truncation - AI agents need complete context

            logger.debug(f"LLM enhanced description for {method.upper()} {path}")
            return enhanced_desc

        except Exception as e:
            logger.warning(f"LLM enhancement failed for {method} {path}: {e}, falling back to rule-based")
            return self._create_enhanced_description(method, path, operation)

    def _create_enhanced_description(self, method: str, path: str, operation: Dict[str, Any]) -> str:
        """
        Create an enhanced, agent-friendly description for an API operation (rule-based fallback).
        Formatted for OpenAI tool/function calling compatibility.

        Args:
            method: HTTP method
            path: API path
            operation: Operation object from OpenAPI spec

        Returns:
            Enhanced description string in OpenAI-compatible format
        """
        original_desc = operation.get('description', '')
        summary = operation.get('summary', '')
        purpose = self._get_operation_purpose(method, path, operation)

        # Start with clear, concise purpose (OpenAI prefers brief descriptions)
        enhanced_parts = [purpose]

        # Add use cases in a concise format
        use_cases = self._generate_use_cases(method, path, operation)
        if use_cases:
            # Pick the most relevant use case
            enhanced_parts.append(f" Use when: {use_cases[0].lower()}")

        # Add parameter hints if critical
        parameters = operation.get('parameters', [])
        required_params = [p for p in parameters if p.get('required', False)]
        if required_params:
            param_names = [p.get('name', 'unknown') for p in required_params]
            if len(param_names) <= 3:  # Only mention if few required params
                enhanced_parts.append(f". Required: {', '.join(param_names)}")

        # Keep it under 300 characters for OpenAI (recommended limit)
        description = ''.join(enhanced_parts)
        if len(description) > 300:
            description = description[:297] + "..."

        return description

    def _generate_use_cases(self, method: str, path: str, operation: Dict[str, Any]) -> List[str]:
        """
        Generate common use cases for an operation based on its characteristics.

        Args:
            method: HTTP method
            path: API path
            operation: Operation object

        Returns:
            List of use case descriptions
        """
        use_cases = []
        op_id = operation.get('operationId', '').lower()
        method_lower = method.lower()

        # Pattern-based use case generation
        if 'list' in op_id and method_lower == 'get':
            use_cases.append("When you need to discover available resources or check what exists")
            use_cases.append("To monitor or audit resource states across the system")

        if 'get' in op_id and '{' in path:
            use_cases.append("When you have a specific resource identifier and need its current details")
            use_cases.append("To verify the state or configuration of a particular resource")

        if 'create' in op_id or method_lower == 'post':
            use_cases.append("When initializing new resources based on user requirements")
            use_cases.append("To provision resources as part of a workflow or automation")

        if 'update' in op_id or method_lower in ['put', 'patch']:
            use_cases.append("When modifying existing resource configurations or properties")
            use_cases.append("To fix issues or adjust settings based on changing requirements")

        if 'delete' in op_id or method_lower == 'delete':
            use_cases.append("When cleaning up resources that are no longer needed")
            use_cases.append("To remove failed or obsolete resources")

        if 'log' in path or 'log' in op_id:
            use_cases.append("For debugging issues or understanding resource behavior")
            use_cases.append("When investigating errors or tracking execution history")

        if 'status' in path or 'status' in op_id:
            use_cases.append("To check the health or state of resources")
            use_cases.append("When monitoring progress or waiting for operations to complete")

        return use_cases[:3]  # Limit to top 3 use cases

    def _enhance_parameter_description(self, param: Dict[str, Any]) -> str:
        """
        Enhance a parameter description with agent-friendly information (rule-based fallback).
        Formatted for OpenAI tool/function calling compatibility - concise and clear.

        Args:
            param: Parameter object

        Returns:
            Enhanced description in OpenAI-compatible format
        """
        name = param.get('name', '')
        original_desc = param.get('description', '')
        param_type = param.get('type', param.get('schema', {}).get('type', 'string'))
        required = param.get('required', False)

        # Start with original description if exists - NEVER truncate
        if original_desc:
            cleaned = ' '.join(original_desc.split())
            # Always preserve the full original description
            parts = [cleaned]
        else:
            parts = []

        # Add concise pattern-based guidance
        name_lower = name.lower()
        if any(kw in name_lower for kw in ['namespace', 'ns']):
            if not parts:
                parts.append("Kubernetes namespace to scope the operation")
        elif any(kw in name_lower for kw in ['limit', 'max']):
            if not parts:
                parts.append("Maximum number of results to return")
        elif any(kw in name_lower for kw in ['offset', 'skip', 'continue']):
            if not parts:
                parts.append("Pagination token or offset for retrieving more results")
        elif 'selector' in name_lower or 'filter' in name_lower:
            if not parts:
                parts.append("Filter to narrow results based on labels or fields")
        elif 'name' in name_lower and 'prefix' not in name_lower:
            if not parts:
                parts.append("Name of the resource to operate on")

        # If still no description, provide a generic one
        if not parts:
            if required:
                parts.append(f"Required {param_type} parameter")
            else:
                parts.append(f"Optional {param_type} parameter")

        # Build complete enhanced description for AI agents
        description = ' '.join(parts)
        return description

    def generate_overlay(self, validator: Optional['OpenAPIValidator'] = None) -> Dict[str, Any]:
        """
        Generate the complete overlay specification.

        Returns:
            Overlay specification as a dictionary
        """
        logger.info(f"Generating overlay for OpenAPI spec: {self.spec_path}")

        # Initialize overlay structure
        spec_title = self.spec.get('info', {}).get('title', 'API')
        overlay = {
            'overlay': '1.0.0',
            'info': {
                'title': f'MCP Agent Enhancement Overlay for {spec_title}',
                'version': '1.0.0',
                'description': (
                    'This overlay enhances the OpenAPI specification with agent-friendly '
                    'descriptions, use cases, and guidance to improve MCP server tool generation '
                    'and AI agent understanding.'
                )
            },
            'actions': []
        }

        # Process all paths and operations
        paths = self.spec.get('paths', {})
        operations_count = 0

        for path, path_item in paths.items():
            for method in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
                if method not in path_item:
                    continue

                operation = path_item[method]
                operations_count += 1

                # Enhance operation description
                if self.use_llm:
                    enhanced_desc = self._create_enhanced_description_with_llm(method, path, operation, validator)
                else:
                    enhanced_desc = self._create_enhanced_description(method, path, operation)

                overlay['actions'].append({
                    'target': f"$.paths['{path}'].{method}.description",
                    'update': enhanced_desc
                })

                # Enhance operation summary if missing or too brief
                summary = operation.get('summary', '')
                if not summary or len(summary) < 20:
                    purpose = self._get_operation_purpose(method, path, operation)
                    overlay['actions'].append({
                        'target': f"$.paths['{path}'].{method}.summary",
                        'update': purpose
                    })

                # Enhance parameter descriptions for AI agents
                parameters = operation.get('parameters', [])
                for idx, param in enumerate(parameters):
                    if '$ref' in param:
                        continue  # Skip refs for now

                    enhanced_param_desc = self._enhance_parameter_description(param)
                    overlay['actions'].append({
                        'target': f"$.paths['{path}'].{method}.parameters[{idx}].description",
                        'update': enhanced_param_desc
                    })

        # Update validator metrics if provided
        if validator:
            validator.metrics.operations_processed = operations_count
            validator.metrics.overlay_actions_applied = len(overlay['actions'])

        logger.info(f"Generated {len(overlay['actions'])} overlay actions")
        return overlay


class OverlayApplier:
    """
    Applies OpenAPI Overlay specifications to OpenAPI documents.
    Implements the Overlay Specification 1.0.0.
    """

    def __init__(self, openapi_path: str, overlay_path: str):
        """
        Initialize the overlay applier.

        Args:
            openapi_path: Path to the OpenAPI specification file
            overlay_path: Path to the overlay specification file
        """
        self.openapi_path = openapi_path
        self.overlay_path = overlay_path
        self.openapi = self._load_file(openapi_path)
        self.overlay = self._load_file(overlay_path)

    def _load_file(self, path: str) -> Dict[str, Any]:
        """Load a YAML or JSON file."""
        with open(path, 'r') as f:
            if path.endswith('.json'):
                return json.load(f)
            else:
                yaml = YAML(typ='safe', pure=True)
                return yaml.load(f)

    def _set_nested_value(self, obj: Any, path_parts: List[str], value: Any) -> None:
        """
        Set a nested value in a dictionary/list structure.

        Args:
            obj: The object to modify
            path_parts: List of path components
            value: The value to set
        """
        if not path_parts:
            return

        current = obj
        for i, part in enumerate(path_parts[:-1]):
            # Handle array index
            if part.isdigit():
                idx = int(part)
                if isinstance(current, list):
                    while len(current) <= idx:
                        current.append({})
                    current = current[idx]
            else:
                # Handle dictionary key
                if part not in current:
                    # Determine if next part is an array index
                    next_part = path_parts[i + 1]
                    current[part] = [] if next_part.isdigit() else {}
                current = current[part]

        # Set the final value
        last_part = path_parts[-1]
        if last_part.isdigit():
            idx = int(last_part)
            if isinstance(current, list):
                while len(current) <= idx:
                    current.append(None)
                current[idx] = value
        else:
            current[last_part] = value

    def _parse_jsonpath_target(self, target: str) -> List[tuple]:
        """
        Parse a JSONPath target and return matching paths.

        Args:
            target: JSONPath expression

        Returns:
            List of (path_parts, current_value) tuples
        """
        try:
            # Use jsonpath-ng for more complex expressions
            expr = jsonpath_parse(target)
            matches = expr.find(self.openapi)
            results = []

            for match in matches:
                # Convert the path to a list of parts
                path_str = str(match.full_path)
                # Parse the path string into components
                parts = []
                for component in path_str.split('.'):
                    # Handle array indices
                    if '[' in component and ']' in component:
                        key = component.split('[')[0]
                        if key:
                            parts.append(key)
                        # Extract indices
                        indices = component.split('[')[1:]
                        for idx_str in indices:
                            idx = idx_str.rstrip(']').strip('"').strip("'")
                            parts.append(idx)
                    else:
                        parts.append(component)

                results.append((parts, match.value))

            return results
        except Exception as e:
            logger.warning(f"Failed to parse JSONPath '{target}': {e}")
            # Fallback to simple path parsing
            simple_path = target.replace('$.', '').replace('[', '.').replace(']', '').replace("'", "").replace('"', '')
            parts = [p for p in simple_path.split('.') if p]
            return [(parts, None)]

    def apply_action(self, action: Dict[str, Any]) -> None:
        """
        Apply a single overlay action to the OpenAPI document.

        Args:
            action: The action object from the overlay
        """
        target = action.get('target')
        if not target:
            logger.warning("Action missing 'target' field, skipping")
            return

        # Handle update action
        if 'update' in action:
            update_value = action['update']
            matches = self._parse_jsonpath_target(target)

            if matches:
                # Update existing paths
                for path_parts, current_value in matches:
                    logger.debug(f"Updating {'.'.join(path_parts)} with new value")
                    self._set_nested_value(self.openapi, path_parts, update_value)
            else:
                # Path doesn't exist, create it
                # Parse the target as a simple path
                simple_path = target.replace('$.', '').replace('[', '.').replace(']', '').replace("'", "").replace('"', '')
                parts = [p for p in simple_path.split('.') if p]
                logger.debug(f"Creating new path {'.'.join(parts)} with value")
                self._set_nested_value(self.openapi, parts, update_value)

    def apply_overlay(self) -> Dict[str, Any]:
        """
        Apply all actions from the overlay to the OpenAPI document.

        Returns:
            The modified OpenAPI document
        """
        overlay_version = self.overlay.get('overlay')
        if not overlay_version or not overlay_version.startswith('1.0'):
            logger.warning(f"Unexpected overlay version: {overlay_version}")

        actions = self.overlay.get('actions', [])
        logger.info(f"Applying {len(actions)} overlay actions")

        for idx, action in enumerate(actions):
            try:
                self.apply_action(action)
            except Exception as e:
                logger.error(f"Error applying action {idx}: {e}", exc_info=True)

        logger.info("Overlay application complete")
        return self.openapi


class OpenAPIEnhancer:
    """
    Main orchestrator for OpenAPI enhancement pipeline.
    Combines overlay generation, application, and MCP code generation.
    """

    def __init__(self, spec_path: str, config_path: Optional[str] = None):
        """
        Initialize the OpenAPI enhancer.

        Args:
            spec_path: Path to the OpenAPI specification file
            config_path: Path to configuration file (optional)
        """
        self.spec_path = spec_path
        self.config_path = config_path
        self.config = self._load_config() if config_path else {}
        self.validator = OpenAPIValidator()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                yaml = YAML(typ='safe', pure=True)
                return yaml.load(f)
        except Exception as e:
            logger.warning(f"Could not load config: {e}, using defaults")
            return {}

    def _fix_openapi_parameters(self, spec_path: str) -> int:
        """
        Fix OpenAPI parameters that are missing schema or content fields.

        According to OpenAPI 3.x spec, parameters must have either a 'schema' or
        'content' field to define their type. This function adds default schemas
        to parameters that are missing both.

        Also removes invalid 'body' parameters (OpenAPI 2.0 style) as they should
        be defined in requestBody instead.

        Additionally, converts Swagger 2.0 specs to OpenAPI 3.x format.

        Args:
            spec_path: Path to the OpenAPI specification file to fix

        Returns:
            Number of parameters that were fixed
        """
        try:
            # Load the OpenAPI spec
            with open(spec_path, 'r', encoding='utf-8') as f:
                spec = json.load(f)

            # Check if this is a Swagger 2.0 spec and convert to OpenAPI 3.x
            if 'swagger' in spec and spec.get('swagger') == '2.0':
                logger.info("Detected Swagger 2.0 spec, converting to OpenAPI 3.0")
                spec['openapi'] = '3.0.0'
                del spec['swagger']
                # basePath and schemes should be converted to servers
                base_path = spec.pop('basePath', '')
                schemes = spec.pop('schemes', ['https'])
                host = spec.pop('host', 'localhost')
                if 'servers' not in spec or not spec['servers']:
                    spec['servers'] = [{
                        'url': f"{schemes[0]}://{host}{base_path}"
                    }]

            fixed_count = 0
            removed_body_params = 0

            # Process all parameters in all operations
            for path, methods in spec.get('paths', {}).items():
                for method, operation in methods.items():
                    if method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                        if 'parameters' in operation:
                            # First pass: remove invalid 'body' parameters
                            # In OpenAPI 3.x, body parameters should be in requestBody, not parameters
                            original_params = operation['parameters']
                            operation['parameters'] = [
                                p for p in original_params
                                if p.get('in') != 'body'
                            ]
                            body_params_removed = len(original_params) - len(operation['parameters'])
                            if body_params_removed > 0:
                                removed_body_params += body_params_removed
                                logger.debug(f"Removed {body_params_removed} body parameter(s) from {method.upper()} {path}")

                            # Second pass: fix parameters missing schema
                            for param in operation['parameters']:
                                # If parameter has neither schema nor content, add a default schema
                                if 'schema' not in param and 'content' not in param:
                                    param_name = param.get('name', '').lower()
                                    param_in = param.get('in', '')

                                    # Infer type from parameter name and location
                                    if any(word in param_name for word in [
                                        'limit', 'timeout', 'seconds', 'nanos', 'period',
                                        'retries', 'count', 'size', 'port', 'lines', 'bytes'
                                    ]):
                                        param['schema'] = {'type': 'integer'}
                                    elif any(word in param_name for word in [
                                        'watch', 'follow', 'previous', 'timestamps', 'orphan',
                                        'force', 'enabled', 'allow', 'skip', 'insecure', 'stream'
                                    ]):
                                        param['schema'] = {'type': 'boolean'}
                                    else:
                                        # Default to string type
                                        param['schema'] = {'type': 'string'}

                                    # Remove old Swagger 2.0 'type' field after adding OpenAPI 3.x 'schema'
                                    if 'type' in param:
                                        del param['type']
                                        logger.debug(f"Removed Swagger 2.0 'type' field from parameter '{param.get('name')}'")

                                    fixed_count += 1
                                    logger.debug(f"Fixed parameter '{param.get('name')}' in {method.upper()} {path}")

            # Save the fixed spec
            total_fixes = fixed_count + removed_body_params
            if total_fixes > 0:
                with open(spec_path, 'w', encoding='utf-8') as f:
                    json.dump(spec, f, indent=2)
                if fixed_count > 0:
                    logger.info(f"Fixed {fixed_count} parameters missing schema definitions")
                if removed_body_params > 0:
                    logger.info(f"Removed {removed_body_params} invalid 'body' parameters (OpenAPI 2.0 style)")

            return total_fixes

        except Exception as e:
            logger.error(f"Error fixing OpenAPI parameters: {e}")
            raise

    def _generate_example_makefile(self, mcp_generator: MCPGenerator):
        """
        Generate a Makefile in the same directory as the OpenAPI spec.

        Args:
            mcp_generator: The MCPGenerator instance with configuration
        """
        try:
            spec_dir = Path(self.spec_path).parent
            makefile_path = spec_dir / "Makefile"

            # Get template directory
            template_dir = Path(__file__).parent / 'templates'
            env = Environment(loader=FileSystemLoader(str(template_dir)))

            # Load template
            template = env.get_template('example_makefile.tpl')

            # Render with context
            content = template.render(
                mcp_name=mcp_generator.mcp_name,
                generate_agent=mcp_generator.generate_agent_flag,
                generate_eval=mcp_generator.generate_eval,
                enable_slim=mcp_generator.enable_slim
            )

            # Write Makefile
            with open(makefile_path, 'w') as f:
                f.write(content)

            logger.info(f"Generated Makefile at: {makefile_path}")
            print(f"✓ Generated Makefile: {makefile_path}")

        except Exception as e:
            logger.warning(f"Failed to generate Makefile: {e}")
            # Don't fail the whole process if Makefile generation fails

    def _generate_agentgateway_config(self, enhanced_spec_path: str, output_dir: str):
        """
        Generate agent gateway configuration YAML file.

        Args:
            enhanced_spec_path: Path to the enhanced OpenAPI specification
            output_dir: Directory where MCP server code was generated
        """
        try:
            spec_dir = Path(self.spec_path).parent
            spec_filename = Path(enhanced_spec_path).name
            gateway_config_path = spec_dir / f"{Path(self.spec_path).stem}-agentgateway.yaml"

            # Determine the host from the enhanced spec
            host = "localhost:8080"  # Default
            try:
                yaml_loader = YAML(typ='safe', pure=True)
                with open(enhanced_spec_path, 'r') as f:
                    if enhanced_spec_path.endswith('.json'):
                        import json
                        spec_data = json.load(f)
                    else:
                        spec_data = yaml_loader.load(f)

                # Extract host from servers or fallback to info
                if 'servers' in spec_data and spec_data['servers']:
                    server_url = spec_data['servers'][0].get('url', '')
                    if '://' in server_url:
                        host = server_url.split('://')[-1]
                    else:
                        host = server_url.lstrip('/')
                elif 'host' in spec_data:
                    host = spec_data['host']
            except Exception as e:
                logger.debug(f"Could not extract host from spec, using default: {e}")

            # Generate agent gateway configuration
            gateway_config = {
                'binds': [{
                    'port': 3000,
                    'listeners': [{
                        'routes': [{
                            'backends': [{
                                'mcp': {
                                    'targets': [{
                                        'name': 'openapi',
                                        'openapi': {
                                            'schema': {
                                                'file': spec_filename
                                            },
                                            'host': host
                                        }
                                    }]
                                }
                            }],
                            'policies': {
                                'cors': {
                                    'allowOrigins': ['*'],
                                    'allowHeaders': ['*']
                                }
                            }
                        }]
                    }]
                }]
            }

            # Write agent gateway config
            with open(gateway_config_path, 'w') as f:
                yaml_writer = YAML()
                yaml_writer.dump(gateway_config, f)

            logger.info(f"Generated agent gateway config at: {gateway_config_path}")
            print(f"✓ Generated agent gateway config: {gateway_config_path}")

        except Exception as e:
            logger.warning(f"Failed to generate agent gateway config: {e}")
            # Don't fail the whole process if config generation fails

    def enhance_and_generate(self, output_dir: str,
                           save_overlay: Optional[str] = None,
                           save_enhanced_spec: Optional[str] = None,
                           skip_overlay: bool = False,
                           overlay_only: bool = False,
                           format: str = 'yaml') -> bool:
        """
        Main enhancement pipeline.

        Args:
            output_dir: Output directory for MCP server code
            save_overlay: Path to save generated overlay (optional)
            save_enhanced_spec: Path to save enhanced spec (optional)
            skip_overlay: Skip overlay generation
            overlay_only: Only generate overlay, skip MCP generation
            format: Output format for overlay ('yaml' or 'json')

        Returns:
            True if successful, False otherwise
        """
        try:
            # Initialize validation session
            self.validator.start_validation_session(self.spec_path)
            original_spec = load_spec_file(self.spec_path)

            enhanced_spec_path = self.spec_path
            overlay_path = None

            # Step 1: Generate overlay (unless skipped)
            if not skip_overlay:
                logger.info("=" * 70)
                logger.info("STEP 1: Generating OpenAPI Overlay")
                logger.info("=" * 70)

                overlay_config = self.config.get('overlay_enhancements', {})
                if overlay_config.get('enabled', True):
                    logger.info("Using overlay enhancement configuration from config.yaml")

                generator = OpenAPIOverlayGenerator(
                    spec_path=self.spec_path,
                    overlay_config=overlay_config
                )

                # Save overlay to specified path or temporary file
                if save_overlay:
                    overlay_path = save_overlay
                else:
                    # Create temporary overlay file
                    temp_overlay = tempfile.NamedTemporaryFile(
                        mode='w',
                        suffix='.yaml',
                        delete=False
                    )
                    overlay_path = temp_overlay.name
                    temp_overlay.close()

                overlay = generator.generate_overlay(self.validator)
                with open(overlay_path, 'w') as f:
                    if format == 'json':
                        json.dump(overlay, f, indent=2)
                    else:
                        yaml = YAML()
                        yaml.dump(overlay, f)

                print(f"✓ Generated overlay: {overlay_path}")

                # Step 2: Apply overlay
                logger.info("")
                logger.info("=" * 70)
                logger.info("STEP 2: Applying Overlay to OpenAPI Spec")
                logger.info("=" * 70)

                # Save enhanced spec to specified path or temporary file
                if save_enhanced_spec:
                    enhanced_spec_path = save_enhanced_spec
                else:
                    # Create temporary enhanced spec file
                    temp_spec = tempfile.NamedTemporaryFile(
                        mode='w',
                        suffix='.json',
                        delete=False
                    )
                    enhanced_spec_path = temp_spec.name
                    temp_spec.close()

                applier = OverlayApplier(self.spec_path, overlay_path)
                enhanced_spec = applier.apply_overlay()

                with open(enhanced_spec_path, 'w') as f:
                    json.dump(enhanced_spec, f, indent=2)

                print(f"✓ Applied overlay, enhanced spec: {enhanced_spec_path}")

                # Fix OpenAPI parameters that may be missing schema definitions
                logger.info("")
                logger.info("=" * 70)
                logger.info("STEP 2.1: Validating and Fixing OpenAPI Parameters")
                logger.info("=" * 70)

                fixed_count = self._fix_openapi_parameters(enhanced_spec_path)
                if fixed_count > 0:
                    print(f"✓ Fixed {fixed_count} parameters with missing schema definitions")
                else:
                    print(f"✓ All parameters are valid")

                # Clean up temporary overlay if not saved
                if not save_overlay:
                    Path(overlay_path).unlink(missing_ok=True)

                # Step 2.2: Run ADR-005 Compliance Validation
                logger.info("")
                logger.info("=" * 70)
                logger.info("STEP 2.2: ADR-005 Compliance Validation")
                logger.info("=" * 70)

                enhanced_spec = load_spec_file(enhanced_spec_path)
                self.validator.end_validation_session(enhanced_spec_path)

                # Run validation suite
                validation_results = self.validator.run_full_validation_suite(original_spec, enhanced_spec)

                # Generate and display report
                validation_report = self.validator.generate_validation_report(validation_results)
                print(validation_report)

                # Check if all validations passed
                all_passed = all(result.passed for result in validation_results.values())
                if not all_passed:
                    logger.warning("Some ADR-005 requirements not met - see validation report above")
                else:
                    logger.info("✅ All ADR-005 requirements satisfied!")

            # Step 3: Generate MCP server code (unless overlay-only mode)
            if not overlay_only:
                logger.info("")
                logger.info("=" * 70)
                logger.info("STEP 3: Generating MCP Server Code")
                logger.info("=" * 70)

                generate_agent = self.config.get('generate_agent', False)
                generate_eval = self.config.get('generate_eval', False)
                enable_slim = self.config.get('enable_slim', False)
                with_a2a_proxy = self.config.get('with_a2a_proxy', False)

                script_dir = Path(__file__).parent.parent / 'openapi_mcp_codegen'

                # Use a default config if none provided
                config_path_to_use = self.config_path
                if not config_path_to_use:
                    # Look for config.yaml in the same directory as the spec
                    spec_dir = Path(self.spec_path).parent
                    default_config = spec_dir / 'config.yaml'
                    if default_config.exists():
                        config_path_to_use = str(default_config)
                    else:
                        # Create a minimal config
                        config_path_to_use = str(spec_dir / 'config.yaml')
                        minimal_config = {
                            'title': 'Generated MCP Server',
                            'description': 'Auto-generated MCP server from OpenAPI specification',
                            'version': '1.0.0'
                        }
                        with open(config_path_to_use, 'w') as f:
                            yaml = YAML()
                            yaml.dump(minimal_config, f)

                mcp_generator = MCPGenerator(
                    script_dir=str(script_dir),
                    spec_path=enhanced_spec_path,
                    output_dir=output_dir,
                    config_path=config_path_to_use,
                    generate_agent=generate_agent,
                    generate_eval=generate_eval,
                    enable_slim=enable_slim,
                    with_a2a_proxy=with_a2a_proxy
                )
                mcp_generator.generate()
                print(f"✓ Generated MCP server code in: {output_dir}")

                # Generate example Makefile at the spec directory level
                self._generate_example_makefile(mcp_generator)

                # Generate agent gateway configuration
                self._generate_agentgateway_config(enhanced_spec_path, output_dir)

                # Clean up temporary enhanced spec if not saved
                if not skip_overlay and not save_enhanced_spec:
                    Path(enhanced_spec_path).unlink(missing_ok=True)

            logger.info("")
            logger.info("=" * 70)
            logger.info("✓ ALL STEPS COMPLETED SUCCESSFULLY")
            logger.info("=" * 70)

            if overlay_only:
                print("\nNext steps:")
                print(f"  1. Review the enhanced spec: {enhanced_spec_path}")
                print(f"  2. Generate MCP code with: python -m openapi_mcp_codegen.openapi_enhancer enhance \\")
                print(f"       {enhanced_spec_path} {output_dir} --config {self.config_path}")
            elif not save_enhanced_spec:
                print("\nNote: Intermediate enhanced spec was cleaned up.")
                print("      Use --save-enhanced-spec to keep it for inspection.")

            return True

        except Exception as e:
            logger.error(f"Error in enhancement pipeline: {e}", exc_info=True)
            print(f"\n✗ Error: {e}", file=sys.stderr)
            return False


def main():
    """Main CLI interface for OpenAPI enhancer."""
    parser = argparse.ArgumentParser(
        description='OpenAPI MCP Enhancer - Unified enhancement pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  enhance          Complete enhancement pipeline (overlay + MCP generation)
  generate-overlay Generate overlay specification only
  apply-overlay    Apply overlay to OpenAPI specification only
  validate         Run ADR-005 compliance validation on existing enhanced spec

Examples:
  # Complete enhancement pipeline
  python openapi_enhancer.py enhance spec.json output/ config.yaml

  # Generate overlay only
  python openapi_enhancer.py generate-overlay spec.json overlay.yaml

  # Apply existing overlay
  python openapi_enhancer.py apply-overlay spec.json overlay.yaml enhanced_spec.json

  # Validate existing enhanced spec
  python openapi_enhancer.py validate original.json enhanced.json
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Enhance command (main pipeline)
    enhance_parser = subparsers.add_parser('enhance', help='Complete enhancement pipeline')
    enhance_parser.add_argument('spec_path', help='Path to OpenAPI specification file')
    enhance_parser.add_argument('output_dir', help='Output directory for MCP server code')
    enhance_parser.add_argument('--config', help='Path to configuration file')
    enhance_parser.add_argument('--save-overlay', metavar='PATH', help='Save generated overlay to path')
    enhance_parser.add_argument('--save-enhanced-spec', metavar='PATH', help='Save enhanced spec to path')
    enhance_parser.add_argument('--skip-overlay', action='store_true', help='Skip overlay generation')
    enhance_parser.add_argument('--overlay-only', action='store_true', help='Only generate overlay')
    enhance_parser.add_argument('--format', choices=['yaml', 'json'], default='yaml', help='Overlay format')

    # Generate overlay command
    overlay_parser = subparsers.add_parser('generate-overlay', help='Generate overlay only')
    overlay_parser.add_argument('spec_path', help='Path to OpenAPI specification file')
    overlay_parser.add_argument('output_path', help='Path for output overlay file')
    overlay_parser.add_argument('--config', help='Path to configuration file')
    overlay_parser.add_argument('--format', choices=['yaml', 'json'], default='yaml', help='Output format')
    overlay_parser.add_argument('--use-llm', action='store_true', help='Use LLM for enhanced descriptions')

    # Apply overlay command
    apply_parser = subparsers.add_parser('apply-overlay', help='Apply overlay only')
    apply_parser.add_argument('spec_path', help='Path to OpenAPI specification file')
    apply_parser.add_argument('overlay_path', help='Path to overlay specification file')
    apply_parser.add_argument('output_path', help='Path for enhanced OpenAPI specification')
    apply_parser.add_argument('--format', choices=['yaml', 'json'], default='json', help='Output format')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Run ADR-005 compliance validation')
    validate_parser.add_argument('original_spec', help='Path to original OpenAPI specification file')
    validate_parser.add_argument('enhanced_spec', help='Path to enhanced OpenAPI specification file')
    validate_parser.add_argument('--violations-only', action='store_true', help='Show only violations and errors')
    validate_parser.add_argument('--show-details', action='store_true', default=True, help='Show detailed violation information')

    # Global options
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.command:
        parser.print_help()
        return 1

    try:
        if args.command == 'enhance':
            enhancer = OpenAPIEnhancer(args.spec_path, args.config)
            success = enhancer.enhance_and_generate(
                output_dir=args.output_dir,
                save_overlay=args.save_overlay,
                save_enhanced_spec=args.save_enhanced_spec,
                skip_overlay=args.skip_overlay,
                overlay_only=args.overlay_only,
                format=args.format
            )
            return 0 if success else 1

        elif args.command == 'generate-overlay':
            config = {}
            if args.config:
                with open(args.config, 'r') as f:
                    yaml = YAML(typ='safe', pure=True)
                    config = yaml.load(f).get('overlay_enhancements', {})

            generator = OpenAPIOverlayGenerator(
                spec_path=args.spec_path,
                use_llm=args.use_llm,
                overlay_config=config
            )

            overlay = generator.generate_overlay()
            with open(args.output_path, 'w') as f:
                if args.format == 'json':
                    json.dump(overlay, f, indent=2)
                else:
                    yaml = YAML()
                    yaml.dump(overlay, f)

            print(f"✓ Generated overlay: {args.output_path}")
            return 0

        elif args.command == 'apply-overlay':
            applier = OverlayApplier(args.spec_path, args.overlay_path)
            enhanced_spec = applier.apply_overlay()

            with open(args.output_path, 'w') as f:
                if args.format == 'json':
                    json.dump(enhanced_spec, f, indent=2)
                else:
                    yaml = YAML()
                    yaml.dump(enhanced_spec, f)

            print(f"✓ Applied overlay: {args.output_path}")
            return 0

        elif args.command == 'validate':
            # Load original and enhanced specs
            original_spec = load_spec_file(args.original_spec)
            enhanced_spec = load_spec_file(args.enhanced_spec)

            # Run validation
            validator = OpenAPIValidator()
            validator.start_validation_session(args.original_spec)
            validator.end_validation_session(args.enhanced_spec)

            validation_results = validator.run_full_validation_suite(original_spec, enhanced_spec)
            validation_report = validator.generate_validation_report(
                validation_results,
                violations_only=args.violations_only,
                show_details=args.show_details
            )

            print(validation_report)

            # Return exit code based on validation results
            all_passed = all(result.passed for result in validation_results.values())

            if args.violations_only and all_passed:
                print("✅ No violations found - all ADR-005 requirements met!")

            return 0 if all_passed else 1

    except Exception as e:
        logger.error(f"Command failed: {e}", exc_info=True)
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    exit(main())
