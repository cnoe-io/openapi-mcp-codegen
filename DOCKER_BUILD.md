# 🐳 Docker Build Guide for Argo Agents

This guide explains how to build and deploy Docker containers for the Argo services (ArgoCD, Argo Workflows, and Argo Rollouts) using the automated build system.

## 🏗️ Build System Overview

The build system creates **multi-architecture** (linux/amd64, linux/arm64) containers for each Argo service in two variants:

- **MCP Variant** (`-mcp`): HTTP/SSE MCP (Model Context Protocol) server
- **A2A Variant** (`-a2a`): Agent-to-Agent protocol server with LLM integration

## 📦 Generated Images

| Service | MCP Image | A2A Image |
|---------|-----------|-----------|
| **ArgoCD** | `ghcr.io/cnoe-io/agent-argocd-mcp` | `ghcr.io/cnoe-io/agent-argocd-a2a` |
| **Argo Workflows** | `ghcr.io/cnoe-io/agent-argo-workflows-mcp` | `ghcr.io/cnoe-io/agent-argo-workflows-a2a` |
| **Argo Rollouts** | `ghcr.io/cnoe-io/agent-argo-rollouts-mcp` | `ghcr.io/cnoe-io/agent-argo-rollouts-a2a` |

## 🚀 Quick Start

### Prerequisites

Before building, ensure you have generated the code for the services:

```bash
# Generate all services
make generate-argocd-agent
make generate-argo-workflows-agent
make generate-argo-rollouts-agent

# Or use the individual targets as needed
```

### Build All Services Locally

```bash
# Build all Argo agent containers locally (multi-arch)
make build-agents-local

# Or using the script directly
./build-agents.sh
```

### Build and Push to Registry

```bash
# Build and push all containers to ghcr.io/cnoe-io
make build-agents-push

# Or using the script directly
./build-agents.sh --push
```

## 🎯 Individual Service Builds

Build specific services for testing or development:

```bash
# Build only ArgoCD containers
make build-agent-argocd

# Build only Argo Workflows containers
make build-agent-argo-workflows

# Build only Argo Rollouts containers
make build-agent-argo-rollouts
```

### Using the Script Directly

```bash
# Build specific service
./build-agents.sh argocd
./build-agents.sh argo-workflows
./build-agents.sh argo-rollouts

# Build and push specific service
./build-agents.sh --push argocd
```

## 🏷️ Image Tagging Strategy

Images are tagged with multiple tags for different use cases:

- **Timestamped**: `autogen-YYYYMMDD-HHMMSS` (e.g., `autogen-20241110-143022`)
- **Latest**: `latest` (for main branch builds)
- **Branch**: `branch-name` (for feature branches)
- **SHA**: `branch-sha` (for commit-specific builds)

Example:
```bash
ghcr.io/cnoe-io/agent-argocd-mcp:autogen-20241110-143022
ghcr.io/cnoe-io/agent-argocd-mcp:latest
ghcr.io/cnoe-io/agent-argocd-a2a:autogen-20241110-143022
ghcr.io/cnoe-io/agent-argocd-a2a:latest
```

## 🔧 Make Targets Reference

| Target | Description |
|--------|-------------|
| `build-agents-check` | Check Docker prerequisites (buildx, multi-arch support) |
| `build-agents-local` | Build all Argo agent containers locally |
| `build-agents-push` | Build and push all containers to registry |
| `build-agent-argocd` | Build only ArgoCD containers |
| `build-agent-argo-workflows` | Build only Argo Workflows containers |
| `build-agent-argo-rollouts` | Build only Argo Rollouts containers |

## 🚢 Running the Containers

### MCP Server (HTTP/SSE)

