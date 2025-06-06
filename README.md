# 🚀 OpenAPI to MCP Server Code Generator

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/poetry-1.0%2B-blueviolet?logo=python)](https://python-poetry.org/)
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

---

## 📦 Requirements

- 🐍 Python **3.8+**
- ⚡ [`uv`](https://github.com/astral-sh/uv) and [`uvx`](https://github.com/astral-sh/uvx) (recommended)
- 🧪 Optional: [Poetry](https://python-poetry.org/) for local development

---

## ⚡ Quick Start with `uvx` (Recommended)

No install required — just run the generator directly from GitHub:

```bash
uvx https://github.com/cnoe-io/openapi-mcp-codegen.git -- generate \
  --spec-file examples/openapi_petstore.json \
  --output-dir examples/mcp_petstore \
  --enhance-docstring-with-llm-openapi
```

### 📌 Optional: Pin a release tag

```bash
uvx https://github.com/cnoe-io/openapi-mcp-codegen.git@v0.2.0 -- generate \
  --spec-file examples/openapi_petstore.json \
  --output-dir examples/mcp_petstore
```

---

## 🧑‍💻 Local Development

Prefer to run locally or contribute?

### 1. **Clone the repo:**

```bash
git clone https://github.com/cnoe-io/openapi-mcp-codegen
cd openapi-mcp-codegen
```

### 2. **Install dependencies with Poetry:**

```bash
poetry install
```

### 3. **Run the generator:**

- The generator will create code in a new directory called `mcp_<server-name>` or the directory you specify.
- Follow the setup instructions printed by the generator.

**Option 1:**

```bash
make generate -- --spec-file examples/openapi_petstore.json --output-dir examples/mcp_petstore
```

**Option 2:**

```bash
poetry run generate --spec-file examples/openapi_petstore.json --output-dir examples/mcp_petstore
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
- Thanks to the MCP community for their support
- Built with [Poetry](https://python-poetry.org/), [uv](https://github.com/astral-sh/uv), and open source love 💜
