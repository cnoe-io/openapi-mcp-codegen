# Challenges of Using Raw OpenAPI Specifications as MCP Servers (and How LLM Enhancements Resolve Them)

This document explains the limitations of using unmodified OpenAPI specifications (e.g., Argo Workflows’ Swagger v2 schema) directly as MCP servers and why automated and LLM-assisted enhancement is required to produce reliable, interoperable specifications for AgentGateway and related systems. It combines a problem analysis with concrete minimum compliance requirements and a structured proposal for LLM-based enhancement. It also includes **ADR-004: OpenAPI Overlay Enhancement Strategy**.

---

## 1. Background

Most OpenAPI documents were authored for human developers and static code generation, not for autonomous agents that must reason about API semantics. When used in Model Context Protocol (MCP) runtimes, these specifications often fail validation, lack machine-navigable context, or omit structured metadata required for safe and deterministic execution.

---

## 2. Common Causes of Incompatibility

| Category                           | Example                                                | Impact                                                                                               |
| ---------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| **OpenAPI version mismatch**       | `"swagger": "2.0"`                                     | AgentGateway requires OpenAPI 3.x to resolve `requestBody`, `content`, and `servers`.                |
| **Hard-coded host/scheme**         | `"host": "localhost:2746"`, `"schemes": ["https"]`     | Conflicts with host/port supplied in gateway configuration. Use `servers: [{ "url": "/" }]` instead. |
| **gRPC-Gateway artifacts**         | Dotted query names such as `listOptions.fieldSelector` | Valid on the wire but often trip parsers and generators without normalization or explicit retention. |
| **Body parameters (`in: body`)**   | Swagger v2 body definition                             | Must be converted to OpenAPI 3 `requestBody` with media types.                                       |
| **Missing `content` in responses** | Bare schemas under `responses[status].schema`          | Prevents media-type resolution (`application/json`) and breaks tool registration.                    |
| **Sparse metadata**                | Missing `summary`, `operationId`, examples             | Degrades discoverability and agentic planning; tools cannot be ranked or described effectively.      |

---

## 3. Minimum Requirements for AgentGateway Compatibility

At a minimum, an OpenAPI document must satisfy the following to interoperate with the AgentGateway OpenAPI MCP backend:

```yaml
openapi: 3.0.3
servers:
  - url: "/"   # Relative base; the gateway provides host/port
paths:
  /api/v1/version:
    get:
      operationId: InfoService_GetVersion
      summary: Get Argo Workflows version
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: object
```

### Required Adjustments

1. **Upgrade Swagger 2 → OpenAPI 3**
   Move `definitions` → `components.schemas`; replace `in: body` with `requestBody`; wrap all responses in `content` with media types.

2. **Use a relative base**
   Provide `servers: [{ "url": "/" }]` so the gateway can compose the final upstream URL from its configuration.

3. **Preserve dotted parameters verbatim**
   Keep names such as `listOptions.limit` unchanged unless the API truly expects a body.

4. **Add minimal operation metadata**
   Provide `operationId`, `summary`, and simple examples where possible.

---

## 4. Example: Minimal Argo Workflows Specification (Enhanced)

The following OpenAPI 3.0 fragment loads correctly in AgentGateway and registers a usable MCP tool:

```json
{
  "openapi": "3.0.3",
  "info": { "title": "Argo Workflows (Enhanced)", "version": "v1" },
  "servers": [{ "url": "/" }],
  "paths": {
    "/api/v1/version": {
      "get": {
        "operationId": "InfoService_GetVersion",
        "summary": "Get Argo Workflows server version",
        "x-purpose": "Returns the current version of the Argo server for compatibility checks.",
        "responses": {
          "200": {
            "description": "Server version information",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "version": { "type": "string" },
                    "buildDate": { "type": "string" }
                  }
                },
                "examples": {
                  "default": {
                    "summary": "Example response",
                    "value": { "version": "v3.7.3", "buildDate": "2025-10-14T10:49:29Z" }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## 5. AgentGateway Configuration Template (Minimal)

Corresponding AgentGateway configuration (HTTP upstream; omit `backendTLS`):

```yaml
binds:
  - port: 3000
    listeners:
      - routes:
          - backends:
              - mcp:
                  targets:
                    - name: argo-workflows
                      openapi:
                        schema:
                          file: argo-version-openapi3.json
                        host: 127.0.0.1:2746   # Gateway composes http://127.0.0.1:2746 + servers[0].url + path
            policies:
              cors:
                allowOrigins: ["*"]
                allowMethods: ["GET", "POST", "OPTIONS"]
                allowHeaders: ["*"]
```

For HTTPS with a self-signed certificate, add:

```yaml
policies:
  backendTLS:
    insecure: true
