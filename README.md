# MCP Generator Tool

- This tool automatically generates a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server from an OpenAPI specification.

- It follows the same structure as the PagerDuty MCP server, making it easy to create new MCP servers for any API that has an OpenAPI specification.

## Features

- Automatically generates a complete MCP server structure
- Supports both JSON and YAML OpenAPI specifications
- Automatically detects file type (.json, .yaml, or .yml)
- Creates tool modules for each API endpoint
- Generates API client code
- Sets up proper logging and error handling
- Creates configuration files (pyproject.toml, .env.example)
- Generates comprehensive documentation

## Requirements

- Python 3.8 or higher
- Poetry for dependency management

## Installation

1. Clone this repository:

```bash
git clone https://github.com/cnoe-io/openapi-mcp-codegen
cd agent-utils
```

2. Install dependencies:
```bash
poetry install
```

## Usage

1. Place your OpenAPI specification file (JSON or YAML) in the project directory

2. Use the `make generate` target

```bash
make generate -- --spec-file examples/openapi_petstore.json --output-dir examples/mcp_petstore
```

    - The generator will code either in new directory called `mcp_<server-name>` or the directory your specified
    - Follow the setup instructions printed by the generator

## Generated MCP Server Structure

The generated MCP server follows this structure:

```
generated_mcp/
├── api/
│   ├── __init__.py
│   └── client.py
├── models/
│   └── __init__.py
├── tools/
│   ├── __init__.py
│   └── [endpoint].py
├── utils/
│   └── __init__.py
├── .env.example
├── __init__.py
├── pyproject.toml
├── README.md
└── server.py
```

## Customization

The generated MCP server can be customized by:

1. Modifying the generated tool modules in the `tools/` directory
2. Adding custom models in the `models/` directory
3. Extending the API client in `api/client.py`
4. Adding utility functions in the `utils/` directory

## Maintainers

[MAINTAINERS.md](MAINTAINERS.md)

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md)

## License

[Apache 2.0](LICENSE)
