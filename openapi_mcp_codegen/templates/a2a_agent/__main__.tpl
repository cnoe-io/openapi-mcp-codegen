{{ file_header }}

# =====================================================
# CRITICAL: Load environment variables FIRST
# =====================================================
from dotenv import load_dotenv
load_dotenv()

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

from agent_{{ agent_name }}.protocol_bindings.a2a_server.agent_executor import {{ agent_display_name.replace(' ', '') }}AgentExecutor # type: ignore[import-untyped]
from agent_{{ agent_name }}.agentcard import create_agent_card
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import (
    BasePushNotificationSender,
    InMemoryPushNotificationConfigStore,
    InMemoryTaskStore,
)

from starlette.middleware.cors import CORSMiddleware

load_dotenv()

A2A_TRANSPORT = os.getenv("A2A_TRANSPORT", "p2p").lower()
SLIM_ENDPOINT = os.getenv("SLIM_ENDPOINT", "http://slim-dataplane:46357")

# We can't use click decorators for async functions so we wrap the main function in a sync function
@click.command()
@click.option('--host', 'host', default=os.getenv('A2A_HOST', 'localhost'), help='Host to bind the A2A server (env: A2A_HOST)')
@click.option('--port', 'port', default=int(os.getenv('A2A_PORT', '10000')), help='Port to bind the A2A server (env: A2A_PORT)')
def main(host: str, port: int):
    asyncio.run(async_main(host, port))

async def async_main(host: str, port: int):
    client = httpx.AsyncClient()
    push_config_store = InMemoryPushNotificationConfigStore()
    push_sender = BasePushNotificationSender(httpx_client=client,
                    config_store=push_config_store)
    request_handler = DefaultRequestHandler(
        agent_executor={{ agent_display_name.replace(' ', '') }}AgentExecutor(),
        task_store=InMemoryTaskStore(),
      push_config_store=push_config_store,
      push_sender= push_sender
    )

    if A2A_TRANSPORT == "slim":
        agent_url = SLIM_ENDPOINT
    else:
        agent_url = f'http://{host}:{port}'

    server = A2AStarletteApplication(
        agent_card=create_agent_card(agent_url), http_handler=request_handler
    )

    if A2A_TRANSPORT == 'slim':
        # Run A2A server over SLIM transport
        # https://docs.agntcy.org/messaging/slim-core/
        print("Running A2A server in SLIM mode.")
        factory = AgntcyFactory()
        transport = factory.create_transport("SLIM", endpoint=agent_url)
        print("Transport created successfully.")

        bridge = factory.create_bridge(server, transport=transport)
        print("Bridge created successfully. Starting the bridge.")
        await bridge.start(blocking=True)
    else:
        # Run a p2p A2A server
        print("Running A2A server in p2p mode.")
        app = server.build()

        # Add CORS middleware to allow cross-origin requests (configurable via environment)
        cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
        cors_methods = os.getenv("CORS_METHODS", "*").split(",") if os.getenv("CORS_METHODS") != "*" else ["*"]
        cors_headers = os.getenv("CORS_HEADERS", "*").split(",") if os.getenv("CORS_HEADERS") != "*" else ["*"]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,  # Configurable origins
            allow_methods=cors_methods,  # Configurable HTTP methods
            allow_headers=cors_headers,  # Configurable headers
            allow_credentials=os.getenv("CORS_CREDENTIALS", "false").lower() == "true",
        )

        # Disable uvicorn access logs to reduce noise from health checks
        config = uvicorn.Config(app, host=host, port=port, access_log=False)
        server = uvicorn.Server(config=config)
        await server.serve()

if __name__ == '__main__':
    main()