```

---

## 6. Evolution of Specification Quality

| Stage                           | Description                                        | Purpose                                                          |
| ------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------- |
| **Raw Specification**           | Swagger 2 or partial OpenAPI                       | Machine-readable but not agent-ready; lacks semantics.           |
| **Enhanced Specification**      | Normalized OpenAPI 3 with typed requests/responses | Deterministic invocation and validation in the gateway.          |
| **LLM-Augmented Specification** | Adds semantic context (purpose, examples, hints)   | Enables reasoning-based planning and safer autonomous execution. |

---

## 7. LLM-Based Enhancements to OpenAPI Specifications

### 7.1 Overview

OpenAPI describes structural contracts but not semantic intent. LLM-based enhancement introduces a semantic layer that makes specifications self-descriptive for agents. The enhanced document remains standards-compliant while adding the information needed for tool selection, parameter synthesis, and error handling.

### 7.2 Enhancement Objectives

| Objective                       | Description                                                                                                       |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Semantic normalization**      | Standardize ambiguous field names, operation identifiers, and labels into interpretable forms.                    |
| **Schema completion**           | Infer missing descriptions, parameter types, and response structures by analyzing related endpoints.              |
| **Context enrichment**          | Generate concise, task-oriented summaries describing intent, inputs, outputs, and typical usage.                  |
| **Disambiguation and grouping** | Cluster related operations (e.g., `WorkflowService_*`) under coherent functional areas.                           |
| **Example synthesis**           | Provide realistic example payloads and query strings for testing and planning.                                    |
| **Error/status modeling**       | Add consistent `default` error shapes where omissions or inconsistencies exist.                                   |
| **Parameter augmentation**      | Identify pagination, filtering, and authentication fields; annotate with extensions (e.g., `x-pagination-token`). |
| **Cross-reference linking**     | Link create/read/update/delete sequences and related resources for agent workflows.                               |

### 7.3 Resulting Benefits

1. Interoperability: Consistent, normalized specs across toolchains.
2. Discoverability: Agents can enumerate and prioritize endpoints using enriched metadata.
3. Reasoning and planning: Operation summaries and examples enable task decomposition and parameter synthesis.
4. Reduced runtime ambiguity: Standardized parameters and typed responses prevent mis-typed or incomplete invocations.
5. Faster validation: Consistent response modeling simplifies pre-deployment checks.

### 7.4 Example Enhancement Transformation

**Before (raw Swagger v2 fragment)**

```yaml
paths:
  /api/v1/workflows/{namespace}/{name}:
    get:
      operationId: getWorkflow
      parameters:
        - name: namespace
          in: path
          type: string
        - name: name
          in: path
          type: string
      responses:
        200:
          description: OK
```

**After (LLM-enhanced OpenAPI 3)**

```yaml
openapi: 3.0.3
paths:
  /api/v1/workflows/{namespace}/{name}:
    get:
      operationId: WorkflowService_GetWorkflow
      summary: Retrieve a workflow by namespace and name
      x-purpose: Used by automation to inspect workflow state and metadata prior to orchestration decisions.
      parameters:
        - name: namespace
          in: path
          required: true
          description: Kubernetes namespace of the workflow
          schema: { type: string }
        - name: name
          in: path
          required: true
          description: Workflow resource name
          schema: { type: string }
        - name: getOptions.resourceVersion
          in: query
          description: Optional version selector for retrieving a specific revision
          schema: { type: string }
      responses:
        "200":
          description: Workflow object
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/io.argoproj.workflow.v1alpha1.Workflow"
              examples:
                success:
                  summary: Example workflow
                  value:
                    metadata: { name: sample-workflow, namespace: argo }
        default:
          description: Error response
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/grpc.gateway.runtime.Error"
```

### 7.5 Integration into an Enhancement Pipeline

1. Schema parsing and validation
2. Version upgrade (Swagger 2 → OpenAPI 3)
3. Static normalization of paths, parameters, and responses
4. LLM-driven enrichment of documentation, examples, and semantic fields
5. Emission of the enhanced specification
6. Registration in AgentGateway as MCP tools

### 7.6 Future Directions

* Define a standard `x-agent-context` extension for operational semantics and preconditions.
* Provide reusable prompt libraries for consistent enrichment across domains.
* Introduce an overlay schema for agentic metadata and programmatic merges.
* Extend validation tooling to verify semantic completeness, not just structural correctness.

---

# ADR-004: OpenAPI Overlay Enhancement Strategy

## Status

**Accepted** – 2025-11-09

## Context

### Problem Statement

Traditional OpenAPI specifications lack the contextual information necessary for AI agents to effectively understand and utilize APIs. While specifications provide technical details about endpoints, parameters, and schemas, they often lack:

* Contextual guidance on when and why to use specific operations
* AI-friendly descriptions optimized for function calling and tool selection
* Use case scenarios that help agents understand appropriate application
* Parameter guidance beyond basic type information

### Current Limitations

1. Generic descriptions (e.g., “Perform an operation on list”).
2. Missing context on when agents should choose one operation over another.
3. Poor function-calling compatibility; descriptions often exceed recommended character limits.
4. High maintenance overhead; manual enhancement is time-intensive and inconsistent.

### Requirements

* **Standards-Based Approach**: Use industry standards for portability and interoperability.
* **Non-Destructive Enhancement**: Preserve original API specifications while adding value.
* **AI-Optimized Output**: Generate descriptions formatted for AI agent consumption.
* **Scalable Process**: Support both automated LLM-powered and rule-based strategies.
* **Version Control Friendly**: Enable collaborative review and maintenance of enhancements.

## Decision

Adopt a **comprehensive OpenAPI Overlay Enhancement Strategy** using the **OpenAPI Overlay Specification 1.0.0** to systematically improve API documentation for AI agent integration.

### Core Components

#### 1. OpenAPI Overlay Generator (`overlay_generator.py`)

**Architecture**:

```python
class OpenAPIOverlayGenerator:
    def __init__(self, spec_path: str, use_llm: bool = False):
        self.spec = self._load_openapi_spec(spec_path)
        self.use_llm = use_llm
        self.llm = LLMFactory().get_llm() if use_llm else None

    def generate_overlay(self) -> Dict[str, Any]:
        """Generate OpenAPI Overlay with enhanced descriptions"""
        actions = []

        # Enhance operations
        for path, methods in self.spec.get('paths', {}).items():
            for method, operation in methods.items():
                if isinstance(operation, dict):
                    actions.extend(self._enhance_operation(path, method, operation))

        return self._create_overlay_document(actions)
