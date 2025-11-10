FROM python:3.13-slim

ARG DEBIAN_FRONTEND=noninteractive

# Base OS deps (git for editable installs)
RUN apt-get update && apt-get install -y --no-install-recommends \
git \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pre-install Python dependencies for better layer caching
COPY pyproject.toml /app/pyproject.toml
COPY README.md /app/README.md
RUN python -m pip install --upgrade pip && python -m pip install -e .

# Now copy the application source
COPY . /app

ENV PYTHONUNBUFFERED=1

# Default command: run the A2A server on 0.0.0.0:8000
CMD ["python", "-m", "protocol_bindings.a2a_server", "--host", "0.0.0.0", "--port", "8000"]