#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
Integrated MCP Code Generation with Overlay Enhancement

This script provides an end-to-end workflow for:
1. Generating an OpenAPI Overlay with agent-friendly enhancements
2. Applying the overlay to the original OpenAPI spec
3. Generating MCP server code from the enhanced spec

Usage:
    python enhance_and_generate.py <spec_path> <output_dir> <config_path> [options]
"""

import argparse
import logging
import tempfile
from pathlib import Path
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openapi_mcp_codegen.overlay_generator import OpenAPIOverlayGenerator
from openapi_mcp_codegen.overlay_applier import OverlayApplier
from openapi_mcp_codegen.mcp_codegen import MCPGenerator
from jinja2 import Environment, FileSystemLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("enhance_and_generate")


def _fix_openapi_parameters(spec_path: str) -> int:
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


def _generate_example_makefile(spec_path: str, mcp_generator: MCPGenerator):
    """
    Generate a Makefile in the same directory as the OpenAPI spec.

    Args:
        spec_path: Path to the OpenAPI specification file
        mcp_generator: The MCPGenerator instance with configuration
    """
    try:
        spec_dir = Path(spec_path).parent
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


def main():
    """Main workflow orchestrator."""
    parser = argparse.ArgumentParser(
        description='Generate MCP server code with OpenAPI Overlay enhancements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with automatic overlay generation and application
  python enhance_and_generate.py spec.json output/ config.yaml

  # Save intermediate overlay and enhanced spec files
  python enhance_and_generate.py spec.json output/ config.yaml \\
    --save-overlay overlay.yaml \\
    --save-enhanced-spec enhanced_spec.json

  # Skip overlay generation and use existing enhanced spec
  python enhance_and_generate.py enhanced_spec.json output/ config.yaml \\
    --skip-overlay
        """
    )

    parser.add_argument(
        'spec_path',
        help='Path to the OpenAPI specification file'
    )
    parser.add_argument(
        'output_dir',
        help='Output directory for generated MCP server code'
    )
    parser.add_argument(
        'config_path',
        help='Path to the MCP code generation configuration file'
    )
    parser.add_argument(
        '--save-overlay',
        metavar='PATH',
        help='Save the generated overlay to this path (optional)'
    )
    parser.add_argument(
        '--save-enhanced-spec',
        metavar='PATH',
        help='Save the enhanced OpenAPI spec to this path (optional)'
    )
    parser.add_argument(
        '--skip-overlay',
        action='store_true',
        help='Skip overlay generation (assumes spec is already enhanced)'
    )
    parser.add_argument(
        '--overlay-only',
        action='store_true',
        help='Only generate and apply overlay, skip MCP code generation'
    )
    parser.add_argument(
        '--format',
        choices=['yaml', 'json'],
        default='yaml',
        help='Format for saved overlay (default: yaml)'
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
        # Step 1: Generate overlay (unless skipped)
        enhanced_spec_path = args.spec_path
        overlay_path = None

        if not args.skip_overlay:
            logger.info("=" * 70)
            logger.info("STEP 1: Generating OpenAPI Overlay")
            logger.info("=" * 70)

            # Load config to get overlay enhancement settings
            import yaml as yaml_loader
            overlay_config = {}
            try:
                with open(args.config_path, 'r', encoding='utf-8') as f:
                    config = yaml_loader.safe_load(f)
                    overlay_config = config.get('overlay_enhancements', {})
                    if overlay_config.get('enabled', True):
                        logger.info("Using overlay enhancement configuration from config.yaml")
            except Exception as e:
                logger.warning(f"Could not load overlay config: {e}, using defaults")

            generator = OpenAPIOverlayGenerator(
                spec_path=args.spec_path,
                overlay_config=overlay_config
            )

            # Save overlay to specified path or temporary file
            if args.save_overlay:
                overlay_path = args.save_overlay
            else:
                # Create temporary overlay file
                temp_overlay = tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.yaml',
                    delete=False
                )
                overlay_path = temp_overlay.name
                temp_overlay.close()

            generator.save_overlay(overlay_path, format=args.format)
            print(f"✓ Generated overlay: {overlay_path}")

            # Step 2: Apply overlay
            logger.info("")
            logger.info("=" * 70)
            logger.info("STEP 2: Applying Overlay to OpenAPI Spec")
            logger.info("=" * 70)

            # Save enhanced spec to specified path or temporary file
            if args.save_enhanced_spec:
                enhanced_spec_path = args.save_enhanced_spec
            else:
                # Create temporary enhanced spec file
                temp_spec = tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.json',
                    delete=False
                )
                enhanced_spec_path = temp_spec.name
                temp_spec.close()

            applier = OverlayApplier(args.spec_path, overlay_path)
            applier.save_result(enhanced_spec_path, format='json')
            print(f"✓ Applied overlay, enhanced spec: {enhanced_spec_path}")

            # Fix OpenAPI parameters that may be missing schema definitions
            logger.info("")
            logger.info("=" * 70)
            logger.info("STEP 2.1: Validating and Fixing OpenAPI Parameters")
            logger.info("=" * 70)

            fixed_count = _fix_openapi_parameters(enhanced_spec_path)
            if fixed_count > 0:
                print(f"✓ Fixed {fixed_count} parameters with missing schema definitions")
            else:
                print(f"✓ All parameters are valid")

            # Clean up temporary overlay if not saved
            if not args.save_overlay:
                Path(overlay_path).unlink(missing_ok=True)

        # Step 3: Generate MCP server code (unless overlay-only mode)
        if not args.overlay_only:
            logger.info("")
            logger.info("=" * 70)
            logger.info("STEP 3: Generating MCP Server Code")
            logger.info("=" * 70)

            # Load config to get generate_agent and other flags
            import yaml
            with open(args.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            generate_agent = config.get('generate_agent', False)
            generate_eval = config.get('generate_eval', False)
            enable_slim = config.get('enable_slim', False)
            with_a2a_proxy = config.get('with_a2a_proxy', False)

            script_dir = Path(__file__).parent.parent / 'openapi_mcp_codegen'
            mcp_generator = MCPGenerator(
                script_dir=str(script_dir),
                spec_path=enhanced_spec_path,
                output_dir=args.output_dir,
                config_path=args.config_path,
                generate_agent=generate_agent,
                generate_eval=generate_eval,
                enable_slim=enable_slim,
                with_a2a_proxy=with_a2a_proxy
            )
            mcp_generator.generate()
            print(f"✓ Generated MCP server code in: {args.output_dir}")

            # Generate example Makefile at the spec directory level
            _generate_example_makefile(args.spec_path, mcp_generator)

            # Clean up temporary enhanced spec if not saved
            if not args.skip_overlay and not args.save_enhanced_spec:
                Path(enhanced_spec_path).unlink(missing_ok=True)

        logger.info("")
        logger.info("=" * 70)
        logger.info("✓ ALL STEPS COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)

        if args.overlay_only:
            print("\nNext steps:")
            print(f"  1. Review the enhanced spec: {enhanced_spec_path}")
            print(f"  2. Generate MCP code with: python -m openapi_mcp_codegen.mcp_codegen \\")
            print(f"       {enhanced_spec_path} {args.output_dir} {args.config_path}")
        elif not args.save_enhanced_spec:
            print("\nNote: Intermediate enhanced spec was cleaned up.")
            print("      Use --save-enhanced-spec to keep it for inspection.")

        return 0

    except Exception as e:
        logger.error(f"Error in workflow: {e}", exc_info=True)
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    exit(main())

