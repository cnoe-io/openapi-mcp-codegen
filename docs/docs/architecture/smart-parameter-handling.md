# Smart Parameter Handling

Smart parameter handling solves the problem of complex API schemas that would generate unusable functions with thousands of parameters.

## The Problem

Kubernetes-style APIs often have deeply nested schemas:
- 1000+ nested parameters in a single operation
- Generated functions become unusable (5,735 lines)
- AI agents cannot effectively use complex function signatures

## The Solution

**Automatic Complexity Detection**:
- Count nested parameters in request schemas
- If >10 parameters detected, switch to dictionary mode
- Maintain type safety through Dict[str, Any] interfaces

## Impact

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Function Size | 5,735 lines | 82 lines | **98.6% reduction** |
| Parameter Count | 1,000+ | 7 | **99.3% reduction** |
| Usability | Unusable | Clean interface | **AI & human friendly** |

For technical implementation details, see [ADR-001](../adr/ADR-001-openapi-mcp-architecture.md#smart-parameter-handling-algorithm).