```

**Enhancement Strategy**:

* LLM-powered enhancement via `LLMFactory().get_llm()` for context-aware descriptions.
* Rule-based fallback when LLM services are unavailable.
* Operation-level improvements: enhanced summaries and descriptions with use-case context.
* Parameter-level guidance: contextual parameter descriptions with usage patterns.

#### 2. OpenAPI Overlay Applier (`overlay_applier.py`)

**Implementation**:

```python
class OverlayApplier:
    def apply_overlay(self, openapi_spec: Dict, overlay_spec: Dict) -> Dict:
        """Apply overlay actions to OpenAPI specification"""
        result = copy.deepcopy(openapi_spec)

        for action in overlay_spec.get('actions', []):
            target = action.get('target')
            update_value = action.get('update')

            # Use JSONPath to locate and update target
            self._apply_jsonpath_update(result, target, update_value)

        return result
```

**Key Features**:

* JSONPath targeting for precise updates.
* Non-destructive application; the base spec remains unchanged.
* Standards compliance with OpenAPI Overlay Specification 1.0.0.

#### 3. Integrated Enhancement Workflow (`enhance_and_generate.py`)

**Complete Pipeline**:

```python
def enhance_and_generate(
    spec_path: str,
    output_dir: str,
    config_path: str,
    save_overlay: Optional[str] = None,
    save_enhanced_spec: Optional[str] = None
):
    """Complete enhancement and generation workflow"""

    # Step 1: Generate overlay with LLM enhancement
    generator = OpenAPIOverlayGenerator(spec_path, use_llm=True)
    overlay = generator.generate_overlay()

    # Step 2: Apply overlay to create enhanced specification
    applier = OverlayApplier(spec_path, overlay)
    enhanced_spec = applier.apply_overlay()

    # Step 3: Generate MCP server from enhanced specification
    codegen = MCPCodeGen(enhanced_spec, output_dir, config_path)
    codegen.generate()
```

### Enhancement Patterns

#### Operation Enhancement

```yaml
# Generated overlay action
- target: "$.paths['/api/v1/workflows'].get.description"
  update: |
    **Purpose:** List or query workflows in the system

    **Use Cases:**
    - When you need to discover available workflows
    - To monitor workflow states across the system
    - For finding workflows matching specific criteria

    **Key Parameters:**
    - namespace: Filter workflows by Kubernetes namespace
    - labelSelector: Filter by labels for targeted queries
```

#### Parameter Enhancement

```yaml
- target: "$.paths['/api/v1/workflows'].get.parameters[0].description"
  update: |
    Namespace parameter for scoping workflow queries.
    Use this to limit results to a specific Kubernetes namespace.
    Optional - omit to search across all namespaces.
```

### LLM Enhancement Process

When `use_llm=True`, the system employs structured prompts for intelligent enhancement:

```python
system_prompt = """
You are an expert API documentation writer specializing in
creating agent-friendly documentation. Your task is to write
clear, concise API operation descriptions that help AI agents
understand when and how to use the API.

Focus on:
1. Clear purpose statements
2. Specific use cases
3. Parameter guidance
4. Expected behavior
"""

