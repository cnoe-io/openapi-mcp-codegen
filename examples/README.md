# MCP Examples generated with openapi_mcp_codegen

## Petstore OpenAPI to MCP Generator

- [Petstore](https://petstore3.swagger.io/api/v3/openapi.json)

### Generate without LLM docstring enhancements

```
make generate -- --spec-file examples/petstore/openapi_petstore.json --output-dir examples/petstore/mcp_server
```

### Generate with LLM docstring enhancements

```
make generate -- --spec-file examples/petstore/openapi_petstore.json --output-dir examples/petstore/mcp_server --enhance-docstring-with-llm
```

### Generate with LLM docstring enhancements with OpenAPI Spec

```
make generate -- --spec-file examples/petstore/openapi_petstore.json --output-dir examples/petstore/mcp_server --enhance-docstring-
with-llm-openapi
```

## ArgoCD OpenAPI to MCP Generator

- [ArgoCD OpenAPI Spec](./argocd/argocd_openapi.json)

```
make generate -- --spec-file examples/argocd/openapi_argocd.json --output-dir examples/argocd/mcp_server
```

### Generate with LLM docstring enhancements

```
make generate -- --spec-file examples/argocd/openapi_argocd.json --output-dir examples/argocd/mcp_server --enhance-docstring-with-llm
```

### Generate with LLM docstring enhancements with OpenAPI Spec

```
make generate -- --spec-file examples/petstore/openapi_argocd.json --output-dir examples/argocd/mcp_server --enhance-docstring-
with-llm-openapi
```
