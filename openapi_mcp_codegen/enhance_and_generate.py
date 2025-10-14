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

            generator = OpenAPIOverlayGenerator(spec_path=args.spec_path)

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

            # Clean up temporary overlay if not saved
            if not args.save_overlay:
                Path(overlay_path).unlink(missing_ok=True)

        # Step 3: Generate MCP server code (unless overlay-only mode)
        if not args.overlay_only:
            logger.info("")
            logger.info("=" * 70)
            logger.info("STEP 3: Generating MCP Server Code")
            logger.info("=" * 70)

            script_dir = Path(__file__).parent.parent / 'openapi_mcp_codegen'
            mcp_generator = MCPGenerator(
                script_dir=str(script_dir),
                spec_path=enhanced_spec_path,
                output_dir=args.output_dir,
                config_path=args.config_path
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

