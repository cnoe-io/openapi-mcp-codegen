# MCP Examples generated with openapi_mcp_codegen

## Petstore OpenAPI to MCP Generator

- [Petstore](https://petstore3.swagger.io/api/v3/openapi.json)

```
make generate -- --spec-file examples/petstore/openapi_petstore.json --output-dir examples/petstore/mcp_server
```

## ArgoCD OpenAPI to MCP Generator

- [ArgoCD OpenAPI Spec](./argocd/argocd_openapi.json)

```
make generate -- --spec-file examples/argocd/openapi_argocd.json --output-dir examples/argocd/mcp_server
```