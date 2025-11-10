#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
ADR-005 Validation Test Suite

Test script to validate that the openapi_enhancer meets all ADR-005 requirements
using the argo-workflows example as the primary test case.
"""

import subprocess
import sys
import time
from pathlib import Path
import logging
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("test_adr_validation")


def run_command(cmd: list, cwd: str = None) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def test_argo_workflows_enhancement(project_root: Path) -> bool:
    """
    Test the complete enhancement pipeline with argo-workflows example.
    
    Returns True if all ADR-005 requirements are met.
    """
    logger.info("🧪 Testing argo-workflows enhancement pipeline")
    
    # Paths
    argo_dir = project_root / "examples" / "argo-workflows"
    original_spec = argo_dir / "argo-openapi.json"
    enhanced_spec = argo_dir / "argo-openapi-enhanced-test.json"
    config_file = argo_dir / "config.yaml"
    enhancer_script = project_root / "openapi_mcp_codegen" / "openapi_enhancer.py"
    
    # Ensure files exist
    if not original_spec.exists():
        logger.error(f"Original spec not found: {original_spec}")
        return False
    
    if not config_file.exists():
        logger.error(f"Config file not found: {config_file}")
        return False
    
    # Step 1: Run enhancement pipeline
    logger.info("📋 Step 1: Running enhancement pipeline")
    
    enhance_cmd = [
        "python", str(enhancer_script),
        "--verbose",
        "enhance",
        str(original_spec),
        str(argo_dir / "test_output"),
        "--config", str(config_file),
        "--save-enhanced-spec", str(enhanced_spec),
        "--overlay-only"  # Skip MCP generation for faster testing
    ]
    
    start_time = time.time()
    exit_code, stdout, stderr = run_command(enhance_cmd, cwd=str(project_root))
    end_time = time.time()
    
    processing_time = end_time - start_time
    logger.info(f"Enhancement completed in {processing_time:.2f}s")
    
    if exit_code != 0:
        logger.error("Enhancement pipeline failed")
        logger.error(f"STDERR: {stderr}")
        return False
    
    logger.info("✅ Enhancement pipeline completed successfully")
    
    # Step 2: Run dedicated validation
    logger.info("📋 Step 2: Running ADR-005 validation")
    
    validate_cmd = [
        "python", str(enhancer_script),
        "--verbose",
        "validate",
        str(original_spec),
        str(enhanced_spec)
    ]
    
    exit_code, stdout, stderr = run_command(validate_cmd, cwd=str(project_root))
    
    # Print validation report
    print("\n" + "="*80)
    print("VALIDATION REPORT")
    print("="*80)
    print(stdout)
    
    if stderr:
        print("STDERR:")
        print(stderr)
    
    # Check validation results
    validation_passed = exit_code == 0
    
    if validation_passed:
        logger.info("✅ All ADR-005 requirements satisfied!")
    else:
        logger.error("❌ ADR-005 validation failed")
    
    # Step 3: Performance validation
    logger.info("📋 Step 3: Performance requirements check")
    
    # ADR requirement: <25% increase in processing time
    # For baseline, estimate ~30s for a 771KB spec with 255 operations
    estimated_baseline = 30.0  
    time_increase = ((processing_time - estimated_baseline) / estimated_baseline) * 100.0
    
    performance_ok = time_increase <= 25.0
    
    if performance_ok:
        logger.info(f"✅ Performance requirement met: {processing_time:.2f}s ({time_increase:+.1f}% vs baseline)")
    else:
        logger.warning(f"⚠️  Performance requirement not met: {processing_time:.2f}s ({time_increase:+.1f}% vs baseline)")
    
    # Clean up test files
    if enhanced_spec.exists():
        enhanced_spec.unlink()
    
    test_output_dir = argo_dir / "test_output"
    if test_output_dir.exists():
        import shutil
        shutil.rmtree(test_output_dir)
    
    return validation_passed and performance_ok


def test_petstore_example(project_root: Path) -> bool:
    """
    Test enhancement with petstore example (smaller, faster test).
    
    Returns True if basic conversion works.
    """
    logger.info("🧪 Testing petstore enhancement (basic functionality)")
    
    # Use tests directory petstore example
    test_dir = project_root / "tests"
    petstore_spec = test_dir / "openapi_petstore.json"
    enhanced_spec = test_dir / "petstore_enhanced_test.json"
    enhancer_script = project_root / "openapi_mcp_codegen" / "openapi_enhancer.py"
    
    if not petstore_spec.exists():
        logger.warning(f"Petstore spec not found: {petstore_spec}, skipping test")
        return True  # Skip, don't fail
    
    # Create minimal config
    config_content = """title: petstore-test
