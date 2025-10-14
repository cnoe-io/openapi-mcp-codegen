#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
OpenAPI Overlay Applier

Applies OpenAPI Overlay specifications to OpenAPI documents.
This module implements the OpenAPI Overlay Specification 1.0.0 as defined at:
https://www.openapis.org/blog/2024/10/22/announcing-overlay-specification

Usage:
    python overlay_applier.py <openapi_spec> <overlay_spec> <output_spec>
"""

import json
import yaml
import argparse
import logging
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import jsonpath_ng
from jsonpath_ng.ext import parse as jsonpath_parse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("overlay_applier")


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
                return yaml.safe_load(f)

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

    def _remove_nested_value(self, obj: Any, path_parts: List[str]) -> None:
        """
        Remove a nested value from a dictionary/list structure.

        Args:
            obj: The object to modify
            path_parts: List of path components
        """
        if not path_parts:
            return

        current = obj
        for part in path_parts[:-1]:
            if part.isdigit():
                idx = int(part)
                if isinstance(current, list) and idx < len(current):
                    current = current[idx]
                else:
                    return
            else:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return

        # Remove the final value
        last_part = path_parts[-1]
        if last_part.isdigit():
            idx = int(last_part)
            if isinstance(current, list) and idx < len(current):
                current.pop(idx)
        else:
            if isinstance(current, dict) and last_part in current:
                del current[last_part]

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

        # Handle remove action
        elif action.get('remove'):
            matches = self._parse_jsonpath_target(target)

            for path_parts, current_value in matches:
                logger.debug(f"Removing {'.'.join(path_parts)}")
                self._remove_nested_value(self.openapi, path_parts)

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

    def save_result(self, output_path: str, format: str = 'json'):
        """
        Apply the overlay and save the result.

        Args:
            output_path: Path to save the modified OpenAPI document
            format: Output format ('yaml' or 'json')
        """
        result = self.apply_overlay()

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            if format == 'json':
                json.dump(result, f, indent=2)
            else:
                yaml.dump(result, f, default_flow_style=False, sort_keys=False)

        logger.info(f"Enhanced OpenAPI spec saved to: {output_path}")


def main():
    """Main entry point for the overlay applier."""
    parser = argparse.ArgumentParser(
        description='Apply OpenAPI Overlay specifications to OpenAPI documents'
    )
    parser.add_argument(
        'openapi_spec',
        help='Path to the OpenAPI specification file'
    )
    parser.add_argument(
        'overlay_spec',
        help='Path to the overlay specification file'
    )
    parser.add_argument(
        'output_spec',
        help='Path for the output enhanced OpenAPI specification'
    )
    parser.add_argument(
        '--format',
        choices=['yaml', 'json'],
        default='json',
        help='Output format (default: json)'
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
        applier = OverlayApplier(args.openapi_spec, args.overlay_spec)
        applier.save_result(args.output_spec, format=args.format)
        print(f"✓ Successfully applied overlay and saved to: {args.output_spec}")
    except Exception as e:
        logger.error(f"Error applying overlay: {e}", exc_info=True)
        return 1

    return 0


if __name__ == '__main__':
    exit(main())

