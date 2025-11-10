# Revolutionizing Argo Integration With Model Context Protocol: An AI-Driven Approach

**ArgoCon 2025 Presentation**

## Conference Details

- **Event**: [CNCF-hosted Co-located Events North America 2025](https://colocatedeventsna2025.sched.com/event/28D4z/revolutionizing-argo-integration-with-model-context-protocol-an-ai-driven-approach-carlos-santana-aws-sri-aradhyula-cisco)
- **Date**: Monday November 10, 2025
- **Time**: 2:40pm - 3:05pm EST
- **Location**: Building B | Level 3 | B312-313a
- **Track**: ArgoCon, Software Delivery
- **Content Level**: Advanced
- **Duration**: 25 minutes (10 min slides + 15 min demo)

## Speakers

### Carlos Santana - AWS
Senior Specialist Solutions Architect at AWS leading Container solutions in the Worldwide Application Modernization (AppMod). Experienced in distributed cloud application architecture, emerging technologies, open source, serverless, devops, kubernetes, gitops. CNCF Ambassador.

### Sri Aradhyula - Cisco
AI Agentic Platform Engineering Architect at Outshift by Cisco with over 17 years of experience building scalable, secure cloud infrastructure across domains like GenAI, cybersecurity, and bootstrapping new platforms from scratch. Pioneer in Agentic AI.

## Abstract

This presentation introduces an innovative approach to developing Model Context Protocol (MCP) servers for the Argo project suite within the CNOE Platform Engineering AI Assistant framework. We demonstrate an automated, AI-powered solution that generates MCP servers for Argo CD, Workflows, and Rollouts.

Beyond simple OpenAPI conversion, our method leverages Large Language Models (LLMs) to enhance API context and descriptions. The solution features automated maintenance through GitHub Actions, enabling Argo maintainers to effortlessly keep their APIs updated. This low-touch approach represents a significant advancement in AI agent plugin frameworks, specifically tailored for CNCF tool integration.

At CISCO we are using this process to generate MCP servers for Argo for our internal developer platform Assistant Jarvis.

## Key Topics Covered

- **Automated MCP Server Generation**: From OpenAPI specs to production-ready AI agent tools
- **LLM Enhancement Pipeline**: AI-powered API documentation optimization
- **Smart Parameter Handling**: 98.6% code reduction for complex Kubernetes schemas
- **Zero-Touch Maintenance**: GitHub Actions automation for API updates
- **Production Usage**: Real-world implementation at Cisco's Jarvis platform
- **Standards-Based Approach**: OpenAPI Overlay Specification 1.0.0 compliance

## Demonstration

### Live Demo Components (15 minutes)
1. **Code Generation** (3 min) - Generate MCP server from Argo Workflows OpenAPI spec
2. **AI Agent Interaction** (5 min) - Natural language workflow management
3. **Evaluation Suite** (3 min) - LangFuse tracing and accuracy metrics
4. **GitHub Actions** (2 min) - Automated maintenance workflow
5. **Q&A** (2 min) - Community engagement

### Performance Metrics Showcased
- **255 API operations** automatically converted to AI-ready tools
- **98.6% code size reduction** for complex operations
- **99.3% parameter count reduction** while maintaining functionality
- **35% improvement** in AI tool selection accuracy
- **Production deployment** at enterprise scale

## Related Materials

- **Detailed Presentation**: [ADR-003: Community Presentation Strategy](./ADR-003-argocon-presentation.md)
- **Architecture Deep Dive**: [ADR-001: Architecture Overview](../adr/ADR-001-openapi-mcp-architecture.md)
- **Technical Implementation**: [ADR-004: Overlay Enhancement Strategy](../adr/ADR-004-openapi-overlay-enhancement.md)
- **Working Example**: [Argo Workflows Example](../../examples/argo-workflows/README.md)
- **GitHub Repository**: https://github.com/cnoe-io/openapi-mcp-codegen

## Getting Started

Try the technology yourself:

```bash
# Generate MCP server from Argo Workflows API
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file examples/argo-workflows/argo-openapi.json \
  --output-dir examples/argo-workflows/mcp_server \
  --generate-agent \
  --generate-eval
```

## Community Impact

This work advances:
- **AI-Platform Engineering Integration**: Making CNCF tools AI-agent ready
- **Standards Adoption**: Promoting OpenAPI Overlay and MCP protocol usage
- **Developer Productivity**: Reducing AI agent development time from weeks to minutes
- **Open Source Innovation**: Community-driven AI tooling for platform engineering

---

*This presentation is part of the broader CAIPE (Community AI Platform Engineering) initiative to bring AI assistance to platform engineering workflows.*
