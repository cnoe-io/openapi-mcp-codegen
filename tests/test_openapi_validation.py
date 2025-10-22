#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
Test script to validate OpenAPI specifications for common issues.

This script checks for:
1. Parameters missing both 'schema' and 'content' fields
2. Other OpenAPI specification validation issues
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def validate_parameters(spec_path: str) -> Tuple[List[str], int]:
    """
    Validate that all parameters have either a 'schema' or 'content' field.
    Also check for invalid 'body' parameters (OpenAPI 2.0 style).

    Args:
        spec_path: Path to the OpenAPI specification file

    Returns:
        Tuple of (list of error messages, count of errors)
    """
    errors = []
    error_count = 0

    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            spec = json.load(f)
    except Exception as e:
        return [f"Failed to load OpenAPI spec: {e}"], 1

    # Check all parameters in all operations
    for path, methods in spec.get('paths', {}).items():
        for method, operation in methods.items():
            if method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                for param in operation.get('parameters', []):
                    param_name = param.get('name', '<unnamed>')
                    param_in = param.get('in', '<unknown>')

                    # Check for invalid 'body' parameters (OpenAPI 2.0 style)
                    # In OpenAPI 3.x, body should be in requestBody, not parameters
                    if param_in == 'body':
                        error_msg = (
                            f"ERROR: {method.upper()} {path} - "
                            f"parameter '{param_name}' has in='body' "
                            f"(OpenAPI 2.0 style, should use requestBody in OpenAPI 3.x)"
                        )
                        errors.append(error_msg)
                        error_count += 1
                        continue

                    # According to OpenAPI 3.x spec, parameters must have either
                    # 'schema' or 'content' to define their type
                    # (exception: cookie parameters may have different rules)
                    if 'schema' not in param and 'content' not in param:
                        # Cookie parameters might have different rules
                        if param_in == 'cookie':
                            continue

                        error_msg = (
                            f"ERROR: {method.upper()} {path} - "
                            f"parameter '{param_name}' (in: {param_in}) "
                            f"has neither 'schema' nor 'content'"
                        )
                        errors.append(error_msg)
                        error_count += 1

    return errors, error_count


def validate_openapi_spec(spec_path: str, verbose: bool = False) -> bool:
    """
    Validate an OpenAPI specification file.

    Args:
        spec_path: Path to the OpenAPI specification file
        verbose: If True, print all error details

    Returns:
        True if validation passes, False otherwise
    """
    print(f"Validating OpenAPI spec: {spec_path}")
    print("=" * 70)

    # Check if file exists
    if not Path(spec_path).exists():
        print(f"ERROR: File not found: {spec_path}")
        return False

    # Validate parameters
    errors, error_count = validate_parameters(spec_path)

    if error_count == 0:
        print("✓ All parameters are valid (have schema or content)")
        print("=" * 70)
        print(f"VALIDATION PASSED: {spec_path}")
        return True
    else:
        print(f"✗ Found {error_count} parameter(s) with missing schema/content")
        if verbose:
            print("\nError details:")
            for error in errors:
                print(f"  {error}")
        print("=" * 70)
        print(f"VALIDATION FAILED: {spec_path}")
        return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate OpenAPI specifications for common issues'
    )
    parser.add_argument(
        'spec_path',
        help='Path to the OpenAPI specification file to validate'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed error messages'
    )

    args = parser.parse_args()

    success = validate_openapi_spec(args.spec_path, verbose=args.verbose)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

