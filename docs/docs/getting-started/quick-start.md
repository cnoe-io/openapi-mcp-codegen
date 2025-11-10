# Quick Start

Get up and running with OpenAPI MCP Codegen in minutes.

## Prerequisites

- **Python 3.8+**
- **uv package manager** (recommended) or pip
- An OpenAPI specification file (JSON or YAML)

## Installation

Install uv if you haven't already:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Generate Your First MCP Server

Generate a complete MCP server from an OpenAPI specification:

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir examples/petstore \
  --generate-agent \
  --generate-eval
```

This command will:
- ✅ Generate a production-ready MCP server
- ✅ Create a LangGraph React agent
- ✅ Include evaluation and testing frameworks
- ✅ Provide configuration templates

## What Gets Generated

After running the generator, you'll have:

```
examples/petstore/
├── mcp_server/                  # MCP server package
│   ├── pyproject.toml
│   ├── README.md
│   ├── .env.example
│   └── mcp_petstore/
│       ├── server.py            # MCP server entry point
│       ├── api/client.py        # HTTP API client
│       ├── models/base.py       # Data models
│       └── tools/               # Generated tool modules
├── agent/                       # LangGraph agent
│   ├── agent.py
│   ├── a2a_server.py
│   └── Makefile
└── eval/                        # Evaluation framework
    ├── evaluate_agent.py
    └── dataset.yaml
```

## Test Your MCP Server

1. **Configure Environment**:
   ```bash
   cd examples/petstore
   cp .env.example .env
   # Edit .env with your API credentials and LLM keys
   ```

2. **Start the Mock API** (for testing):
   ```bash
   uv run python petstore_mock_server.py
   ```

3. **Run the Agent** (in a new terminal):
   ```bash
   make run-a2a
   ```

4. **Test with Client** (in a new terminal):
   ```bash
   make run-a2a-client
   ```

## Try Some Commands

Once your agent is running, try these natural language commands:

- `"List all pets"`
- `"Add a new pet named Fluffy"`
- `"Find pets with status available"`
- `"Get details for pet ID 123"`

## Next Steps

- [Configure your environment](./configuration.md) for production use
- [Explore examples](./examples.md) with different APIs
- [Learn about the architecture](../architecture/overview.md)
- [Understand the enhancement pipeline](../enhancement/openapi-overlay.md)

## Enhanced Generation with LLM

For AI-optimized MCP servers with enhanced documentation:

```bash
# Set your LLM API key
export OPENAI_API_KEY=your-key-here

# Generate with LLM enhancements
python -m openapi_mcp_codegen.enhance_and_generate \
    examples/argo-workflows/openapi_argo_workflows.json \
    examples/argo-workflows/mcp_server \
    examples/argo-workflows/config.yaml \
    --save-overlay overlay.yaml \
    --save-enhanced-spec enhanced_openapi.json
```

This will:
- 🤖 Use GPT-4/Claude to enhance API descriptions
- 📝 Generate OpenAI-compatible tool descriptions
- ⚡ Create optimized parameter handling
- 🔧 Produce production-ready code

## Troubleshooting

**Command not found?**
- Make sure uv is installed and in your PATH
- Try using the full git URL in the uvx command

**Generation fails?**
- Check that your OpenAPI spec is valid JSON/YAML
- Ensure you have proper file permissions in the output directory
- Review the error messages for specific issues

**Need help?**
- Check our [troubleshooting guide](../cli/troubleshooting.md)
- Visit the [GitHub repository](https://github.com/cnoe-io/openapi-mcp-codegen) for issues and discussions