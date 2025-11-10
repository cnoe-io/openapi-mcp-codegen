# Contributing

We welcome contributions to OpenAPI MCP Codegen! This guide will help you get started with contributing to the project.

## Getting Started

### Prerequisites

- Python 3.8+
- uv package manager
- Git

### Development Setup

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/your-username/openapi-mcp-codegen.git
   cd openapi-mcp-codegen
   ```

2. **Set up Development Environment**:
   ```bash
   uv venv && source .venv/bin/activate
   uv sync
   ```

3. **Verify Installation**:
   ```bash
   python -m openapi_mcp_codegen --help
   ```

## How to Contribute

### 1. Reporting Issues

Found a bug or have a feature request? Please check existing issues first, then:

- Use our [issue templates](https://github.com/cnoe-io/openapi-mcp-codegen/issues/new/choose)
- Provide clear reproduction steps for bugs
- Include relevant OpenAPI specs (sanitized if needed)
- Describe expected vs actual behavior

### 2. Code Contributions

#### Good First Issues

Look for issues labeled `good first issue`:
- Documentation improvements
- Example projects
- Test coverage enhancements
- Template improvements
- Bug fixes in code generation logic

#### Development Workflow

1. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**:
   ```bash
   # Edit code, add tests, update docs
   ```

3. **Test Your Changes**:
   ```bash
   # Run existing tests
   python -m pytest tests/

   # Test with example projects
   cd examples/petstore
   make generate-enhanced
   make validate
   ```

4. **Follow Code Standards**:
   ```bash
   # Format code with ruff
   ruff format .

   # Check linting
   ruff check .
   ```

5. **Commit with Conventional Commits**:
   ```bash
   git commit -m "feat: add support for GraphQL specifications"
   git commit -m "fix: handle missing parameter schemas correctly"
   git commit -m "docs: update installation instructions"
   ```

6. **Create Pull Request**:
   - Use our PR template
   - Link related issues
   - Describe changes and testing done
   - Request review from maintainers

## Development Guidelines

### Code Structure

- `openapi_mcp_codegen/`: Main package code
  - `mcp_codegen.py`: Core generation logic
  - `overlay_generator.py`: LLM enhancement pipeline
  - `overlay_applier.py`: OpenAPI overlay application
  - `templates/`: Jinja2 templates for code generation
- `examples/`: Working examples with different APIs
- `tests/`: Unit and integration tests
- `docs/`: Documentation source

### Coding Standards

- **Python Style**: Follow PEP 8, enforced by ruff
- **Type Hints**: Use type annotations for all public APIs
- **Docstrings**: Google-style docstrings for modules, classes, and functions
- **Error Handling**: Comprehensive error handling with informative messages
- **Logging**: Use Python logging module with appropriate levels

### Testing Guidelines

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test full generation workflows
- **Example Tests**: Ensure examples continue to work
- **Template Tests**: Verify template rendering

```bash
# Run specific test categories
python -m pytest tests/test_mcp_codegen.py
python -m pytest tests/test_openapi_validation.py
python -m pytest -k "test_template"
```

### Template Development

When modifying Jinja2 templates:

- Test with multiple OpenAPI specifications
- Ensure generated code is valid Python
- Include proper type hints and docstrings
- Handle edge cases (empty parameters, complex schemas)
- Format generated code with ruff

### LLM Enhancement Guidelines

When working on LLM integration:

- Support multiple providers (OpenAI, Anthropic)
- Implement graceful fallbacks for LLM unavailability
- Follow OpenAI function calling best practices
- Keep descriptions under recommended character limits
- Test with real API specifications

## Types of Contributions

### 1. Core Features

- **New Generator Features**: OpenAPI 3.1 support, GraphQL integration
- **Enhancement Pipeline**: Improved LLM prompts, new overlay patterns
- **Code Generation**: Better type mapping, optimization improvements
- **CLI Improvements**: New commands, better error messages

### 2. Templates and Examples

- **New API Examples**: Additional real-world API integrations
- **Template Improvements**: Better generated code patterns
- **Documentation**: Enhanced README templates, better docstrings
- **Configuration**: More flexible configuration options

### 3. Testing and Quality

- **Test Coverage**: Unit tests for uncovered code paths
- **Integration Tests**: End-to-end generation workflows
- **Performance**: Benchmarking and optimization
- **Validation**: Better OpenAPI specification validation

### 4. Documentation

- **User Guides**: Better getting started experiences
- **API Documentation**: Comprehensive API reference
- **Examples**: More detailed example walkthroughs
- **Architecture**: Design documentation and ADRs

## Community Guidelines

### Communication

- **GitHub Discussions**: General questions and feature discussions
- **Issues**: Bug reports and specific feature requests
- **Pull Requests**: Code changes and improvements
- **CNOE Slack**: Real-time community discussion

### Code of Conduct

We follow the [CNCF Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md). Please be respectful, inclusive, and collaborative.

### Review Process

1. **Automated Checks**: CI/CD runs tests, linting, and security scans
2. **Maintainer Review**: Core maintainers review for design and quality
3. **Community Feedback**: Other contributors may provide input
4. **Approval**: Requires approval from CAIPE maintainers
5. **Merge**: Squash and merge with conventional commit messages

## Recognition

Contributors are recognized through:

- **GitHub Contributors**: Listed on repository
- **Release Notes**: Major contributions highlighted
- **Community Calls**: Recognition in CNOE community meetings
- **Maintainer Track**: Path to becoming a project maintainer

## Development Resources

### Key Files for Understanding

- `openapi_mcp_codegen/mcp_codegen.py`: Core generation logic
- `openapi_mcp_codegen/templates/`: Template structure
- `examples/petstore/`: Complete working example
- `tests/test_mcp_codegen.py`: Integration test patterns

### Debugging Tips

- Use `--dry-run` flag to preview generation without writing files
- Enable debug logging: `export LOG_LEVEL=DEBUG`
- Test with simple OpenAPI specs first
- Use generated code logging for runtime debugging

### External Dependencies

- **MCP Protocol**: Uses `mcp>=1.9.0` for FastMCP server
- **Template Engine**: Jinja2 for code generation
- **HTTP Client**: httpx for generated API clients
- **Code Formatting**: ruff for Python code formatting

## Getting Help

- **Documentation**: Check existing docs first
- **Examples**: Review working examples in `examples/`
- **Issues**: Search existing issues for similar problems
- **Discussions**: Ask questions in GitHub Discussions
- **Community**: Join CNOE Slack for real-time help

## Release Process

Releases follow semantic versioning and automated processes:

1. **Development**: Features merged to `main` branch
2. **Testing**: Comprehensive testing on multiple platforms
3. **Release**: Automated release creation with conventional commits
4. **Distribution**: Published to PyPI and GitHub releases
5. **Documentation**: Updated examples and documentation

Thank you for contributing to OpenAPI MCP Codegen and helping make API-AI integration easier for everyone! 🚀
