---
sidebar_position: 1
---

# Introduction

## What is OpenAPI MCP Codegen

> **⭐ GitHub repository**: [github.com/cnoe-io/openapi-mcp-codegen](https://github.com/cnoe-io/openapi-mcp-codegen)

> 💡 *Tip: **OpenAPI MCP Codegen** transforms OpenAPI specifications into production-ready MCP servers and intelligent A2A agents. Just as a 🦸‍♂️ cape empowers a superhero, MCP servers empower AI agents with seamless API integration! 🚀*

As [Platform Engineering](https://platformengineering.org/blog/what-is-platform-engineering), [SRE](https://en.wikipedia.org/wiki/Site_reliability_engineering) and [DevOps](https://en.wikipedia.org/wiki/DevOps) teams increasingly adopt AI-powered workflows, integrating existing APIs with AI agents remains a significant challenge. Manual integration takes weeks per service, results in inconsistent quality, and creates maintenance overhead with every API update.

OpenAPI MCP Codegen is an open-source tool that provides **two primary capabilities**:

1. **MCP Server Generation**: Transform OpenAPI specifications into production-ready MCP (Model Context Protocol) servers
2. **A2A Agent Generation**: Create standalone Agent-to-Agent (A2A) compatible agents that connect to external MCP servers

The tool bridges the gap between traditional REST APIs and AI-powered integrations through intelligent code generation and LLM-enhanced documentation, enabling AI agents to effectively discover, understand, and utilize APIs with minimal human intervention.

The tool generates specialized MCP servers that integrate seamlessly with AI agents and platform engineering tools. Below are some example integrations enabled by generated MCP servers:

* 🚀 **Argo Workflows** - AI-powered workflow management and monitoring
* 🔄 **Argo CD** - Intelligent continuous deployment operations
* 📊 **Argo Rollouts** - Smart progressive delivery management
* 🏗️ **Backstage** - Enhanced developer portal interactions
* ☸ **Kubernetes APIs** - Natural language cluster operations
* 📈 **Splunk** - AI-driven observability and analytics
* 🔧 **Custom APIs** - Any OpenAPI 3.0+ specification

*...and any REST API with an OpenAPI specification can be transformed into an AI-friendly MCP server.*

## Core Components

OpenAPI MCP Codegen is built around **three main components**:

### 1. MCP Server Generator (`mcp_codegen.py`)
Transforms OpenAPI specifications into production-ready MCP servers with:
* **Type-Safe Python Code**: Full async/await support with comprehensive type hints
* **Smart Parameter Handling**: Automatically detects complex schemas and uses dictionary mode for 1000+ parameter operations
* **Tool Module Generation**: Each API endpoint becomes a callable tool for AI agents
* **LLM-Enhanced Docstrings**: AI-optimized function documentation for better agent comprehension

### 2. A2A Agent Generator (`a2a_agent_codegen.py`)
Creates standalone agents that connect to external MCP servers with:
* **Complete Agent Package**: Full agent structure with protocol bindings and client integration
* **AgentGateway Compatible**: Works seamlessly with external MCP servers and AgentGateway
* **Configurable System Prompts**: LLM-generated or custom system prompts for domain expertise
* **Skills-Based Architecture**: Structured capability definitions from config or OpenAPI operations

### 3. CLI Interface (`__main__.py`)
Provides two primary commands:
* **`generate-mcp`**: Create MCP servers with optional agent wrappers, evaluation frameworks, and system prompt generation
* **`generate-a2a-agent-with-remote-mcp`**: Generate standalone A2A agents for external MCP servers

The system also includes:
* **LLM-Enhanced Generation**: AI-generated system prompts and enhanced docstrings optimized for agent comprehension
* **Smart Parameter Handling**: Intelligent consolidation of complex schemas, reducing 1000+ parameter functions to clean, usable interfaces
* **Production-Ready Output**: Generates fully-typed Python code with async HTTP clients, comprehensive error handling, and auto-generated documentation
* **Evaluation Framework**: Optional evaluation suites for testing agent performance and accuracy

## Goals of the project

- **Automated AI-API Integration**: Transform any OpenAPI specification into production-ready MCP servers and A2A agents that AI systems can effectively utilize, reducing integration time from weeks to minutes.

- **Dual Generation Approach**: Provide both self-contained MCP servers and standalone A2A agents that connect to external MCP servers, supporting different deployment architectures and use cases.

- **LLM-Enhanced Intelligence**: Generate AI-optimized system prompts, enhanced docstrings, and evaluation frameworks that improve agent performance and accuracy in real-world scenarios.

- **Production Excellence**: Ensure generated code meets enterprise requirements with comprehensive type safety, error handling, smart parameter management, and automated testing capabilities.

- **Community-Powered Ecosystem**: Foster a collaborative community of platform engineers, API developers, and AI practitioners to continuously improve generation templates and expand API coverage across the CNCF landscape.

## Key Features

### 🚀 MCP Server Generation
- **Complete MCP Servers**: Transform OpenAPI specs into fully functional MCP servers with typed Python code
- **Smart Parameter Handling**: Automatically detects complex schemas and uses dictionary mode for 1000+ parameter operations
- **Tool Module Architecture**: Each API endpoint becomes a callable tool with proper error handling and logging
- **Agent Wrapper Generation**: Optional LangGraph agent wrappers with A2A server bindings

### 🤝 A2A Agent Generation
- **Standalone Agents**: Create complete A2A-compatible agents that connect to external MCP servers
- **AgentGateway Ready**: Generated agents work seamlessly with AgentGateway and other MCP infrastructures
- **Skills-Based Configuration**: Structured capability definitions from config files or OpenAPI operations
- **Protocol Bindings**: Complete protocol binding layers for different transport mechanisms

### 🧠 LLM-Enhanced Intelligence
- **System Prompt Generation**: AI-generated system prompts optimized for specific API domains
- **Enhanced Docstrings**: LLM-optimized function documentation for better agent tool selection
- **Evaluation Frameworks**: Optional evaluation suites for testing agent performance and accuracy
- **Smart Documentation**: AI-friendly descriptions that improve tool discovery and usage

### ⚙️ Production Ready
- **Type-Safe Code**: Full Python type hints with proper error handling and async/await patterns
- **Template System**: Jinja2-based generation with customizable templates for different output formats
- **Zero-Config Deployment**: From OpenAPI spec to running MCP server or A2A agent in minutes

### 📊 Real-World Impact
- **98.6% code size reduction** for complex API operations
- **99.3% parameter count reduction** while maintaining full functionality
- **35% improvement** in AI tool selection accuracy
- **Production usage** at Cisco's Jarvis platform and other enterprise environments

## Who we are

This project is maintained by the **CAIPE** (Community AI Platform Engineering) maintainers - a community of Platform Engineers, SREs, API developers, and AI practitioners from companies across the [CNCF](https://www.cncf.io/) and [CNOE.io](https://cnoe.io/) ecosystems. We're passionate about open source and advancing AI-powered platform engineering through standards-based API integration, automated code generation, and community-driven innovation.

As part of the broader CAIPE initiative, our mission is to make every API AI-agent ready, enabling the next generation of intelligent platform operations and developer experiences through automated MCP server generation and LLM-enhanced API documentation.