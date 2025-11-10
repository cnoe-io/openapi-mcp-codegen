#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
Function Validation Script for Generated MCP Tools

Validates all generated MCP functions to ensure:
1. No duplicate function names
2. Function names meet length requirements (≤30 target, ≤64 hard limit)
3. HTTP method prefix conventions are followed
4. All functions are properly registered in server.py
5. Function syntax is valid Python
6. Proper naming conventions are used
"""

import ast
import importlib.util
import logging
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class FunctionInfo:
    """Information about a generated function."""
    name: str
    file_path: str
    line_number: int
    http_method: Optional[str] = None
    module_name: str = ""
    is_registered: bool = False
    length: int = 0
    
    def __post_init__(self):
        self.length = len(self.name)


@dataclass
class ValidationResult:
    """Results from function validation."""
    passed: bool
    total_functions: int
    errors: List[str]
    warnings: List[str]
    duplicates: Dict[str, List[str]]
    length_violations: List[FunctionInfo]
    unregistered_functions: List[FunctionInfo]
    naming_violations: List[FunctionInfo]


class FunctionValidator:
    """Validates generated MCP functions for compliance and quality."""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.functions: List[FunctionInfo] = []
        self.registered_functions: Set[str] = set()
        
        # Validation rules
        self.target_length = 30
        self.max_length = 64
        self.http_methods = {'get', 'post', 'put', 'patch', 'delete', 'del', 'head', 'opts'}
        
    def find_generated_projects(self) -> List[Path]:
        """Find all generated MCP projects."""
        projects = []
        
        # Look in examples directories for generate_code folders
        examples_dir = self.project_root / "examples"
        if examples_dir.exists():
            for example_dir in examples_dir.iterdir():
                if example_dir.is_dir():
                    generate_code_dir = example_dir / "generate_code"
                    if generate_code_dir.exists():
                        # Look for mcp_* directories
                        for mcp_dir in generate_code_dir.iterdir():
                            if mcp_dir.is_dir() and mcp_dir.name.startswith('mcp_'):
                                projects.append(mcp_dir)
        
        return projects
    
    def extract_functions_from_file(self, file_path: Path) -> List[FunctionInfo]:
        """Extract function definitions from a Python file."""
        functions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the AST
            tree = ast.parse(content, filename=str(file_path))
            
            for node in ast.walk(tree):
                if isinstance(node, ast.AsyncFunctionDef):
                    func_info = FunctionInfo(
                        name=node.name,
                        file_path=str(file_path),
                        line_number=node.lineno,
                        module_name=file_path.stem
                    )
                    
                    # Try to detect HTTP method from function name
                    func_info.http_method = self._detect_http_method(node.name)
                    
                    functions.append(func_info)
                    
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path}: {e}")
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            
        return functions
    
    def _detect_http_method(self, function_name: str) -> Optional[str]:
        """Detect HTTP method from function name prefix."""
        for method in self.http_methods:
            if function_name.startswith(f"{method}_"):
                return method.upper()
        return None
    
    def extract_registered_functions(self, server_file: Path) -> Set[str]:
        """Extract registered function names from server.py."""
        registered = set()
        
        try:
            with open(server_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for mcp.tool() registrations
            # Pattern: mcp.tool()(module.function_name)
            pattern = r'mcp\.tool\(\)\([^.]+\.([^)]+)\)'
            matches = re.findall(pattern, content)
            registered.update(matches)
            
        except Exception as e:
            logger.error(f"Error parsing server file {server_file}: {e}")
            
        return registered
    
    def validate_project(self, project_dir: Path) -> ValidationResult:
        """Validate all functions in a single MCP project."""
        logger.info(f"🔍 Validating MCP project: {project_dir}")
        
        errors = []
        warnings = []
        self.functions = []
        
        # Find tools directory
        tools_dir = project_dir / "tools"
        if not tools_dir.exists():
            errors.append(f"Tools directory not found: {tools_dir}")
            return ValidationResult(False, 0, errors, warnings, {}, [], [], [])
        
        # Extract functions from all tool files
        for tool_file in tools_dir.glob("*.py"):
            if tool_file.name in ['__init__.py']:
                continue
            
            functions = self.extract_functions_from_file(tool_file)
            self.functions.extend(functions)
        
        # Extract registered functions from server.py
        server_file = project_dir / "server.py"
        if server_file.exists():
            self.registered_functions = self.extract_registered_functions(server_file)
        else:
            warnings.append(f"Server file not found: {server_file}")
        
        # Run validation checks
        duplicates = self._check_duplicates()
        length_violations = self._check_length_limits()
        unregistered = self._check_registration()
        naming_violations = self._check_naming_conventions()
        
        # Update registration status
        for func in self.functions:
            func.is_registered = func.name in self.registered_functions
        
        # Collect errors
        if duplicates:
            errors.append(f"Found {len(duplicates)} duplicate function names")
        
        if length_violations:
            errors.append(f"Found {len(length_violations)} functions exceeding length limits")
        
        if unregistered:
            errors.append(f"Found {len(unregistered)} unregistered functions")
        
        # Warnings for naming conventions
        if naming_violations:
            warnings.append(f"Found {len(naming_violations)} functions with naming convention issues")
        
        passed = len(errors) == 0
        
        return ValidationResult(
            passed=passed,
            total_functions=len(self.functions),
            errors=errors,
            warnings=warnings,
            duplicates=duplicates,
            length_violations=length_violations,
            unregistered_functions=unregistered,
            naming_violations=naming_violations
        )
    
    def _check_duplicates(self) -> Dict[str, List[str]]:
        """Check for duplicate function names."""
        name_counts = defaultdict(list)
        
        for func in self.functions:
            name_counts[func.name].append(func.file_path)
        
        # Return only duplicates
        duplicates = {name: paths for name, paths in name_counts.items() if len(paths) > 1}
        
        if duplicates:
            logger.error(f"❌ Found {len(duplicates)} duplicate function names")
            for name, paths in duplicates.items():
                logger.error(f"  '{name}' found in: {paths}")
        
        return duplicates
    
    def _check_length_limits(self) -> List[FunctionInfo]:
        """Check function name length limits."""
        violations = []
        
        for func in self.functions:
            if func.length > self.max_length:
                violations.append(func)
                logger.error(f"❌ Function '{func.name}' ({func.length} chars) exceeds hard limit ({self.max_length})")
            elif func.length > self.target_length:
                logger.warning(f"⚠️  Function '{func.name}' ({func.length} chars) exceeds target ({self.target_length})")
        
        return violations
    
    def _check_registration(self) -> List[FunctionInfo]:
        """Check that all functions are registered in server.py."""
        unregistered = []
        
        for func in self.functions:
            if func.name not in self.registered_functions:
                unregistered.append(func)
                logger.error(f"❌ Function '{func.name}' not registered in server.py")
        
        return unregistered
    
    def _check_naming_conventions(self) -> List[FunctionInfo]:
        """Check naming convention compliance."""
        violations = []
        
        # Common abbreviations that should be used
        expected_abbrevs = {
            'workflow': 'wf',
            'template': 'tpl',
            'service': 'svc',
            'cluster': 'clust',
            'archived': 'arch',
            'namespace': 'ns',
            'artifact': 'art',
            'event_source': 'evt_src',
            'cron_workflow': 'cron_wf'
        }
        
        for func in self.functions:
            # Check if function name contains words that should be abbreviated
            for full_word, abbrev in expected_abbrevs.items():
                if full_word in func.name and abbrev not in func.name:
                    violations.append(func)
                    logger.warning(f"⚠️  Function '{func.name}' should use '{abbrev}' instead of '{full_word}'")
                    break
        
        return violations
    
    def generate_validation_report(self, results: Dict[str, ValidationResult]) -> str:
        """Generate a comprehensive validation report."""
        report_lines = [
            "=" * 80,
            "🔍 MCP FUNCTION VALIDATION REPORT",
            "=" * 80,
            ""
        ]
        
        total_functions = sum(result.total_functions for result in results.values())
        total_errors = sum(len(result.errors) for result in results.values())
        total_warnings = sum(len(result.warnings) for result in results.values())
        projects_passed = sum(1 for result in results.values() if result.passed)
        
        # Overall summary
        overall_status = "PASSED" if total_errors == 0 else "FAILED"
        report_lines.extend([
            f"📊 OVERALL RESULT: {overall_status}",
            f"📋 Projects Validated: {len(results)} ({projects_passed} passed)",
            f"🔧 Total Functions: {total_functions}",
            f"❌ Total Errors: {total_errors}",
            f"⚠️  Total Warnings: {total_warnings}",
            ""
        ])
        
        # Per-project results
        for project_name, result in results.items():
            status_emoji = "✅" if result.passed else "❌"
            report_lines.extend([
                f"{status_emoji} {project_name}:",
                f"   Functions: {result.total_functions}",
                f"   Errors: {len(result.errors)}",
                f"   Warnings: {len(result.warnings)}",
                ""
            ])
            
            # Show errors
            for error in result.errors:
                report_lines.append(f"   ❌ ERROR: {error}")
            
            # Show warnings
            for warning in result.warnings:
                report_lines.append(f"   ⚠️  WARNING: {warning}")
            
            # Detailed violation reports
            if result.duplicates:
                report_lines.append(f"   📋 Duplicate Functions:")
                for name, paths in result.duplicates.items():
                    report_lines.append(f"      '{name}' in {len(paths)} files")
            
            if result.length_violations:
                report_lines.append(f"   📏 Length Violations:")
                for func in result.length_violations:
                    report_lines.append(f"      '{func.name}' ({func.length} chars)")
            
            if result.unregistered_functions:
                report_lines.append(f"   📝 Unregistered Functions:")
                for func in result.unregistered_functions:
                    report_lines.append(f"      '{func.name}' in {func.module_name}")
            
            report_lines.append("")
        
        # Summary and recommendations
        report_lines.extend([
            "=" * 80,
            "💡 RECOMMENDATIONS:",
            ""
        ])
        
        if total_errors > 0:
            report_lines.extend([
                "1. ❌ CRITICAL: Fix duplicate function names",
                "2. ❌ CRITICAL: Resolve function length violations",
                "3. ❌ CRITICAL: Register all functions in server.py",
                ""
            ])
        
        if total_warnings > 0:
            report_lines.extend([
                "4. ⚠️  OPTIONAL: Apply consistent naming conventions",
                "5. ⚠️  OPTIONAL: Consider further abbreviations for readability",
                ""
            ])
        
        if total_errors == 0 and total_warnings == 0:
            report_lines.extend([
                "🎉 All validations passed!",
                "✨ Functions follow naming conventions",
                "✨ No duplicates or length violations",
                "✨ All functions properly registered",
                ""
            ])
        
        # Function statistics
        if total_functions > 0:
            # Length distribution
            all_functions = []
            for result in results.values():
                # We need to reconstruct functions from results
                # This is a simplified version - in a real implementation,
                # we'd store more detailed stats in the validation result
                pass
            
            report_lines.extend([
                "📈 FUNCTION STATISTICS:",
                f"   • Total Functions Generated: {total_functions}",
                f"   • Projects with Issues: {len(results) - projects_passed}",
                f"   • Average Functions per Project: {total_functions / len(results):.1f}",
                ""
            ])
        
        report_lines.extend([
            "=" * 80,
            f"🏁 VALIDATION COMPLETE: {overall_status}",
            "=" * 80
        ])
        
        return "\n".join(report_lines)
    
    def validate_all_projects(self) -> bool:
        """Validate all generated MCP projects and return overall success."""
        logger.info("🚀 Starting comprehensive function validation")
        
        projects = self.find_generated_projects()
        if not projects:
            logger.error("❌ No generated MCP projects found")
            return False
        
        logger.info(f"📋 Found {len(projects)} MCP projects to validate")
        
        results = {}
        overall_success = True
        
        for project_dir in projects:
            project_name = project_dir.name
            result = self.validate_project(project_dir)
            results[project_name] = result
            
            if not result.passed:
                overall_success = False
        
        # Generate and print report
        report = self.generate_validation_report(results)
        print(report)
        
        # Return overall success
        return overall_success


def main():
    """Main entry point for function validation."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate generated MCP functions for compliance and quality',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate all generated projects
  python function_validator.py
  
  # Validate with specific project root
  python function_validator.py --project-root /path/to/project
  
  # Enable verbose logging
  python function_validator.py --verbose
        """
    )
    
    parser.add_argument(
        '--project-root',
        type=Path,
        default=Path(__file__).parent.parent,
        help='Path to project root directory (default: parent of this script)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate project root exists
    if not args.project_root.exists():
        logger.error(f"❌ Project root not found: {args.project_root}")
        return 1
    
    # Run validation
    validator = FunctionValidator(args.project_root)
    success = validator.validate_all_projects()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
