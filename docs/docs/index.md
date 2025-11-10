---
sidebar_position: 1
---

# Introduction

## What is OpenAPI MCP Codegen

> **⭐ GitHub repository**: [github.com/cnoe-io/openapi-mcp-codegen](https://github.com/cnoe-io/openapi-mcp-codegen)

> 💡 *Tip: **OpenAPI MCP Codegen** transforms traditional REST APIs into AI-friendly MCP (Model Context Protocol) servers. Just as a 🦸‍♂️ cape empowers a superhero, MCP servers empower AI agents with seamless API integration! 🚀*

As [Platform Engineering](https://platformengineering.org/blog/what-is-platform-engineering), [SRE](https://en.wikipedia.org/wiki/Site_reliability_engineering) and [DevOps](https://en.wikipedia.org/wiki/DevOps) teams increasingly adopt AI-powered workflows, integrating existing APIs with AI agents remains a significant challenge. Manual integration takes weeks per service, results in inconsistent quality, and creates maintenance overhead with every API update.


OpenAPI MCP Codegen is an open-source tool that automatically transforms OpenAPI specifications into production-ready MCP (Model Context Protocol) servers. It bridges the gap between traditional REST APIs and AI-powered integrations by using LLM-enhanced documentation and intelligent code generation, enabling AI agents to effectively discover, understand, and utilize APIs with minimal human intervention.

The tool generates specialized MCP servers that integrate seamlessly with AI agents and platform engineering tools. Below are some example integrations enabled by generated MCP servers:

* 🚀 **Argo Workflows** - AI-powered workflow management and monitoring
* 🔄 **Argo CD** - Intelligent continuous deployment operations
* 📊 **Argo Rollouts** - Smart progressive delivery management
* 🏗️ **Backstage** - Enhanced developer portal interactions
* ☸ **Kubernetes APIs** - Natural language cluster operations
* 📈 **Splunk** - AI-driven observability and analytics
* 🔧 **Custom APIs** - Any OpenAPI 3.0+ specification

*...and any REST API with an OpenAPI specification can be transformed into an AI-friendly MCP server.*

Together, these MCP servers enable AI agents to perform complex API operations using natural language workflows. The system also includes:

* **LLM-Enhanced Documentation**: AI-generated, contextual descriptions optimized for function calling with "Use when:" patterns and OpenAI-compatible formatting under 300 characters.
* **Smart Parameter Handling**: Intelligent consolidation of complex Kubernetes-style schemas, reducing 1000+ parameter functions to clean, usable interfaces with 98.6% code reduction.
* **Standards-Based Approach**: Uses OpenAPI Overlay Specification 1.0.0 for non-destructive, version-controlled API enhancements that work across toolchains.
* **Production-Ready Output**: Generates fully-typed Python MCP servers with async HTTP clients, comprehensive error handling, and auto-generated documentation.
* **Zero-Touch Maintenance**: GitHub Actions workflows automatically update MCP servers when APIs change, ensuring always up-to-date integrations.

## Goals of the project

- **Automated AI-API Integration**: Transform any OpenAPI specification into a production-ready MCP server that AI agents can effectively utilize, reducing integration time from weeks to minutes.

- **Standards-Driven Enhancement**: Use industry standards (OpenAPI Overlay 1.0.0, MCP Protocol) to create portable, maintainable, and reusable API enhancements that work across different AI platforms and toolchains.

- **Community-Powered Ecosystem**: Foster a collaborative community of platform engineers, API developers, and AI practitioners to continuously improve prompt libraries, enhance code generation templates, and expand API coverage across the CNCF landscape.

- **Production Excellence**: Ensure generated MCP servers meet enterprise requirements with comprehensive type safety, error handling, observability, and automated testing capabilities.

## Key Features

### 🤖 LLM Enhancement Pipeline
- **GPT-4/Claude Integration**: Analyzes OpenAPI operations and generates contextual, AI-friendly descriptions
- **Declarative Prompts**: Version-controlled prompt templates in `prompt.yaml` for consistent enhancement patterns
- **OpenAPI Overlay Output**: Standards-compliant enhancement specifications that can be reviewed, edited, and reused

### ⚙️ Intelligent Code Generation
- **Smart Parameter Handling**: Automatically detects complex schemas and uses dictionary mode to prevent unusable 1000+ parameter functions
- **Type-Safe Interfaces**: Full Python type hints with proper error handling and async/await patterns
- **Template System**: Jinja2-based generation with customizable templates for different output formats

### 🔧 Production Ready
- **AgentGateway Integration**: Auto-generated configuration for immediate deployment
- **Comprehensive Testing**: Automated validation, evaluation suites, and integration testing
- **Zero-Config Deployment**: From OpenAPI spec to running MCP server in minutes

### 📊 Real-World Impact
- **98.6% code size reduction** for complex API operations
- **99.3% parameter count reduction** while maintaining full functionality
- **35% improvement** in AI tool selection accuracy
- **Production usage** at Cisco's Jarvis platform and other enterprise environments

## Who we are

This project is maintained by the **CAIPE** (Community AI Platform Engineering) maintainers - a community of Platform Engineers, SREs, API developers, and AI practitioners from companies across the [CNCF](https://www.cncf.io/) and [CNOE.io](https://cnoe.io/) ecosystems. We're passionate about open source and advancing AI-powered platform engineering through standards-based API integration, automated code generation, and community-driven innovation.

As part of the broader CAIPE initiative, our mission is to make every API AI-agent ready, enabling the next generation of intelligent platform operations and developer experiences through automated MCP server generation and LLM-enhanced API documentation.