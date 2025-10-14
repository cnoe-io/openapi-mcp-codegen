#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
OpenAPI Overlay Generator for MCP Servers

This module generates OpenAPI Overlay specifications to enhance API descriptions
with agent-friendly documentation. The overlays improve the quality of generated
MCP server tools by adding clear, contextual descriptions that help LLM agents
better understand when and how to use each API operation.

Usage:
    python overlay_generator.py <openapi_spec_path> <output_overlay_path> [options]
"""

import json
import yaml
import argparse
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import re

try:
    from cnoe_agent_utils import LLMFactory
    from langchain_core.messages import SystemMessage
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    logger = logging.getLogger("overlay_generator")
    logger.warning("cnoe_agent_utils not available, LLM enhancement disabled")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("overlay_generator")


class OpenAPIOverlayGenerator:
    """
    Generates OpenAPI Overlay specifications to enhance API documentation
    for better AI agent understanding and MCP server code generation.
    """

    def __init__(self, spec_path: str, use_llm: bool = False, llm_config: Optional[Dict] = None):
        """
        Initialize the overlay generator.

        Args:
            spec_path: Path to the OpenAPI specification file
            use_llm: Whether to use LLM for generating enhanced descriptions
            llm_config: Configuration for LLM (if use_llm is True)
        """
        self.spec_path = spec_path
        self.spec = self._load_spec()
        self.use_llm = use_llm and LLM_AVAILABLE
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
                return yaml.safe_load(f)

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

    def _generate_parameter_guidance(self, parameters: List[Dict[str, Any]]) -> List[str]:
        """
        Generate agent-friendly guidance for parameters.

        Args:
            parameters: List of parameter objects

        Returns:
            List of guidance strings
        """
        guidance = []

        required_params = [p for p in parameters if p.get('required', False)]
        optional_params = [p for p in parameters if not p.get('required', False)]

        if required_params:
            param_names = [p.get('name', 'unknown') for p in required_params]
            guidance.append(f"Required parameters: {', '.join(param_names)}")

        if optional_params:
            param_names = [p.get('name', 'unknown') for p in optional_params]
            guidance.append(f"Optional parameters for filtering or customization: {', '.join(param_names)}")

        # Identify common parameter patterns
        filter_params = [p for p in parameters if any(
            keyword in p.get('name', '').lower()
            for keyword in ['filter', 'selector', 'query', 'search']
        )]
        if filter_params:
            guidance.append("Use filter parameters to narrow down results based on specific criteria")

        pagination_params = [p for p in parameters if any(
            keyword in p.get('name', '').lower()
            for keyword in ['limit', 'offset', 'page', 'continue']
        )]
        if pagination_params:
            guidance.append("Supports pagination for large result sets")

        return guidance

    def _create_enhanced_description_with_llm(self, method: str, path: str, operation: Dict[str, Any]) -> str:
        """
        Create an enhanced description using LLM.

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
            original_desc = operation.get('description', '')
            summary = operation.get('summary', '')
            operation_id = operation.get('operationId', '')
            parameters = operation.get('parameters', [])
            
            param_info = []
            for p in parameters:
                param_info.append({
                    'name': p.get('name', ''),
                    'type': p.get('type', p.get('schema', {}).get('type', 'string')),
                    'required': p.get('required', False),
                    'description': p.get('description', '')
                })

            system_msg = SystemMessage(
                content=(
                    "You are an expert at writing concise, OpenAI-compatible tool descriptions. "
                    "Your task is to write clear, brief descriptions that help AI function calling understand when to use each API operation. "
                    "Follow these strict rules:\n"
                    "1. Keep descriptions under 250 characters (OpenAI's recommended limit)\n"
                    "2. Start with what the operation does (verb + object)\n"
                    "3. Add one use case if space allows: 'Use when: <scenario>'\n"
                    "4. NO markdown formatting, bullet points, or special characters\n"
                    "5. NO parameter listings in the description\n"
                    "6. Write in plain, direct language\n\n"
                    "Example good description: 'Retrieve details of a specific workflow by name. Use when: you need to check workflow status or configuration.'\n"
                    "Example bad description: '**Purpose:** Lists workflows\\n\\n**Usage:**...'"
                )
            )

            user_prompt = f"""
API: {method.upper()} {path}
Operation: {operation_id}
Summary: {summary}
Original: {original_desc[:200] if original_desc else 'None'}

Write a concise, OpenAI-compatible tool description (max 250 chars, no markdown).
"""

            response = self.llm.invoke([system_msg, SystemMessage(content=user_prompt)])
            enhanced_desc = response.content.strip()
            
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

    def _enhance_parameter_description_with_llm(self, param: Dict[str, Any], operation_context: str = "") -> str:
        """
        Enhance a parameter description using LLM.

        Args:
            param: Parameter object
            operation_context: Context about the operation this parameter belongs to

        Returns:
            LLM-generated enhanced description
        """
        if not self.llm:
            return self._enhance_parameter_description(param)

        try:
            name = param.get('name', '')
            original_desc = param.get('description', '')
            param_type = param.get('type', param.get('schema', {}).get('type', 'string'))
            required = param.get('required', False)

            system_msg = SystemMessage(
                content=(
                    "You are an expert at writing OpenAI-compatible parameter descriptions. "
                    "Write clear, brief descriptions for function parameters. "
                    "Rules:\n"
                    "1. Keep under 100 characters\n"
                    "2. Plain text only, no markdown or special formatting\n"
                    "3. Start with what the parameter does\n"
                    "4. Be specific and actionable\n\n"
                    "Example good: 'Namespace to scope the operation to'\n"
                    "Example bad: '**Optional parameter** - only include when...'"
                )
            )

            user_prompt = f"""
Parameter: {name} ({param_type})
{'Required' if required else 'Optional'}
Original: {original_desc[:100] if original_desc else 'None'}
Context: {operation_context[:50]}

Write concise parameter description (max 100 chars, plain text).
"""

            response = self.llm.invoke([system_msg, SystemMessage(content=user_prompt)])
            return response.content.strip()

        except Exception as e:
            logger.warning(f"LLM enhancement failed for parameter {param.get('name')}: {e}")
            return self._enhance_parameter_description(param)

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

        # Start with original description if good
        if original_desc:
            cleaned = ' '.join(original_desc.split())
            # Keep original if it's clear and concise
            if len(cleaned) <= 100:
                return cleaned
            # Otherwise, truncate and enhance
            parts = [cleaned[:80] + "..."]
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
                parts.append(f"Name of the {self._extract_resource_from_path(param)} to operate on")

        # If still no description, provide a generic one
        if not parts:
            if required:
                parts.append(f"Required {param_type} parameter")
            else:
                parts.append(f"Optional {param_type} parameter")

        # Keep under 150 characters for OpenAI
        description = ' '.join(parts)
        if len(description) > 150:
            description = description[:147] + "..."

        return description
    
    def _extract_resource_from_path(self, param: Dict[str, Any]) -> str:
        """Extract resource type from parameter context."""
        # This is a simple helper to make parameter descriptions more contextual
        return "resource"

    def generate_overlay(self) -> Dict[str, Any]:
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
        for path, path_item in paths.items():
            for method in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
                if method not in path_item:
                    continue

                operation = path_item[method]

                # Enhance operation description
                if self.use_llm:
                    enhanced_desc = self._create_enhanced_description_with_llm(method, path, operation)
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

                # Enhance parameter descriptions
                parameters = operation.get('parameters', [])
                operation_context = f"{method.upper()} {path} - {operation.get('summary', '')}"
                
                for idx, param in enumerate(parameters):
                    if '$ref' in param:
                        continue  # Skip refs for now

                    if self.use_llm:
                        enhanced_param_desc = self._enhance_parameter_description_with_llm(param, operation_context)
                    else:
                        enhanced_param_desc = self._enhance_parameter_description(param)
                        
                    overlay['actions'].append({
                        'target': f"$.paths['{path}'].{method}.parameters[{idx}].description",
                        'update': enhanced_param_desc
                    })

        logger.info(f"Generated {len(overlay['actions'])} overlay actions")
        return overlay

    def save_overlay(self, output_path: str, format: str = 'yaml'):
        """
        Generate and save the overlay to a file.

        Args:
            output_path: Path to save the overlay file
            format: Output format ('yaml' or 'json')
        """
        overlay = self.generate_overlay()

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            if format == 'json':
                json.dump(overlay, f, indent=2)
            else:
                yaml.dump(overlay, f, default_flow_style=False, sort_keys=False)

        logger.info(f"Overlay saved to: {output_path}")


def main():
    """Main entry point for the overlay generator."""
    parser = argparse.ArgumentParser(
        description='Generate OpenAPI Overlay specifications for MCP server enhancement'
    )
    parser.add_argument(
        'spec_path',
        help='Path to the OpenAPI specification file (JSON or YAML)'
    )
    parser.add_argument(
        'output_path',
        help='Path for the output overlay file'
    )
    parser.add_argument(
        '--format',
        choices=['yaml', 'json'],
        default='yaml',
        help='Output format for the overlay (default: yaml)'
    )
    parser.add_argument(
        '--use-llm',
        action='store_true',
        help='Use LLM to generate enhanced descriptions (requires additional setup)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        generator = OpenAPIOverlayGenerator(
            spec_path=args.spec_path,
            use_llm=args.use_llm
        )
        generator.save_overlay(args.output_path, format=args.format)
        print(f"✓ Successfully generated overlay: {args.output_path}")
    except Exception as e:
        logger.error(f"Error generating overlay: {e}", exc_info=True)
        return 1

    return 0


if __name__ == '__main__':
    exit(main())

