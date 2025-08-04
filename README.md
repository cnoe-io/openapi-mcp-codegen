# 🚀 OpenAPI to MCP Server Code Generator

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Conventional Commits](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/conventional_commits.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/conventional_commits.yml)
[![Ruff Linter](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/ruff.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/ruff.yml)
[![Super Linter](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/superlinter.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/superlinter.yml)
[![Unit Tests](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/unittest.yaml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/unittest.yaml)
[![Dependabot Updates](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/dependabot/dependabot-updates)

---

Easily generate a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server from any OpenAPI specification!

This tool helps you bootstrap new MCP servers for any API with an OpenAPI spec.

---

## ✨ Features

- ⚡ **Automatic MCP server generation** from OpenAPI specs
- 📝 Supports **JSON** and **YAML** formats
- 🔍 **Auto-detects** spec file type (`.json`, `.yaml`, `.yml`)
- 🛠️ **Tool modules** for each API endpoint
- 🤖 **API client code** generation
- 📋 **Logging** & **error handling** setup
- ⚙️ **Configuration files** (`pyproject.toml`, `.env.example`)
- 📚 **Comprehensive documentation** generation
- 🤖 **Enhanced Docstrings via LLM** integration
- 🚀 **`--generate-agent` flag** – additionally produces a LangGraph
  React agent (with A2A server, Makefile, README and .env.example)
  alongside the generated MCP server.

---

## 📦 Requirements

- 🐍 Python **3.13+**
- ⚡ [uv](https://docs.astral.sh/uv/getting-started/installation/)

---

## ⚡ Quick Start with `uv` (Recommended)

**Note:** Install uv first: https://docs.astral.sh/uv/getting-started/installation/

```
uv sync
```

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir examples/petstore/mcp_server \
  --generate-agent
```

### 📌 Optional: Pin a release tag

```bash
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git@v0.1.0 openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir examples/petstore/mcp_server \
  --generate-agent
```

### 🤖 Optional: Enhance Docstrings via LLM

Use the `--enhance-docstring-with-llm` flag if you want to improve generated docstrings with an LLM. This option leverages your LLM provider's configuration via environment variables.
To set up your LLM provider, refer to [this guide](https://cnoe-io.github.io/ai-platform-engineering/getting-started/docker-compose/configure-llms).

```bash
pipx run --spec git+https://github.com/cnoe-io/openapi-mcp-codegen.git@main openapi_mcp_codegen \
  --spec-file examples/petstore/openapi_petstore.json \
  --output-dir examples/petstore/mcp_server \
  --generate-agent \
  --enhance-docstring-with-llm  # Optional: enhances docstrings using LLM (see guide)
```

---

## 🧑‍💻 Local Development

Prefer to run locally or contribute?

**Note:** Install uv first: https://docs.astral.sh/uv/getting-started/installation/

### 1. **Clone the repo:**

```bash
git clone https://github.com/cnoe-io/openapi-mcp-codegen
cd openapi-mcp-codegen
```

### 2. **Install dependencies with Poetry:**

```bash
uv sync
```

### 3. **Run the generator:**

- The generator will create code in a new directory called `mcp_<server-name>` in the directory you specify.
- Follow the setup instructions printed by the generator.

**Option 1:**

```bash
make generate -- --spec-file examples/petstore/openapi_petstore.json --output-dir examples/petstore/mcp_server
```

**Option 2:**

```bash
uv run openapi_mcp_codegen --spec-file examples/petstore/openapi_petstore.json --output-dir examples/petstore/mcp_server
```

---

## 🗂️ Generated MCP Server Structure

```text
mcp_petstore/
├── mcp_petstore/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── client.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── [models].py
│   ├── server.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── [tools].py
│   └── utils/
│       └── __init__.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

### 🛠 Working with the generated agent

When you run the generator with `--generate-agent`, the output directory
also contains:

* `agent.py` – LangGraph wrapper
* `protocol_bindings/a2a_server/` – runnable A2A server
* `Makefile`, `README.md`, `.env.example`

Example:

```bash
cd examples/petstore/mcp_server
cp .env.example .env         # add {{ MCP_NAME | upper }}_API_URL & TOKEN
make run-a2a                 # start the A2A server

# In another terminal:
make run-a2a-client          # docker chat client
```

---

## 🛠️ Customization

- ✏️ Modify generated tool modules in `tools/`
- 🧩 Add custom models in `models/`
- 🔌 Extend the API client in `api/client.py`
- 🛠️ Add utility functions in `utils/`

---

## 👥 Maintainers

See [MAINTAINERS.md](MAINTAINERS.md)

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

[Apache 2.0](LICENSE)

---

## 🔒 Security

If you discover a security vulnerability, please see our [SECURITY.md](SECURITY.md) for responsible disclosure guidelines.

---

## 🧑‍💼 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

---

## 🙏 Acknowledgements

- [MCP on PyPI](https://pypi.org/project/mcp/), the official [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) Python package
- Uses [uv](https://github.com/astral-sh/uv)
