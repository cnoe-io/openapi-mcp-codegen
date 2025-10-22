# OpenAPI Specification Fixes and Enhancements

## Summary

This document describes the automatic fixes applied to OpenAPI specifications to ensure compatibility with AgentGateway and OpenAPI 3.x standards.

## Issues Fixed

### 1. Swagger 2.0 to OpenAPI 3.x Conversion

**Problem:** Many API specs are still in Swagger 2.0 format, which uses different structure than OpenAPI 3.x.

**Solution:** Automatically detect and convert Swagger 2.0 specs to OpenAPI 3.x:
- Convert `swagger: "2.0"` to `openapi: "3.0.0"`
- Convert `host`, `basePath`, and `schemes` to `servers` array
- Example:
  ```yaml
  # Swagger 2.0
  swagger: "2.0"
  host: "localhost:2746"
  basePath: ""
  schemes: ["http"]

  # Converted to OpenAPI 3.x
  openapi: "3.0.0"
  servers:
    - url: "http://localhost:2746"
  ```

### 2. Missing Parameter Schemas

**Problem:** 349 parameters were missing both `schema` and `content` fields, which are required in OpenAPI 3.x.

**Solution:** Automatically infer and add appropriate schemas based on parameter names:
- **Integer types:** limit, timeout, seconds, nanos, period, retries, count, size, port, lines, bytes
- **Boolean types:** watch, follow, previous, timestamps, orphan, force, enabled, allow, skip, insecure, stream
- **String types:** All other parameters (default)

Example:
```yaml
# Before
- name: limit
  in: query

# After
- name: limit
  in: query
  schema:
    type: integer
```

### 3. Invalid Body Parameters

**Problem:** 29 parameters had `in: body`, which is Swagger 2.0 syntax and invalid in OpenAPI 3.x.

**Solution:** Remove these parameters from the `parameters` array. In OpenAPI 3.x, request bodies should be defined using the `requestBody` field instead.

Example:
```yaml
# Before (Swagger 2.0 style)
parameters:
  - name: body
    in: body
    schema: {...}

# After (OpenAPI 3.x style)
parameters: []
requestBody:
  content:
    application/json:
      schema: {...}
```

## Implementation

The fixes are automatically applied in the `enhance_and_generate.py` script in step 2.1:

```python
# Step 2.1: Validating and Fixing OpenAPI Parameters
fixed_count = _fix_openapi_parameters(enhanced_spec_path)
```

### Function: `_fix_openapi_parameters()`

Located in: `openapi_mcp_codegen/enhance_and_generate.py`

This function:
1. Detects Swagger 2.0 specs and converts them to OpenAPI 3.x
2. Removes invalid `body` parameters
3. Adds missing `schema` fields with inferred types
4. Saves the fixed specification

## Validation

A test script is provided to validate OpenAPI specifications:

```bash
# Validate a spec
python tests/test_openapi_validation.py path/to/spec.json

# Validate with verbose output
python tests/test_openapi_validation.py path/to/spec.json -v
```

The test script checks for:
- Parameters with neither `schema` nor `content`
- Invalid `body` parameters (Swagger 2.0 style)

## Usage

### Generate Enhanced MCP Server (with automatic fixes)

```bash
cd examples/argo-workflows
make generate-enhanced
```

Or use the script directly:

```bash
python -m openapi_mcp_codegen.enhance_and_generate \
    openapi_argo_workflows.json \
    mcp_server \
    config.yaml \
    --save-overlay overlay.yaml \
    --save-enhanced-spec enhanced_openapi.json
```

### Validate a Spec

```bash
cd examples/argo-workflows
make validate                 # Validate enhanced spec
make validate-original        # Validate original spec
```

## Results

For the Argo Workflows example:
- ✅ Converted from Swagger 2.0 to OpenAPI 3.0.0
- ✅ Fixed 349 parameters missing schema definitions
- ✅ Removed 29 invalid 'body' parameters
- ✅ AgentGateway loads the spec without errors
- ✅ All validation tests pass

## AgentGateway Configuration

Example `agw.yaml` configuration:

```yaml
binds:
- port: 3000
  listeners:
  - routes:
    - policies:
        cors:
          allowOrigins:
            - "*"
          allowHeaders:
            - "*"
      backends:
      - mcp:
          targets:
          - name: openapi
            openapi:
              schema:
                file: enhanced_openapi.json
              host: localhost
              port: 2746
              path: /
```

**Important:** Make sure to specify `path: /` when using `port` in the OpenAPI backend configuration.

## Related Files

- `openapi_mcp_codegen/enhance_and_generate.py` - Main enhancement script
- `tests/test_openapi_validation.py` - Validation test script
- `examples/argo-workflows/Makefile` - Example usage commands

## References

- [OpenAPI 3.0 Specification](https://spec.openapis.org/oas/v3.0.0)
- [Swagger 2.0 Specification](https://swagger.io/specification/v2/)
- [AgentGateway Documentation](https://github.com/cnoe-io/agent-gateway)