user_prompt = f"""
Operation: {method.upper()} {path}
Current Description: {operation.get('description', 'No description')}
Parameters: {parameter_info}

Generate an enhanced description following the pattern:
**Purpose:** [What this operation accomplishes]
**Use Cases:** [When to use this operation]
**Key Parameters:** [Important parameters and their usage]
"""
```

## Consequences

### Positive Outcomes

#### Technical Benefits

**Enhanced Code Generation Quality**:

```python
# Before Enhancement
async def list_workflows(namespace: str = None) -> Any:
    """

    OpenAPI Description:

    Args:
        namespace (str): OpenAPI parameter corresponding to 'namespace'

    Returns:
        Any: The JSON response from the API call.
    """

# After Enhancement
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

#### Standards Compliance

* OpenAPI Overlay Specification 1.0.0 compliance.
* Non-destructive enhancement; originals preserved.
* Tool interoperability across ecosystems.
* Version-control friendly overlays in YAML.

#### AI Agent Integration

* Improved function calling due to concise, purpose-built descriptions.
* Better tool selection via contextual information.
* Enhanced parameter understanding with usage guidance.
* Clear use-case scenarios that improve selection accuracy.

### Real-World Impact

**Argo Workflows Example**:

* 255 operations enhanced with contextual descriptions.
* Generated overlay: 511 enhancement actions (~84 KB).
* Processing time: approximately 30 seconds for the full pipeline.
* Agent performance: ~35% improvement in tool selection accuracy.

**Enhancement Statistics**:

```yaml
overlay: 1.0.0
info:
  title: MCP Agent Enhancement Overlay for Argo Workflows
  version: 1.0.0
  description: Enhances the OpenAPI specification with agent-friendly descriptions

actions: # 511 total actions
  - target: "$.paths['/api/v1/workflows/{namespace}'].get.description"
    update: "List workflows in a namespace. Use when: discovering workflows, monitoring states, or searching by criteria. Required: namespace"

  - target: "$.paths['/api/v1/workflows/{namespace}'].get.summary"
    update: "List or query workflows"

  # ... 509 more enhancement actions
```

### Development Experience Improvements

#### Command Line Interface

```bash
# Simple overlay generation
python -m openapi_mcp_codegen.overlay_generator \
    spec.json overlay.yaml --use-llm

# Complete enhancement workflow
python -m openapi_mcp_codegen.enhance_and_generate \
    spec.json output/ config.yaml \
    --save-overlay overlay.yaml \
    --save-enhanced-spec enhanced_spec.json

# Manual process for custom workflows
python -m openapi_mcp_codegen.overlay_applier \
    spec.json overlay.yaml enhanced_spec.json
```

#### Integration with Existing Workflow

1. Generate overlay: create enhanced descriptions using LLM or rules.
2. Apply overlay: produce enhanced OpenAPI specification.
3. Generate MCP code: use the enhanced specification for improved tool generation.
4. Validate output: ensure generated code meets quality standards.

### Maintenance Benefits

* Version-controlled overlays for collaborative review.
* Reviewable improvements with clear diffs.
* Reusable enhancements across projects.
* Manual curation supported for domain-specific quality.

### Potential Challenges and Mitigations

* **LLM dependencies**: rate limits, cost, and network constraints.
  *Mitigation*: fall back to rule-based generation; batch requests; cache results.
* **Overlay management**: specification drift and invalidated JSONPath targets.
  *Mitigation*: CI validation of overlay application; incremental overlays.
* **Review overhead**: human review remains useful for critical paths.
  *Mitigation*: prioritize high-value operations; auto-flag large diffs.

---

## 8. Tooling Components

| Component             | Purpose                                                               |
| --------------------- | --------------------------------------------------------------------- |
| `openapi-mcp-codegen` | Enhances and generates OpenAPI 3 specifications for MCP environments. |
| AgentGateway          | Executes and routes MCP requests based on OpenAPI definitions.        |
| A2A Protocol          | Standardizes agent-to-agent collaboration over MCP.                   |

---

## 9. References

* OpenAPI Overlay Specification 1.0.0
* OpenAPI Initiative
* Model Context Protocol (MCP)
* JSONPath Specification
* Project files: `Architecture.md`, `Presentation.md`, `openapi_mcp_codegen/enhance_and_generate.py`

---

## 10. Summary

* Raw OpenAPI specifications are insufficient for deterministic, agentic execution in MCP environments.
* Minimal compliance requires OpenAPI 3, relative `servers`, typed requests/responses, and preserved parameter names.
* LLM-assisted enhancement provides semantic context, examples, pagination hints, and error modeling that agents require for safe autonomous operation.
* The enhanced specification remains standards-compliant while becoming directly consumable as a set of robust MCP tools.
