version: "3.9"
services:
  {{ mcp_name }}-a2a:
    image: agent_{{ mcp_name }}:latest
    working_dir: /app
    volumes:
      - ./:/app
    command: ["python", "-m", "protocol_bindings.a2a_server", "--host", "0.0.0.0", "--port", "${A2A_PORT:-8000}"]
    environment:
      - {{ mcp_name | upper }}_API_URL=${{ mcp_name | upper }}_API_URL
      - {{ mcp_name | upper }}_TOKEN=${{ mcp_name | upper }}_TOKEN
      - LANGFUSE_PUBLIC_KEY=${LANGFUSE_PUBLIC_KEY}
      - LANGFUSE_SECRET_KEY=${LANGFUSE_SECRET_KEY}
      - LANGFUSE_HOST=http://host.docker.internal:3000
      - PYTHONUNBUFFERED=1
      - LANGFUSE_TRACING_ENABLED=${LANGFUSE_TRACING_ENABLED}
    ports:
      - "${A2A_PORT:-8000}:${A2A_PORT:-8000}"
  {{ mcp_name }}-slim:
    image: agent_{{ mcp_name }}:latest
    working_dir: /app
    volumes:
      - ./:/app
    command: ["python", "-m", "protocol_bindings.a2a_server", "--host", "0.0.0.0", "--port", "${SLIM_A2A_PORT:-8001}", "--enable-slim"]
    environment:
      - {{ mcp_name | upper }}_API_URL=${{ mcp_name | upper }}_API_URL
      - {{ mcp_name | upper }}_TOKEN=${{ mcp_name | upper }}_TOKEN
      - SLIM_ENDPOINT=http://slim-dataplane:46357
      - LANGFUSE_PUBLIC_KEY=${LANGFUSE_PUBLIC_KEY}
      - LANGFUSE_SECRET_KEY=${LANGFUSE_SECRET_KEY}
      - LANGFUSE_HOST=http://host.docker.internal:3000
      - LANGFUSE_TRACING_ENABLED=${LANGFUSE_TRACING_ENABLED}

    depends_on:
      - slim-dataplane

    ports:
      - "${SLIM_A2A_PORT:-8001}:${SLIM_A2A_PORT:-8001}"

  slim-dataplane:
    image: ghcr.io/agntcy/slim:latest
    volumes:
      - ./slim-config.yaml:/config.yaml:ro
    command: ["/slim", "--config", "/config.yaml"]
    ports:
      - "46357:46357"