```bash
# ArgoCD MCP Server
docker run -p 8000:8000 \
  -e ARGOCD_SERVER=https://argocd.example.com \
  -e ARGOCD_TOKEN=your-token \
  ghcr.io/cnoe-io/agent-argocd-mcp:latest

# Argo Workflows MCP Server
docker run -p 8000:8000 \
  -e ARGO_SERVER=https://argo-workflows.example.com:2746 \
  -e ARGO_TOKEN=your-token \
  ghcr.io/cnoe-io/agent-argo-workflows-mcp:latest

# Argo Rollouts MCP Server
docker run -p 8000:8000 \
  -e ARGO_ROLLOUTS_SERVER=https://argo-rollouts.example.com \
  -e ARGO_ROLLOUTS_TOKEN=your-token \
  ghcr.io/cnoe-io/agent-argo-rollouts-mcp:latest
```

### A2A Agent Server (with LLM)

```bash
# ArgoCD A2A Agent
docker run -p 8000:8000 \
  -e ARGOCD_SERVER=https://argocd.example.com \
  -e ARGOCD_TOKEN=your-token \
  -e OPENAI_API_KEY=your-openai-key \
  ghcr.io/cnoe-io/agent-argocd-a2a:latest

# Argo Workflows A2A Agent
docker run -p 8000:8000 \
  -e ARGO_SERVER=https://argo-workflows.example.com:2746 \
  -e ARGO_TOKEN=your-token \
  -e ANTHROPIC_API_KEY=your-anthropic-key \
  ghcr.io/cnoe-io/agent-argo-workflows-a2a:latest
```

## 🤖 GitHub Actions CI/CD

The repository includes a GitHub Actions workflow (`.github/workflows/build-argo-agents.yml`) that:

- **Triggers on**: Push to main/develop, PRs, manual dispatch
- **Matrix Build**: All services × both variants (6 total images)
- **Multi-arch**: Builds for linux/amd64 and linux/arm64
- **Security**: Includes Trivy vulnerability scanning
- **Registry**: Pushes to `ghcr.io/cnoe-io` organization

### Manual Workflow Dispatch

You can trigger builds manually from the GitHub Actions tab:

1. Go to **Actions** → **Build and Push Argo Agent Containers**
2. Click **Run workflow**
3. Choose whether to push images to registry

## 🔍 Build Script Features

The `build-agents.sh` script provides:

- ✅ **Multi-architecture builds** (linux/amd64, linux/arm64)
- ✅ **Automatic prerequisite checking** (Docker, buildx)
- ✅ **Colored output** with progress indicators
- ✅ **Error handling** with detailed failure reporting
- ✅ **Build caching** for faster subsequent builds
- ✅ **Flexible service selection** (all or individual)
- ✅ **Push mode** for registry deployment

## 📋 Troubleshooting

### Common Issues

**Missing generated code:**
```bash
❌ Generated code not found for argo-workflows. Run 'make generate-argo-workflows-agent' first.
```
**Solution**: Generate the code first using the appropriate make target.

**Docker buildx not available:**
```bash
❌ Docker buildx is required but not available.
```
**Solution**: Update Docker to a version that includes buildx, or install it separately.

**Permission denied on script:**
```bash
./build-agents.sh: Permission denied
```
**Solution**: Make the script executable: `chmod +x build-agents.sh`

### Debug Mode

For verbose output, modify the script's first line:
```bash
#!/bin/bash -x  # Enable debug mode
```

## 🔐 Security Considerations

- Images run as non-root user (`appuser`, UID 1001)
- Multi-stage builds minimize attack surface
- Regular vulnerability scanning with Trivy
- No secrets embedded in images (use environment variables)
- Read-only root filesystem compatible

## 📈 Performance Optimization

- **Build caching**: Uses GitHub Actions cache and Docker layer caching
- **Multi-stage builds**: Separates build and runtime dependencies
- **Parallel builds**: Matrix builds run concurrently
- **Minimal base images**: Uses `python:3.13-slim` for smaller sizes

## 🤝 Contributing

When adding new services:

1. Add the service to the `SERVICES` array in `build-agents.sh`
2. Create individual build targets in the `Makefile`
3. Update the GitHub Actions matrix in the workflow file
4. Update this documentation

For questions or issues, please open a GitHub issue or contact the maintainers.
