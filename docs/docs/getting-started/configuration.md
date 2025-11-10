# Configuration

## config.yaml Structure

The `config.yaml` file controls package metadata, authentication, and enhancement settings.

## Basic Configuration

```yaml
title: petstore
description: Petstore API MCP Server
author: Your Name
email: you@example.com
version: 0.1.0
license: Apache-2.0

headers:
  Authorization: Bearer {token}
  Accept: application/json
```

## Enhancement Configuration

```yaml
overlay_enhancements:
  enabled: true
  use_llm: true
  max_description_length: 300
```

## Environment Variables

```bash
# API Configuration
PETSTORE_API_URL=https://api.example.com
PETSTORE_TOKEN=your-token

# LLM Configuration
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai
```

For detailed configuration options, see [CLI Reference](../cli/configuration-files.md).
