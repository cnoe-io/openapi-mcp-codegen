# 🧠 {{ mcp_name | capitalize }} MCP Server

This module implements the **MCP protocol bindings** for the `{{ mcp_name | capitalize }}` agent.

It auto-generates MCP compliant tools or data models and server code.

The server acts as a wrapper over the agent's async call loop and translates standard input/output formats.

---

## 📄 Overview

- **Description**: {{ mcp_description }}
- **Version**: {{ mcp_version }}
- **Author**: {{ mcp_author }}

---

## 📁 Module Structure

```
mcp_server/
├── mcp_argocd
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── client.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── api_foo.py
│   └── utils/
│       └── __init__.py
├── pyproject.toml
└── README.md
```

---

## 🚀 Running the MCP Server
{% if a2a_proxy %}
Note: Generated with --with-a2a-proxy. The agent includes a WebSocket upstream server intended to run behind an external “a2a-proxy” that translates A2A requests (JSON-RPC/SSE) into upstream WebSocket frames. Deploy the proxy and configure it to connect to ws://localhost:8000, then direct A2A clients to the proxy’s /a2a/v1.
{% endif %}

Make sure dependencies are installed and environment variables are configured. Then run:

```bash
poetry run mcp_{{ mcp_name }}
```

Or directly with Python:

```bash
python -m {{ agent_pkg_name }}.protocol_bindings.mcp_server.main
```

---

## 🌐 API Endpoints

- `POST /v1/task` — Submit a task for execution
- `GET  /v1/task/{task_id}` — Query result of a submitted task
- `GET  /v1/spec` — Get OpenAPI spec for tool ingestion

You can test with:

```bash
curl -X POST http://localhost:8000/v1/task \
  -H "Content-Type: application/json" \
  -d '{
    "input": "status of ArgoCD app",
    "agent_id": "{{ agent_id }}",
    "tool_config": {}
  }'
```

---

## ⚙️ Environment Variables

| Variable             | Description                              |
|----------------------|------------------------------------------|
| `{{ agent_env_prefix }}_ID`   | Agent identifier used in API requests |
| `{{ agent_env_prefix }}_PORT` | Port to run the MCP server (default: 8000) |

---

## 🧰 Available Tools

The following tools are exposed by this agent via the MCP protocol. These are defined in the `tools/` directory and registered at runtime.

{% for tool in tools %}
---

### 🔧 `{{ tool.name }}`

- **Description**: {{ tool.description or "No description provided." }}
- **Tool Name**: `{{ tool.name }}`
- **Endpoint**: `POST /v1/task`

#### 📥 Input Schema

```json
{{ tool.input_schema | tojson(indent=2) }}
```

#### 📤 Output Schema

```json
{{ tool.output_schema | tojson(indent=2) }}
```

#### 🧪 Example Request

```bash
curl -X POST http://localhost:8000/v1/task \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "{{ agent_id }}",
    "tool_name": "{{ tool.name }}",
    "input": {{ tool.sample_input | tojson(indent=2) }}
  }'
```
{% endfor %}

---

## 🧪 Testing

To test locally:

```bash
make run-mcp
```

Or with the included MCP client:

```bash
python client/mcp_client.py
```

---

## 📚 References

- [OpenAPI MCP Codegen](https://github.com/cnoe-io/openapi-mcp-codegen)