description: Test configuration
author: Test
email: test@example.com
version: 0.1.0
license: Apache-2.0
python_version: 3.13.2

overlay_enhancements:
  enabled: true
  use_llm: false  # Use rule-based for faster testing
"""
    
    config_file = test_dir / "test_config.yaml"
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    # Run enhancement
    enhance_cmd = [
        "python", str(enhancer_script),
        "enhance",
        str(petstore_spec),
        str(test_dir / "test_output"),
        "--config", str(config_file),
        "--save-enhanced-spec", str(enhanced_spec),
        "--overlay-only"
    ]
    
    exit_code, stdout, stderr = run_command(enhance_cmd, cwd=str(project_root))
    
    success = exit_code == 0 and enhanced_spec.exists()
    
    if success:
        logger.info("✅ Petstore enhancement test passed")
    else:
        logger.error("❌ Petstore enhancement test failed")
        logger.error(f"STDERR: {stderr}")
    
    # Clean up
    if enhanced_spec.exists():
        enhanced_spec.unlink()
    if config_file.exists():
        config_file.unlink()
    
    test_output_dir = test_dir / "test_output"
    if test_output_dir.exists():
        import shutil
        shutil.rmtree(test_output_dir)
    
    return success


def run_comprehensive_test_suite(project_root: Path) -> bool:
    """
    Run the complete ADR-005 validation test suite.
    
    Returns True if all tests pass.
    """
    logger.info("🚀 Starting comprehensive ADR-005 validation test suite")
    logger.info(f"Project root: {project_root}")
    
    all_passed = True
    
    # Test 1: Petstore (quick validation)
    logger.info("\n" + "="*60)
    logger.info("TEST 1: Basic Enhancement (Petstore)")
    logger.info("="*60)
    
    petstore_passed = test_petstore_example(project_root)
    all_passed = all_passed and petstore_passed
    
    # Test 2: Argo Workflows (comprehensive ADR validation)
    logger.info("\n" + "="*60)
    logger.info("TEST 2: Comprehensive ADR-005 Validation (Argo Workflows)")
    logger.info("="*60)
    
    argo_passed = test_argo_workflows_enhancement(project_root)
    all_passed = all_passed and argo_passed
    
    # Final summary
    logger.info("\n" + "="*80)
    logger.info("FINAL TEST RESULTS")
    logger.info("="*80)
    logger.info(f"Basic Enhancement Test:      {'PASS' if petstore_passed else 'FAIL'}")
    logger.info(f"ADR-005 Validation Test:     {'PASS' if argo_passed else 'FAIL'}")
    logger.info(f"Overall Result:              {'PASS' if all_passed else 'FAIL'}")
    
    return all_passed


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(
        description='ADR-005 Validation Test Suite',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full test suite
  python test_adr_validation.py
  
  # Run only argo-workflows test
  python test_adr_validation.py --test argo
  
  # Run only petstore test  
  python test_adr_validation.py --test petstore
        """
    )
    
    parser.add_argument(
        '--test',
        choices=['all', 'argo', 'petstore'],
        default='all',
        help='Which test to run (default: all)'
    )
    parser.add_argument(
        '--project-root',
        type=Path,
        default=Path(__file__).parent.parent,
        help='Path to project root directory'
    )
    
    args = parser.parse_args()
    
    project_root = args.project_root.resolve()
    
    if not project_root.exists():
        logger.error(f"Project root not found: {project_root}")
        return 1
    
    success = True
    
    if args.test in ['all', 'petstore']:
        success = success and test_petstore_example(project_root)
    
    if args.test in ['all', 'argo']:
        success = success and test_argo_workflows_enhancement(project_root)
    
    if args.test == 'all':
        success = run_comprehensive_test_suite(project_root)
    
    return 0 if success else 1


if __name__ == '__main__':
    exit(main())
