# MCP Generator Tool

This tool automatically generates a Model Context Protocol (MCP) server from an OpenAPI specification. It follows the same structure as the PagerDuty MCP server, making it easy to create new MCP servers for any API that has an OpenAPI specification.

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
git clone <https://github.com/cnoe-io/agent-utils>
cd agent-utils
```

2. Install dependencies:
```bash
poetry install
```

## Usage

1. Place your OpenAPI specification file (JSON or YAML) in the project directory

2. Open `generate_mcp.py` and update line 24 to point to your specification file:
```python
spec_path = os.path.join(script_dir, 'your_openapi_spec.json')  # Replace with your filename (.json, .yaml, or .yml)
```

3. Run the generator:
```bash
poetry run python generate_mcp.py
```

4. The generator will create a new directory called `yourapi_mcp` containing your MCP server

5. Follow the setup instructions printed by the generator

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

This project is maintained by:
- Rehan Agrawal (rehagraw@cisco.com)

For any questions or issues, please contact the maintainers.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
