# 🐾 Petstore MCP Server Usage with SSE

Welcome to the Petstore MCP Server guide! This document will help you set up and run the Petstore mock server, MCP server, and MCP Inspector. Follow the steps below to get started. 🚀

---

## ⚙️ Prerequisites

Before proceeding, ensure you have Python 3.13 or higher installed on your system. This is required due to upstream dependencies with MCP and other libraries.

To set up a virtual environment, you can use one of the following methods:

1. Use the `make` command:
  ```bash
  make setup-venv
  ```

1. Alternatively, using Python's `venv` module:
  ```bash
  python -m venv .venv
  ```

Activate the virtual environment before continuing:
```bash
source .venv/bin/activate
```

## 🛠️ Step 1: Start the Petstore Mock Server

Open **Terminal 1** and run the following command to start the Petstore mock server:

```bash
python examples/petstore/petstore_mock_server.py examples/petstore/openapi_petstore.json --port 10000
```

This will start the mock server on port `10000`.

## 📄 Swagger Documentation

You can access the Swagger specification for the Petstore API by visiting the following URL:

[Swagger Docs](http://127.0.0.1:10000/docs)

This provides an interactive interface to explore the API endpoints and their details.
---

## 🛠️ Step 2: Start the MCP Server

Open **Terminal 2** and follow these steps:

1. Populate sample data:

  Run the following command to populate sample data for the server:

  ```bash
  sh +x ./sample_data.sh
  ```
2. Install dependencies using Poetry:

  ```bash
  cd examples/petstore
  poetry install
  ```

3. Set the environment variables:

  ```bash
  export PETSTORE_API_URL=http://localhost:10000
  export PETSTORE_TOKEN=foo  # Note: PETSTORE_TOKEN is ignored in the mock server
  export MCP_MODE=sse # Other options stdio or http
  ```

4. Start the MCP server:

  You can use Poetry to run the server:
  ```bash
  poetry run python mcp_server/mcp_petstore/server.py
  ```

  Alternatively, just use python:
  ```bash
  python mcp_server/mcp_petstore/server.py
  ```

---

## 🛠️ Step 3: Start the MCP Inspector

Run the following command to start the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
```

```
Starting MCP inspector...
⚙️ Proxy server listening on 127.0.0.1:6277
🔑 Session token: REMOVED
Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth

🔗 Open inspector with token pre-filled:
   http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=<REMOVED>

```

Once the inspector is running, follow the link provided in the terminal to access the MCP Proxy with AUTH. Then:

1. Connect to the MCP server at:
  ```
  Transport Type: SSE
  URL: http://localhost:10000
  ```

2. Explore the available tools by clicking **List Tools** under tools.

---

🎉 You're all set! If you encounter any issues or have questions, feel free to reach out to the community or check the documentation for further assistance. Happy coding! 💻