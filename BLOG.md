# Building a Komodor Agent (with A2A, SLIM, LangGraph, MCP and Langfuse for Evaluation)

At Outshift by Cisco we use Komodor to simplify our cluster management at scale. Komodor provides an AI assistant, Klaudia, that specializes in root-cause analysis (RCA). This guide shows how to use the OpenAPI → MCP code generator to build an A2A-enabled LangGraph ReAct agent that calls Klaudia and Komodor APIs through MCP. Optionally, you can enable the SLIM transport from AGNTCY (https://agntcy.org/) for secure low-latency interactive messaging (see SLIM Core: https://docs.agntcy.org/messaging/slim-core/). The agent also ships an eval-mode used to collect a golden dataset to run evaluations with results & tracing uploaded to Langfuse.

## Overview

We will:

- Generate an MCP server from Komodor’s OpenAPI spec
- Generate a LangGraph React agent with A2A bindings
- Optionally enable SLIM transport via AGNTCY for low-latency messaging
- Optionally enable tracing/observability with Langfuse
- Build a golden dataset of expected requests/responses using **eval-mode**
- Run automated evaluation and upload results to Langfuse

## Prerequisites

- `uv` installed
- Komodor OpenAPI spec ([access here](https://api.komodor.com/api/docs/doc.json))
- LLM provider credentials (OpenAI, Azure OpenAI, etc.)
- [Docker](https://www.docker.com/get-started/) (for running the A2A client and SLIM agents)
- Optional: [Langfuse deployed locally](https://langfuse.com/self-hosting/docker-compose) or accessible remotely

## Quick Start

```bash
mkdir komodor_agent
cd komodor_agent
# Configure the Komodor client auth headers
echo "headers:\n  X-API-KEY: \"{token}\"" >> config.yaml
# Get the Komodor OpenAPI spec
curl -s https://api.komodor.com/api/docs/doc.json > komodor_api.yaml
# Generate the agent and eval code
uvx --from git+https://github.com/cnoe-io/openapi-mcp-codegen.git openapi_mcp_codegen \
  --spec-file komodor_api.yaml \
  --output-dir . \
  --generate-agent \
  --generate-eval \
  --enable-slim
```

## Architecture

The generated architecture looks like this for the Komodor agent:

```mermaid
flowchart TD
  %% Client side
  subgraph Client Layer
    A[A2A Client]
  end

  %% Transport/Messaging
  subgraph Messaging Layer
    S[SLIM Dataplane]
  end

  %% A2A Server
  subgraph Agent Transport Layer
    B[A2A Server]
  end

  %% Agent Framework
  subgraph Agent Framework Layer
    C[LangGraph ReAct Agent]
  end

  %% Tools/MCP and external API
  subgraph Tools/MCP Layer
    D[Komodor MCP Server]
    E[Komodor API (HTTPS)]
  end

  %% Edges
  A -- A2A over SLIM --> S
  S -- A2A over SLIM --> B
  B --> C
  C -. STDIO .-> D
  D -. HTTPS .-> E
  E -. HTTPS response .-> D
  D -. STDIO .-> C
```

## Running the agent

Placeholder for GIF: running the agent with SLIM enabled  
[GIF: Insert screen capture showing make run-a2a-and-slim and make run-slim-client]

### Setup environment variables

Follow [this guide](https://cnoe-io.github.io/ai-platform-engineering/getting-started/docker-compose/configure-llms/) to setting up your LLM provider environment variables, then with your Komodor ([optionally Langfuse](https://langfuse.com/faq/all/where-are-langfuse-api-keys)) API keys: You do not need any host.docker.internal configuration here since Komodor is an external service.

```bash
export KOMODOR_API_URL=https://api.komodor.com
export KOMODOR_TOKEN=<your-komodor-api-key>
# If you deployed Langfuse locally:
export LANGFUSE_HOST=http://localhost:3000
export LANGFUSE_PUBLIC_KEY=<your-langfuse-public-key>
export LANGFUSE_SECRET_KEY=<your-langfuse-secret-key>
```

### Run the agent and client

```bash
make run-a2a
```

Then in a separate terminal:

```bash
make run-a2a-client
```

Now you're able to interact with your agent! Ask a query like "What clusters do I have?"

## 1) Generate and Run an A2A-enabled Agent

- Run the generator (as shown in Quick Start). The command includes --enable-slim to generate SLIM transport support and a docker-compose file.
- Start any required mock or dev server for the Komodor API if applicable, or point to a real environment.
- Launch the generated A2A agent server.
- Use an A2A client (or A2A Inspector) to send queries like: “Run RCA on namespace X for service Y” or “Explain the incident timeline for deployment Z.”

Placeholder for GIF 1: generating and running the A2A-enabled agent
[GIF: Insert screen capture showing generation, starting the agent, and a client invoking Komodor via A2A]

Example steps (adjust for the generated paths/targets):

```bash
cd examples/komodor
# If a mock server is available, run it; otherwise skip
# uv run python komodor_mock_server.py

# Start the A2A server
make run-a2a

# In a separate terminal, run a client (or use A2A Inspector)
make run-a2a-client
```

You should now be able to issue RCA or troubleshooting queries. If Langfuse is configured, you’ll see traces for prompts, tool calls, and responses.

## 2) Run eval-mode to Build a Golden Dataset of Expected Requests

Eval-mode helps you curate a set of canonical prompts and expected tool trajectories/outputs for Komodor scenarios (e.g., RCA for specific namespaces, pods, or incident patterns).

Placeholder for GIF 2: running eval-mode to build the golden dataset  
[GIF: Insert screen capture showing interactive eval-mode, selecting tools, entering queries, and saving to eval/dataset.yaml]

Steps:

```bash
cd examples/komodor
make run-a2a-eval-mode
```

- The tool lists appear with descriptions  
- Enter queries that represent real user scenarios  
- Iterate to refine the strategy and expected behavior  
- The tool stores trajectories and outputs in eval/dataset.yaml  

## 3) Run Evaluation and Upload Results to Langfuse

Once the golden dataset is ready, run the automated evaluation. The evaluation includes:
- Correctness scoring (LLM-as-judge)
- Hallucination checks
- Trajectory accuracy (graph-level)

Placeholder for GIF 3: running evaluation and seeing results in Langfuse  
[GIF: Insert screen capture showing evaluation run, dataset created in Langfuse, and dashboards with metrics]

Run:

```bash
cd examples/komodor
make eval
```

This will:
- Create a new dataset in Langfuse  
- Execute each dataset case through the agent  
- Upload results and metrics to Langfuse for analysis  

## 4) Run the agent over SLIM and use the SLIM client

If you generated with --enable-slim, you can run the A2A server bridged to SLIM (AGNTCY). Because Komodor is an external API, you don’t need host.docker.internal in your environment. Ensure your Komodor configuration is set:

```bash
export KOMODOR_API_URL=https://api.komodor.com
export KOMODOR_TOKEN=<your-komodor-api-key>
```

Start the SLIM stack (A2A over HTTP + A2A bridged to SLIM + slim-dataplane via docker-compose):
```bash
make run-a2a-and-slim
```

In a separate terminal, connect using the SLIM client:
```bash
make run-slim-client
```

Placeholder for GIF: running the agent with SLIM enabled  
[GIF: Insert screen capture showing make run-a2a-and-slim and make run-slim-client]

## Tips and Conventions

- Operation IDs in the Komodor OpenAPI spec become Python function names (snake_case)
- Parameters map to typed function arguments in generated tools
- API client headers (e.g., Authorization) can be configured in a config.yaml and/or via environment variables
- Use --dry-run to preview generation
- Use --enhance-docstring-with-llm to improve tool docstrings
- If you enable --generate-system-prompt, the generator crafts a SYSTEM prompt tailored to the generated Komodor tools and endpoints
- Use --enable-slim to generate an A2A server bridged through AGNTCY SLIM; use make run-a2a-and-slim and make run-slim-client to run and connect over SLIM.

## Troubleshooting

- Ensure KOMODOR_API_URL and KOMODOR_API_TOKEN are set correctly
- Check logs for HTTP status codes and validation errors
- Verify A2A server is reachable (e.g., curl http://localhost:8000/.well-known/agent.json)
- If using Langfuse, verify keys/host and that LANGFUSE_TRACING_ENABLED=True
- For A2A Inspector, follow its setup and point it to your agent URL
- For SLIM transport, ensure docker-compose brings up slim-dataplane and the SLIM-bridged agent. No host.docker.internal is required for Komodor since it’s external.

## Next Steps

- Expand your golden dataset with more RCA scenarios, including noisy neighbor, resource exhaustion, failing readiness probes, and misconfigurations
- Integrate into CI to catch regressions in agent reasoning or tool usage
- Share Langfuse dashboards with your team to track quality over time
