#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
Example: Using the OpenAPI Overlay Generator

This script demonstrates how to use the overlay generator programmatically
to enhance OpenAPI specifications for better MCP server generation.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from openapi_mcp_codegen.overlay_generator import OpenAPIOverlayGenerator
from openapi_mcp_codegen.overlay_applier import OverlayApplier
from openapi_mcp_codegen.mcp_codegen import MCPGenerator


def example1_generate_overlay():
    """Example 1: Generate an overlay without LLM (rule-based)."""
    print("=" * 70)
    print("Example 1: Generate Overlay (Rule-Based)")
    print("=" * 70)

    generator = OpenAPIOverlayGenerator(
        spec_path='argo-workflows/openapi_argo_workflows.json',
        use_llm=False
    )

    # Generate and inspect the overlay
    overlay = generator.generate_overlay()

    print(f"✓ Generated overlay with {len(overlay['actions'])} actions")
    print(f"  Title: {overlay['info']['title']}")
    print(f"  Version: {overlay['info']['version']}")

    # Show first action
    if overlay['actions']:
        action = overlay['actions'][0]
        print(f"\n  First action:")
        print(f"    Target: {action['target']}")
        print(f"    Update: {action['update'][:100]}...")

    # Save to file
    generator.save_overlay('argo-workflows/example_overlay.yaml', format='yaml')
    print(f"\n✓ Saved to: argo-workflows/example_overlay.yaml\n")


def example2_generate_with_llm():
    """Example 2: Generate an overlay with LLM enhancement."""
    print("=" * 70)
    print("Example 2: Generate Overlay (LLM-Enhanced)")
    print("=" * 70)

    try:
        generator = OpenAPIOverlayGenerator(
            spec_path='argo-workflows/openapi_argo_workflows.json',
            use_llm=True
        )

        if generator.use_llm:
            print("✓ LLM is available and will be used")
        else:
            print("⚠ LLM not available, falling back to rule-based")

        generator.save_overlay('argo-workflows/llm_enhanced_overlay.yaml', format='yaml')
        print(f"✓ Saved to: argo-workflows/llm_enhanced_overlay.yaml\n")

    except Exception as e:
        print(f"Note: LLM enhancement requires cnoe_agent_utils: {e}\n")


def example3_apply_overlay():
    """Example 3: Apply an overlay to an OpenAPI spec."""
    print("=" * 70)
    print("Example 3: Apply Overlay to OpenAPI Spec")
    print("=" * 70)

    applier = OverlayApplier(
        openapi_path='argo-workflows/openapi_argo_workflows.json',
        overlay_path='argo-workflows/example_overlay.yaml'
    )

    # Apply and save
    applier.save_result('argo-workflows/enhanced_openapi.json', format='json')
    print(f"✓ Applied overlay and saved to: argo-workflows/enhanced_openapi.json\n")


def example4_full_workflow():
    """Example 4: Complete workflow - overlay + MCP generation."""
    print("=" * 70)
    print("Example 4: Full Workflow (Overlay + MCP Generation)")
    print("=" * 70)

    # Step 1: Generate overlay
    print("\n[Step 1/3] Generating overlay...")
    generator = OpenAPIOverlayGenerator(
        spec_path='argo-workflows/openapi_argo_workflows.json',
        use_llm=False
    )
    generator.save_overlay('argo-workflows/workflow_overlay.yaml', format='yaml')
    print("✓ Overlay generated")

    # Step 2: Apply overlay
    print("\n[Step 2/3] Applying overlay...")
    applier = OverlayApplier(
        openapi_path='argo-workflows/openapi_argo_workflows.json',
        overlay_path='argo-workflows/workflow_overlay.yaml'
    )
    applier.save_result('argo-workflows/workflow_enhanced.json', format='json')
    print("✓ Overlay applied")

    # Step 3: Generate MCP code
    print("\n[Step 3/3] Generating MCP server code...")
    script_dir = Path(__file__).parent.parent / 'openapi_mcp_codegen'
    mcp_gen = MCPGenerator(
        script_dir=str(script_dir),
        spec_path='argo-workflows/workflow_enhanced.json',
        output_dir='argo-workflows/mcp_server_example',
        config_path='argo-workflows/config.yaml'
    )
    mcp_gen.generate()
    print("✓ MCP server code generated in: argo-workflows/mcp_server_example\n")


def example5_inspect_overlay():
    """Example 5: Inspect what changes an overlay will make."""
    print("=" * 70)
    print("Example 5: Inspect Overlay Contents")
    print("=" * 70)

    generator = OpenAPIOverlayGenerator(
        spec_path='argo-workflows/openapi_argo_workflows.json',
        use_llm=False
    )

    overlay = generator.generate_overlay()

    # Count action types
    update_actions = sum(1 for a in overlay['actions'] if 'update' in a)
    remove_actions = sum(1 for a in overlay['actions'] if a.get('remove'))

    print(f"Overlay Statistics:")
    print(f"  Total actions: {len(overlay['actions'])}")
    print(f"  Update actions: {update_actions}")
    print(f"  Remove actions: {remove_actions}")

    # Show actions by target pattern
    desc_updates = sum(1 for a in overlay['actions'] if 'description' in a.get('target', ''))
    summary_updates = sum(1 for a in overlay['actions'] if 'summary' in a.get('target', ''))
    param_updates = sum(1 for a in overlay['actions'] if 'parameters' in a.get('target', ''))

    print(f"\n  Actions by type:")
    print(f"    Description updates: {desc_updates}")
    print(f"    Summary updates: {summary_updates}")
    print(f"    Parameter updates: {param_updates}")

    # Show sample actions for different paths
    print(f"\n  Sample actions:")
    for i, action in enumerate(overlay['actions'][:3]):
        print(f"\n    Action {i+1}:")
        print(f"      Target: {action['target']}")
        update = action.get('update', '')
        if len(update) > 100:
            update = update[:100] + "..."
        print(f"      Update: {update}")

    print()


def main():
    """Run all examples."""
    os.chdir(Path(__file__).parent)

    print("\n" + "=" * 70)
    print("OpenAPI Overlay Generator Examples")
    print("=" * 70 + "\n")

    try:
        # Run examples
        example1_generate_overlay()
        example2_generate_with_llm()
        example3_apply_overlay()
        example5_inspect_overlay()

        # example4_full_workflow()  # Uncomment to run full workflow

        print("=" * 70)
        print("✓ All examples completed successfully!")
        print("=" * 70)
        print("\nGenerated files:")
        print("  - argo-workflows/example_overlay.yaml")
        print("  - argo-workflows/enhanced_openapi.json")
        print("\nTo run the full workflow, uncomment example4_full_workflow() in the script.")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())

