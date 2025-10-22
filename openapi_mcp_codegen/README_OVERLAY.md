# OpenAPI Overlay Generator for MCP Servers

This module provides tools to generate and apply OpenAPI Overlay specifications to enhance API documentation for better AI agent understanding and MCP server code generation.

## Overview

The OpenAPI Overlay Generator implements the [OpenAPI Overlay Specification 1.0.0](https://www.openapis.org/blog/2024/10/22/announcing-overlay-specification) to enhance API descriptions with agent-friendly documentation. This improves the quality of generated MCP server tools by providing clear, contextual descriptions that help LLM agents better understand when and how to use each API operation.

## Components

### 1. overlay_generator.py

Generates OpenAPI Overlay specifications with enhanced descriptions.

**Features:**
- **LLM-Powered Enhancement**: Uses `LLMFactory().get_llm()` to generate intelligent, context-aware descriptions
- **Rule-Based Fallback**: Provides high-quality enhancements even without LLM
- **Operation-Level Enhancements**: Improves operation summaries and descriptions
- **Parameter-Level Enhancements**: Adds context and guidance for each parameter
- **Use Case Generation**: Suggests common scenarios for using each operation

**Usage:**
```bash
# With LLM enhancement (recommended)
python -m openapi_mcp_codegen.overlay_generator \
    examples/argo-workflows/openapi_argo_workflows.json \
    examples/argo-workflows/overlay.yaml \
    --use-llm

# Without LLM (rule-based)
python -m openapi_mcp_codegen.overlay_generator \
    examples/argo-workflows/openapi_argo_workflows.json \
    examples/argo-workflows/overlay.yaml

# JSON output format
python -m openapi_mcp_codegen.overlay_generator \
    spec.json overlay.json \
    --format json
```

**Python API:**
```python
from openapi_mcp_codegen.overlay_generator import OpenAPIOverlayGenerator

# Create generator with LLM enhancement
generator = OpenAPIOverlayGenerator(
    spec_path='openapi.json',
    use_llm=True
)

# Generate and save overlay
generator.save_overlay('overlay.yaml', format='yaml')
```

### 2. overlay_applier.py

Applies OpenAPI Overlay specifications to OpenAPI documents.

**Usage:**
```bash
python -m openapi_mcp_codegen.overlay_applier \
    original_spec.json \
    overlay.yaml \
    enhanced_spec.json
```

**Python API:**
```python
from openapi_mcp_codegen.overlay_applier import OverlayApplier

applier = OverlayApplier(
    openapi_path='openapi.json',
    overlay_path='overlay.yaml'
)

applier.save_result('enhanced_openapi.json', format='json')
```

### 3. enhance_and_generate.py

Integrated workflow that combines overlay generation, application, and MCP code generation.

**Usage:**
```bash
# Complete workflow with LLM enhancement
python -m openapi_mcp_codegen.enhance_and_generate \
    examples/argo-workflows/openapi_argo_workflows.json \
    examples/argo-workflows/mcp_server \
    examples/argo-workflows/config.yaml

# Save intermediate files for inspection
python -m openapi_mcp_codegen.enhance_and_generate \
    spec.json output/ config.yaml \
    --save-overlay overlay.yaml \
    --save-enhanced-spec enhanced_spec.json

# Only generate and apply overlay (skip MCP generation)
python -m openapi_mcp_codegen.enhance_and_generate \
    spec.json output/ config.yaml \
    --overlay-only \
    --save-overlay overlay.yaml \
    --save-enhanced-spec enhanced_spec.json
```

## How It Works

### 1. Enhancement Strategy

The overlay generator enhances OpenAPI specifications in several ways:

#### Operation Descriptions
- **Purpose**: What the operation accomplishes
- **Use Cases**: When and why to use it
- **Key Parameters**: What inputs are needed
- **Expected Behavior**: What happens when called

#### Parameter Descriptions
- **Context**: How the parameter fits into the operation
- **Usage Guidance**: When to include optional parameters
- **Type Information**: Expected data types and formats
- **Pattern Recognition**: Special handling for common patterns (pagination, filtering, etc.)

### 2. LLM Enhancement

When `--use-llm` is enabled, the generator uses `LLMFactory().get_llm()` to create intelligent descriptions:

```python
llm = LLMFactory().get_llm()

system_msg = SystemMessage(
    content=(
        "You are an expert API documentation writer specializing in "
        "creating agent-friendly documentation. Your task is to write "
        "clear, concise API operation descriptions that help AI agents "
        "understand when and how to use the API..."
    )
)

response = llm.invoke([system_msg, HumanMessage(content=user_prompt)])
```

The LLM enhancement:
- Understands API semantics and patterns
- Generates context-aware descriptions
- Provides actionable guidance for AI agents
- Falls back to rule-based generation on errors

### 3. Overlay Structure

Generated overlays follow the OpenAPI Overlay Specification 1.0.0:

```yaml
overlay: 1.0.0
info:
  title: MCP Agent Enhancement Overlay for Argo Workflows
  version: 1.0.0
  description: Enhances the OpenAPI specification with agent-friendly descriptions...

actions:
  - target: "$.paths['/api/v1/workflows'].get.description"
    update: |
      **Purpose:** List or query workflows in the system

      **Use Cases:**
      - When you need to discover available workflows
      - To monitor workflow states across the system

      **Key Parameters:**
      - namespace: Filter workflows by Kubernetes namespace
      - labelSelector: Filter by labels for targeted queries

  - target: "$.paths['/api/v1/workflows'].get.parameters[0].description"
    update: |
      Namespace parameter for scoping workflow queries.
      Use this to limit results to a specific Kubernetes namespace.
      Optional - omit to search across all namespaces.
```

## Benefits for MCP Servers

Enhanced OpenAPI specifications lead to better MCP server code generation:

1. **Clearer Tool Descriptions**: AI agents understand what each tool does
2. **Better Parameter Guidance**: Agents know when and how to use parameters
3. **Use Case Context**: Agents learn appropriate scenarios for each operation
4. **Improved Decision Making**: Better documentation helps agents choose the right tools

### Before Enhancement

```python
async def list_workflows(namespace: str = None) -> Any:
    """


    OpenAPI Description:


    Args:
        namespace (str): OpenAPI parameter corresponding to 'namespace'


    Returns:
        Any: The JSON response from the API call.
    """
```

### After Enhancement

```python
async def list_workflows(namespace: str = None) -> Any:
    """
    **Purpose:** List and query workflows across the system

    Use this operation when you need to discover available workflows,
    monitor workflow states, or find workflows matching specific criteria.

    **Key Parameters:**
    - namespace: Scope results to a specific Kubernetes namespace. Omit to
      search all namespaces.
    - labelSelector: Filter workflows using Kubernetes label selectors for
      targeted queries.

    **Common Use Cases:**
    - Discovering all workflows in a namespace
    - Finding workflows with specific labels or states
    - Monitoring workflow execution across the cluster

    Returns:
        Any: List of workflow objects with their current states and metadata
    """
```

## Integration with mcp_codegen.py

The overlay generator integrates seamlessly with the existing code generator:

1. **Generate Overlay**: Create enhanced descriptions
2. **Apply Overlay**: Produce enhanced OpenAPI spec
3. **Generate MCP Code**: Use enhanced spec for better tool generation

### Fixing Double Underscores

The updated `camel_to_snake` function in `mcp_codegen.py` now removes double underscores:

```python
def camel_to_snake(name):
    if name.isupper():
        return "_".join(name).lower()
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    s2 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    # Replace multiple underscores with a single underscore
    s3 = re.sub(r'_+', '_', s2)
    return s3
```

Before: `archived_workflow_service__list_archived_workflows`
After: `archived_workflow_service_list_archived_workflows`

## Requirements

### Required
- Python 3.8+
- PyYAML
- jsonpath-ng (for overlay applier)

### Optional (for LLM enhancement)
- cnoe_agent_utils
- langchain-core

Install dependencies:
```bash
pip install pyyaml jsonpath-ng

# For LLM enhancement
pip install cnoe_agent_utils langchain-core
```

## Examples

### Example 1: Generate Overlay for Argo Workflows

```bash
python -m openapi_mcp_codegen.overlay_generator \
    examples/argo-workflows/openapi_argo_workflows.json \
    examples/argo-workflows/overlay.yaml \
    --use-llm \
    --verbose
```

### Example 2: Apply Overlay and Generate MCP Code

```bash
# Complete workflow
python -m openapi_mcp_codegen.enhance_and_generate \
    examples/argo-workflows/openapi_argo_workflows.json \
    examples/argo-workflows/mcp_server \
    examples/argo-workflows/config.yaml \
    --save-overlay examples/argo-workflows/overlay.yaml \
    --save-enhanced-spec examples/argo-workflows/enhanced_openapi.json
```

### Example 3: Manual Process

```bash
# Step 1: Generate overlay
python -m openapi_mcp_codegen.overlay_generator \
    spec.json overlay.yaml --use-llm

# Step 2: Apply overlay
python -m openapi_mcp_codegen.overlay_applier \
    spec.json overlay.yaml enhanced_spec.json

# Step 3: Generate MCP code
python -m openapi_mcp_codegen.mcp_codegen \
    enhanced_spec.json output_dir/ config.yaml
```

## References

- [OpenAPI Overlay Specification 1.0.0](https://www.openapis.org/blog/2024/10/22/announcing-overlay-specification)
- [OpenAPI Initiative](https://www.openapis.org/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)

## License

Copyright 2025 CNOE
SPDX-License-Identifier: Apache-2.0

