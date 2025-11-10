# CLI Commands

## Main Commands

### openapi_mcp_codegen

Primary command for generating MCP servers:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file INPUT_SPEC \
  --output-dir OUTPUT_DIR \
  [OPTIONS]
```

### enhance_and_generate

Enhanced generation with LLM optimization:

```bash
python -m openapi_mcp_codegen.enhance_and_generate \
    INPUT_SPEC \
    OUTPUT_DIR \
    CONFIG_FILE \
    [OPTIONS]
```

### overlay_generator

Generate OpenAPI overlays:

```bash
python -m openapi_mcp_codegen.overlay_generator \
    INPUT_SPEC \
    OUTPUT_OVERLAY \
    [--use-llm]
```

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--generate-agent` | Create LangGraph agent | `false` |
| `--generate-eval` | Include evaluation framework | `false` |
| `--save-overlay` | Save generated overlay | Not saved |
| `--enhance-docstring-with-llm` | LLM docstring enhancement | `false` |

For complete option reference, run with `--help`.
