# Argo Workflows Setup Guide

This guide helps you set up Argo Workflows for testing with the generated MCP server.

## Prerequisites

- Kubernetes cluster (local or remote)
- kubectl configured to access your cluster

## Install Argo Workflows

```bash
export ARGO_WORKFLOWS_VERSION="v3.7.3"

# Create namespace
kubectl create namespace argo

# Install Argo Workflows
kubectl apply -n argo -f "https://github.com/argoproj/argo-workflows/releases/download/${ARGO_WORKFLOWS_VERSION}/quick-start-minimal.yaml"
```

## Install Argo CLI

```bash
# Detect OS
ARGO_OS="darwin"
if [[ "$(uname -s)" != "Darwin" ]]; then
  ARGO_OS="linux"
fi

# Download the binary
curl -sLO "https://github.com/argoproj/argo-workflows/releases/download/v3.7.3/argo-$ARGO_OS-amd64.gz"

# Unzip
gunzip "argo-$ARGO_OS-amd64.gz"

# Make binary executable
chmod +x "argo-$ARGO_OS-amd64"

# Move binary to path
mv "./argo-$ARGO_OS-amd64" /usr/local/bin/argo

# Test installation
argo version
```

## Access Argo UI

```bash
# Port forward to access UI
kubectl -n argo port-forward svc/argo-server 2746:2746
```

The Argo UI will be available at: http://localhost:2746

## Testing with Generated MCP Server

Once you have Argo Workflows running:

1. Generate the MCP server (see [Presentation Overview](./index.md))
2. Configure the MCP server to point to your Argo instance
3. Use the AI agent to interact with Argo workflows

## Configuration

Update your environment variables to point to your Argo instance:

```bash
# For local Argo Workflows
export ARGO_API_URL=http://localhost:2746

# For production setup, use your Argo server URL
export ARGO_API_URL=https://argo.yourdomain.com

# Set authentication if required
export ARGO_TOKEN=your-token-here
```
