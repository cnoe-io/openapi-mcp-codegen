# OpenAPI MCP Codegen Documentation Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
npm install
```

## Local Development with auto-reload

> **Note:** This site will auto-reload on new changes

```bash
npm run start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build Static Site

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Serve Static Site

```bash
npm run serve
```

## Deployment with Github Actions

[![Publish Docs](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/publish-gh-pages.yml/badge.svg)](https://github.com/cnoe-io/openapi-mcp-codegen/actions/workflows/publish-gh-pages.yml)

## Documentation Structure

This documentation covers:

- **Getting Started**: Installation, basic usage, and configuration
- **Architecture**: Technical overview and design decisions
- **Enhancement Pipeline**: LLM integration and OpenAPI overlays
- **Examples**: Working examples with different APIs
- **CLI Reference**: Command-line tools and configuration
- **Integration**: AI agents, AgentGateway, and observability
- **ADRs**: Architecture Decision Records documenting key design choices

## Contributing to Documentation

Documentation improvements are welcome! See the [Contributing Guide](../docs/contributing.md) for details on how to contribute.