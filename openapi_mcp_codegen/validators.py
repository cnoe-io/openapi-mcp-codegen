#!/usr/bin/env python3
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""
OpenAPI Enhancement Validators

Comprehensive validation suite to ensure compliance with ADR-005 requirements
and OpenAPI 3.x standards. Provides auto-validation during enhancement pipeline.
"""

import json
import time
from typing import Dict, Any, List, Tuple, Optional
import logging
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger("validators")


@dataclass
class ValidationResult:
    """Results from OpenAPI validation checks."""
    passed: bool
    score: float  # 0-100 percentage
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class EnhancementMetrics:
    """Metrics for tracking enhancement pipeline performance."""
    start_time: float = 0.0
    end_time: float = 0.0
    original_size: int = 0
    enhanced_size: int = 0
    operations_processed: int = 0
    parameters_fixed: int = 0
    body_params_converted: int = 0
    overlay_actions_applied: int = 0
    llm_calls_made: int = 0
    llm_success_rate: float = 0.0
    conversion_success: bool = False

    # LLM Token tracking
    generation_tokens_input: int = 0
    generation_tokens_output: int = 0
    generation_tokens_total: int = 0
    validation_tokens_input: int = 0
    validation_tokens_output: int = 0
    validation_tokens_total: int = 0
    total_tokens_used: int = 0


class OpenAPIValidator:
    """
    Comprehensive OpenAPI validation suite ensuring ADR-005 compliance.
    """

    def __init__(self):
        self.metrics = EnhancementMetrics()
        self.adr_requirements = {
            'conversion_success_rate': 95.0,  # >95%
            'parameter_fix_rate': 100.0,      # 100%
            'body_param_conversion_rate': 100.0,  # 100%
            'llm_accuracy': 90.0,             # >90%
            'performance_increase_limit': 25.0,  # <25%
        }

    def start_validation_session(self, original_spec_path: str) -> None:
        """Start a validation session with baseline metrics."""
        self.metrics.start_time = time.time()
        if Path(original_spec_path).exists():
            self.metrics.original_size = Path(original_spec_path).stat().st_size
        logger.info("🔍 Starting validation session")

    def end_validation_session(self, enhanced_spec_path: str = None) -> None:
        """End validation session and calculate final metrics."""
        self.metrics.end_time = time.time()
        if enhanced_spec_path and Path(enhanced_spec_path).exists():
            self.metrics.enhanced_size = Path(enhanced_spec_path).stat().st_size

        # Calculate total tokens
        self.metrics.total_tokens_used = (
            self.metrics.generation_tokens_total +
            self.metrics.validation_tokens_total
        )

        logger.info("✅ Validation session completed")

    def add_generation_tokens(self, input_tokens: int, output_tokens: int) -> None:
        """Add token usage from generation phase."""
        self.metrics.generation_tokens_input += input_tokens
        self.metrics.generation_tokens_output += output_tokens
        self.metrics.generation_tokens_total += (input_tokens + output_tokens)

    def add_validation_tokens(self, input_tokens: int, output_tokens: int) -> None:
        """Add token usage from validation phase."""
        self.metrics.validation_tokens_input += input_tokens
        self.metrics.validation_tokens_output += output_tokens
        self.metrics.validation_tokens_total += (input_tokens + output_tokens)

    def extract_token_usage(self, llm_response) -> Tuple[int, int]:
        """
        Extract token usage from LLM response if available.

        Returns:
            Tuple of (input_tokens, output_tokens)
        """
        try:
            # Try to extract tokens from response metadata
            if hasattr(llm_response, 'usage_metadata'):
                usage = llm_response.usage_metadata
                input_tokens = getattr(usage, 'input_tokens', 0)
                output_tokens = getattr(usage, 'output_tokens', 0)
                return input_tokens, output_tokens

            # Try alternative attribute names
            elif hasattr(llm_response, 'token_usage'):
                usage = llm_response.token_usage
                input_tokens = getattr(usage, 'prompt_tokens', 0)
                output_tokens = getattr(usage, 'completion_tokens', 0)
                return input_tokens, output_tokens

            # Try response_metadata
            elif hasattr(llm_response, 'response_metadata'):
                metadata = llm_response.response_metadata
                if 'token_usage' in metadata:
                    usage = metadata['token_usage']
                    input_tokens = usage.get('prompt_tokens', 0)
                    output_tokens = usage.get('completion_tokens', 0)
                    return input_tokens, output_tokens

            # Estimate tokens based on content length (rough approximation)
            content = getattr(llm_response, 'content', '')
            estimated_output = len(content.split()) // 0.75  # Rough token estimate
            return 0, int(estimated_output)

        except Exception as e:
            logger.debug(f"Could not extract token usage: {e}")
            return 0, 0

    def validate_swagger_conversion(self, original_spec: Dict[str, Any], enhanced_spec: Dict[str, Any]) -> ValidationResult:
        """
        Validate Swagger 2.0 to OpenAPI 3.x conversion according to ADR-005.

        Checks:
        - Proper version conversion (swagger: 2.0 → openapi: 3.x)
        - Schema structure compliance
        - Reference path updates
        """
        errors = []
        warnings = []
        score = 0.0

        # Check if original was Swagger 2.0
        was_swagger = 'swagger' in original_spec and original_spec.get('swagger') == '2.0'

        if was_swagger:
            # Validate conversion to OpenAPI 3.x
            if 'openapi' not in enhanced_spec:
                errors.append("Missing 'openapi' field in enhanced spec")
            elif not enhanced_spec.get('openapi', '').startswith('3.'):
                errors.append(f"Invalid OpenAPI version: {enhanced_spec.get('openapi')}")
            else:
                score += 30.0  # 30% for version conversion

            # Check that old Swagger fields are removed
            swagger_fields = ['swagger', 'basePath', 'host', 'schemes', 'consumes', 'produces']
            remaining_fields = [f for f in swagger_fields if f in enhanced_spec]
            if remaining_fields:
                warnings.append(f"Swagger 2.0 fields still present: {remaining_fields}")
            else:
                score += 20.0  # 20% for field cleanup

            # Check servers field exists (converted from host/basePath)
            if 'servers' not in enhanced_spec or not enhanced_spec['servers']:
                warnings.append("No servers field found (should be converted from host/basePath)")
            else:
                score += 20.0  # 20% for servers conversion
        else:
            # Already OpenAPI 3.x, check it remains valid
            if 'openapi' in enhanced_spec and enhanced_spec.get('openapi', '').startswith('3.'):
                score += 70.0  # 70% for maintaining OpenAPI version
            else:
                errors.append("OpenAPI version corrupted during enhancement")

        # Check essential OpenAPI structure
        required_fields = ['info', 'paths']
        for field in required_fields:
            if field not in enhanced_spec:
                errors.append(f"Missing required field: {field}")
            else:
                score += 15.0  # 15% each for required fields

        passed = len(errors) == 0 and score >= self.adr_requirements['conversion_success_rate']

        return ValidationResult(
            passed=passed,
            score=score,
            message=f"Swagger conversion: {score:.1f}% ({'PASS' if passed else 'FAIL'})",
            details={
                'was_swagger_2_0': was_swagger,
                'final_openapi_version': enhanced_spec.get('openapi'),
                'remaining_swagger_fields': remaining_fields if was_swagger else [],
            },
            errors=errors,
            warnings=warnings
        )

    def validate_parameter_schemas(self, enhanced_spec: Dict[str, Any]) -> ValidationResult:
        """
        Validate that all parameters have proper schemas according to OpenAPI 3.x.

        ADR Requirement: 100% of parameters have valid schemas
        """
        errors = []
        warnings = []
        total_params = 0
        invalid_params = 0

        paths = enhanced_spec.get('paths', {})

        for path, path_obj in paths.items():
            for method, operation in path_obj.items():
                if method.lower() in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
                    parameters = operation.get('parameters', [])

                    for param in parameters:
                        total_params += 1
                        param_name = param.get('name', f'param_{total_params}')

                        # Check for required schema or content field
                        has_schema = 'schema' in param
                        has_content = 'content' in param
                        has_type_directly = 'type' in param  # Old Swagger 2.0 style

                        if not (has_schema or has_content):
                            if has_type_directly:
                                warnings.append(f"Parameter '{param_name}' in {method.upper()} {path} uses direct 'type' (Swagger 2.0 style)")
                            else:
                                errors.append(f"Parameter '{param_name}' in {method.upper()} {path} missing schema/content")
                                invalid_params += 1

                        # Validate schema structure if present
                        if has_schema:
                            schema = param['schema']
                            if not isinstance(schema, dict) or 'type' not in schema:
                                errors.append(f"Invalid schema for parameter '{param_name}' in {method.upper()} {path}")
                                invalid_params += 1

        # Calculate score based on ADR requirement (100% valid schemas)
        if total_params > 0:
            valid_params = total_params - invalid_params
            score = (valid_params / total_params) * 100.0
        else:
            score = 100.0  # No parameters to validate

        passed = score >= self.adr_requirements['parameter_fix_rate']

        self.metrics.parameters_fixed = total_params - invalid_params

        return ValidationResult(
            passed=passed,
            score=score,
            message=f"Parameter schemas: {valid_params}/{total_params} valid ({score:.1f}%) ({'PASS' if passed else 'FAIL'})",
            details={
                'total_parameters': total_params,
                'valid_parameters': valid_params,
                'invalid_parameters': invalid_params,
            },
            errors=errors,
            warnings=warnings
        )

    def validate_body_parameter_conversion(self, original_spec: Dict[str, Any], enhanced_spec: Dict[str, Any]) -> ValidationResult:
        """
        Validate that all Swagger 2.0 body parameters were properly converted to requestBody.

        ADR Requirement: 100% converted to proper requestBody
        """
        errors = []
        warnings = []

        # Count body parameters in original spec
        original_body_params = 0
        remaining_body_params = 0
        converted_to_request_body = 0

        original_paths = original_spec.get('paths', {})
        enhanced_paths = enhanced_spec.get('paths', {})

        # Count original body parameters
        for path, path_obj in original_paths.items():
            for method, operation in path_obj.items():
                if method.lower() in ['post', 'put', 'patch']:  # Methods that can have body
                    parameters = operation.get('parameters', [])
                    body_params = [p for p in parameters if p.get('in') == 'body']
                    original_body_params += len(body_params)

        # Check enhanced spec for remaining body parameters (should be 0)
        for path, path_obj in enhanced_paths.items():
            for method, operation in path_obj.items():
                if method.lower() in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
                    parameters = operation.get('parameters', [])
                    body_params = [p for p in parameters if p.get('in') == 'body']
                    remaining_body_params += len(body_params)

                    if body_params:
                        for param in body_params:
                            errors.append(f"Body parameter '{param.get('name', 'unknown')}' not converted in {method.upper()} {path}")

                    # Check if requestBody exists for operations that had body params
                    if method.lower() in ['post', 'put', 'patch'] and 'requestBody' in operation:
                        converted_to_request_body += 1

        # Calculate conversion success rate
        if original_body_params > 0:
            converted_params = original_body_params - remaining_body_params
            score = (converted_params / original_body_params) * 100.0
        else:
            score = 100.0  # No body parameters to convert

        passed = remaining_body_params == 0 and score >= self.adr_requirements['body_param_conversion_rate']

        self.metrics.body_params_converted = original_body_params - remaining_body_params

        return ValidationResult(
            passed=passed,
            score=score,
            message=f"Body parameter conversion: {original_body_params - remaining_body_params}/{original_body_params} converted ({score:.1f}%) ({'PASS' if passed else 'FAIL'})",
            details={
                'original_body_params': original_body_params,
                'remaining_body_params': remaining_body_params,
                'converted_body_params': original_body_params - remaining_body_params,
                'operations_with_request_body': converted_to_request_body,
            },
            errors=errors,
            warnings=warnings
        )

    def validate_openapi_compliance(self, enhanced_spec: Dict[str, Any]) -> ValidationResult:
        """
        Validate overall OpenAPI 3.x compliance of enhanced specification.
        """
        errors = []
        warnings = []
        score = 0.0

        # Required top-level fields
        required_fields = {
            'openapi': 20.0,
            'info': 20.0,
            'paths': 30.0
        }

        for field, points in required_fields.items():
            if field in enhanced_spec:
                score += points
            else:
                errors.append(f"Missing required field: {field}")

        # Validate info object
        if 'info' in enhanced_spec:
            info = enhanced_spec['info']
            if 'title' in info and 'version' in info:
                score += 10.0
            else:
                warnings.append("Info object missing title or version")

        # Validate paths structure
        if 'paths' in enhanced_spec:
            paths = enhanced_spec['paths']
            if isinstance(paths, dict) and len(paths) > 0:
                score += 10.0

                # Sample validation of a few operations
                valid_operations = 0
                total_operations = 0

                for path, path_obj in list(paths.items())[:5]:  # Sample first 5 paths
                    for method, operation in path_obj.items():
                        if method.lower() in ['get', 'post', 'put', 'patch', 'delete']:
                            total_operations += 1
                            if isinstance(operation, dict):
                                valid_operations += 1

                if total_operations > 0 and (valid_operations / total_operations) > 0.8:
                    score += 10.0
            else:
                warnings.append("Paths object is empty or invalid")

        passed = len(errors) == 0 and score >= 80.0

        return ValidationResult(
            passed=passed,
            score=score,
            message=f"OpenAPI compliance: {score:.1f}% ({'PASS' if passed else 'FAIL'})",
            details={
                'openapi_version': enhanced_spec.get('openapi'),
                'paths_count': len(enhanced_spec.get('paths', {})),
                'has_components': 'components' in enhanced_spec,
            },
            errors=errors,
            warnings=warnings
        )

    def validate_performance_metrics(self, baseline_time: float = None) -> ValidationResult:
        """
        Validate performance metrics against ADR requirements.

        ADR Requirement: <25% increase in processing time
        """
        errors = []
        warnings = []

        processing_time = self.metrics.end_time - self.metrics.start_time

        if baseline_time:
            time_increase = ((processing_time - baseline_time) / baseline_time) * 100.0
            passed = time_increase <= self.adr_requirements['performance_increase_limit']

            if time_increase > self.adr_requirements['performance_increase_limit']:
                errors.append(f"Performance increase {time_increase:.1f}% exceeds limit of {self.adr_requirements['performance_increase_limit']}%")

            score = max(0, 100.0 - (time_increase / self.adr_requirements['performance_increase_limit'] * 100.0))
        else:
            # No baseline, just report processing time
            passed = True
            score = 100.0 if processing_time < 60.0 else 80.0  # Arbitrary reasonable limits
            warnings.append("No baseline time provided for performance comparison")

        return ValidationResult(
            passed=passed,
            score=score,
            message=f"Performance: {processing_time:.2f}s ({'PASS' if passed else 'FAIL'})",
            details={
                'processing_time_seconds': processing_time,
                'baseline_time_seconds': baseline_time,
                'time_increase_percent': ((processing_time - baseline_time) / baseline_time) * 100.0 if baseline_time else None,
            },
            errors=errors,
            warnings=warnings
        )

    def run_full_validation_suite(self, original_spec: Dict[str, Any], enhanced_spec: Dict[str, Any]) -> Dict[str, ValidationResult]:
        """
        Run complete validation suite according to ADR-005 requirements.

        Returns dictionary of validation results for each check.
        """
        logger.info("🧪 Running full ADR-005 compliance validation suite")

        results = {}

        # 1. Swagger conversion validation
        results['swagger_conversion'] = self.validate_swagger_conversion(original_spec, enhanced_spec)

        # 2. Parameter schema validation
        results['parameter_schemas'] = self.validate_parameter_schemas(enhanced_spec)

        # 3. Body parameter conversion validation
        results['body_parameter_conversion'] = self.validate_body_parameter_conversion(original_spec, enhanced_spec)

        # 4. OpenAPI compliance validation
        results['openapi_compliance'] = self.validate_openapi_compliance(enhanced_spec)

        # 5. Performance validation (if metrics available)
        results['performance'] = self.validate_performance_metrics()

        return results

    def generate_validation_report(self, results: Dict[str, ValidationResult], violations_only: bool = False, show_details: bool = True) -> str:
        """
        Generate a comprehensive validation report.
        """
        report_lines = [
            "=" * 80,
            "🔍 ADR-005 VALIDATION REPORT",
            "=" * 80,
            ""
        ]

        total_score = 0.0
        total_checks = 0
        all_passed = True
        total_errors = 0
        total_warnings = 0

        for check_name, result in results.items():
            # If violations_only is True, skip passed results
            if violations_only and result.passed:
                # Still count toward totals
                total_score += result.score
                total_checks += 1
                all_passed = all_passed and result.passed
                continue

            status_emoji = "✅" if result.passed else "❌"
            report_lines.append(f"{status_emoji} {check_name.replace('_', ' ').title()}: {result.message}")

            if result.errors:
                total_errors += len(result.errors)
                if show_details:
                    for error in result.errors:
                        report_lines.append(f"   ❌ ERROR: {error}")

            if result.warnings:
                total_warnings += len(result.warnings)
                if show_details:
                    for warning in result.warnings:
                        report_lines.append(f"   ⚠️  WARNING: {warning}")

            # Show key details for failed checks
            if not result.passed and show_details and result.details:
                report_lines.append(f"   📋 Details:")
                for key, value in result.details.items():
                    if isinstance(value, (list, dict)) and len(str(value)) > 100:
                        report_lines.append(f"      {key}: {type(value).__name__}({len(value)} items)")
                    else:
                        report_lines.append(f"      {key}: {value}")

            report_lines.append("")
            total_score += result.score
            total_checks += 1
            all_passed = all_passed and result.passed

        # Summary
        overall_score = total_score / total_checks if total_checks > 0 else 0
        overall_status = "PASSED" if all_passed and overall_score >= 85.0 else "FAILED"

        # Special handling for violations_only mode
        if violations_only and all_passed:
            report_lines.extend([
                "🎉 NO VIOLATIONS FOUND",
                "   All ADR-005 requirements are met!",
                "=" * 80,
                ""
            ])
        else:
            report_lines.extend([
                "=" * 80,
                f"📊 OVERALL RESULT: {overall_status} ({overall_score:.1f}% average)",
                f"📋 VIOLATIONS SUMMARY: {total_errors} errors, {total_warnings} warnings",
                "=" * 80,
                ""
            ])

        # Show metrics if available
        if self.metrics.end_time > self.metrics.start_time:
            size_change = ""
            if self.metrics.enhanced_size > 0:
                if self.metrics.original_size > 0:
                    change_pct = ((self.metrics.enhanced_size - self.metrics.original_size) / self.metrics.original_size) * 100
                    size_change = f" ({change_pct:+.1f}%)"
                size_change = f"{self.metrics.original_size:,} → {self.metrics.enhanced_size:,} bytes{size_change}"
            else:
                size_change = f"{self.metrics.original_size:,} bytes"

            report_lines.extend([
                "📈 Enhancement Metrics:",
                f"   • Processing Time: {self.metrics.end_time - self.metrics.start_time:.2f}s",
                f"   • Operations Processed: {self.metrics.operations_processed}",
                f"   • Parameters Fixed: {self.metrics.parameters_fixed}",
                f"   • Body Parameters Converted: {self.metrics.body_params_converted}",
                f"   • File Size: {size_change}",
                ""
            ])

            # Show LLM token usage if any tokens were used
            if self.metrics.total_tokens_used > 0:
                report_lines.extend([
                    "🤖 LLM Token Usage:",
                    f"   • Generation Phase:",
                    f"     - Input tokens:  {self.metrics.generation_tokens_input:,}",
                    f"     - Output tokens: {self.metrics.generation_tokens_output:,}",
                    f"     - Total:         {self.metrics.generation_tokens_total:,}",
                    f"   • Validation Phase:",
                    f"     - Input tokens:  {self.metrics.validation_tokens_input:,}",
                    f"     - Output tokens: {self.metrics.validation_tokens_output:,}",
                    f"     - Total:         {self.metrics.validation_tokens_total:,}",
                    f"   • Overall Total:   {self.metrics.total_tokens_used:,} tokens",
                    ""
                ])
            elif self.metrics.llm_calls_made > 0:
                report_lines.extend([
                    "🤖 LLM Usage:",
                    f"   • LLM calls made: {self.metrics.llm_calls_made}",
                    f"   • Token tracking: Not available (using estimates)",
                    ""
                ])

        if all_passed:
            report_lines.extend([
                "🎉 SUCCESS: All ADR-005 requirements met!",
                "   The OpenAPI specification meets all compliance requirements.",
                ""
            ])
        else:
            report_lines.extend([
                "🚨 VALIDATION FAILED: Some ADR-005 requirements not met.",
                f"   Found {total_errors} critical errors and {total_warnings} warnings.",
                "   Please address the issues above before proceeding to production.",
                ""
            ])

        return "\n".join(report_lines)

    def generate_violations_only_report(self, results: Dict[str, ValidationResult]) -> str:
        """
        Generate a focused report showing only violations and issues.
        """
        report_lines = [
            "🚨 COMPLIANCE VIOLATIONS REPORT",
            "=" * 50,
            ""
        ]

        total_errors = 0
        total_warnings = 0
        has_violations = False

        for check_name, result in results.items():
            if result.errors or result.warnings or not result.passed:
                has_violations = True
                status = "FAILED" if not result.passed else "PASSED (with warnings)"
                report_lines.append(f"📋 {check_name.replace('_', ' ').title()}: {status}")
                report_lines.append(f"   Score: {result.score:.1f}%")

                if result.errors:
                    total_errors += len(result.errors)
                    report_lines.append(f"   ❌ Errors ({len(result.errors)}):")
                    for i, error in enumerate(result.errors, 1):
                        report_lines.append(f"      {i}. {error}")

                if result.warnings:
                    total_warnings += len(result.warnings)
                    report_lines.append(f"   ⚠️  Warnings ({len(result.warnings)}):")
                    for i, warning in enumerate(result.warnings, 1):
                        report_lines.append(f"      {i}. {warning}")

                # Show remediation suggestions
                if not result.passed:
                    report_lines.append(f"   🔧 Suggested Actions:")
                    if 'swagger_conversion' in check_name:
                        report_lines.append(f"      • Run enhancement pipeline to convert Swagger 2.0 to OpenAPI 3.x")
                    elif 'parameter_schemas' in check_name:
                        report_lines.append(f"      • Add proper 'schema' fields to parameters missing them")
                        report_lines.append(f"      • Remove direct 'type' fields (use schema.type instead)")
                    elif 'body_parameter' in check_name:
                        report_lines.append(f"      • Convert body parameters to requestBody sections")
                        report_lines.append(f"      • Remove 'in: body' parameters from parameters array")
                    elif 'openapi_compliance' in check_name:
                        report_lines.append(f"      • Ensure OpenAPI 3.x structure compliance")
                        report_lines.append(f"      • Add missing required fields (openapi, info, paths)")

                report_lines.append("")

        if not has_violations:
            report_lines = [
                "✅ NO VIOLATIONS FOUND",
                "=" * 30,
                "",
                "🎉 The OpenAPI specification meets all ADR-005 requirements!",
                "   No compliance issues detected.",
                ""
            ]
        else:
            report_lines.extend([
                "=" * 50,
                f"📊 VIOLATIONS SUMMARY: {total_errors} errors, {total_warnings} warnings",
                "",
                "💡 NEXT STEPS:",
                "   1. Address critical errors first (❌)",
                "   2. Consider fixing warnings (⚠️) for better compliance",
                "   3. Re-run validation after fixes",
                "   4. Use 'enhance' command to auto-fix most issues",
                ""
            ])

        return "\n".join(report_lines)


def load_spec_file(file_path: str) -> Dict[str, Any]:
    """Load an OpenAPI specification from JSON or YAML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.json'):
                return json.load(f)
            else:
                from ruamel.yaml import YAML
                yaml = YAML(typ='safe', pure=True)
                return yaml.load(f)
    except Exception as e:
        logger.error(f"Failed to load spec file {file_path}: {e}")
        return {}
