FROM python:3.13-slim

ARG DEBIAN_FRONTEND=noninteractive

# Base OS deps (git for editable installs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
  && rm -rf /var/lib/apt/lists/*

{% if enable_slim %}
# Optional: install Node + npm to provide npx (used by optional utility MCPs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm \
  && rm -rf /var/lib/apt/lists/*
{% endif %}

WORKDIR /app
COPY . /app

ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip && \
    python -m pip install -e .

# No default CMD; docker-compose supplies the command
