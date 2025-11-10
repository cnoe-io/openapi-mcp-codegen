# Copyright 2025 Cisco
# SPDX-License-Identifier: Apache-2.0

# =====================================================
# CRITICAL: Disable a2a tracing BEFORE any a2a imports
# =====================================================
from cnoe_agent_utils.tracing import disable_a2a_tracing

# Disable A2A framework tracing to prevent interference with custom tracing
disable_a2a_tracing()

# =====================================================
# Now safe to import a2a modules
# =====================================================

import click
import httpx
import uvicorn
import asyncio
import os
from dotenv import load_dotenv
from agntcy_app_sdk.factory import AgntcyFactory

from agent_argo_workflows.protocol_bindings.a2a_server.agent_executor import ArgoWorkflowsAgentExecutor # type: ignore[import-untyped]
from agent_argo_workflows.agentcard import create_agent_card
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import (
    BasePushNotificationSender,
    InMemoryPushNotificationConfigStore,
    InMemoryTaskStore,
)

from starlette.middleware.cors import CORSMiddleware

load_dotenv()

# Only support p2p transport for simplicity

# We can't use click decorators for async functions so we wrap the main function in a sync function
@click.command()
@click.option('--host', 'host', default='localhost')
@click.option('--port', 'port', default=3001)
def main(host: str, port: int):
    asyncio.run(async_main(host, port))

async def async_main(host: str, port: int):
    client = httpx.AsyncClient()
    push_config_store = InMemoryPushNotificationConfigStore()
    push_sender = BasePushNotificationSender(httpx_client=client,
                    config_store=push_config_store)
    request_handler = DefaultRequestHandler(
      agent_executor=ArgoWorkflowsAgentExecutor(),
      task_store=InMemoryTaskStore(),
      push_config_store=push_config_store,
      push_sender= push_sender
    )

    agent_url = f'http://{host}:{port}'

    server = A2AStarletteApplication(
        agent_card=create_agent_card(agent_url), http_handler=request_handler
    )

    # Run a p2p A2A server
    print("Running A2A server in p2p mode.")
    app = server.build()

    # Add CORSMiddleware to allow requests from any origin (disables CORS restrictions)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],  # Allow all headers
    )

    # Disable uvicorn access logs to reduce noise from health checks
    config = uvicorn.Config(app, host=host, port=port, access_log=False)
    server = uvicorn.Server(config=config)
    await server.serve()

if __name__ == '__main__':
    main()
