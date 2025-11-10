"""
Minimal WebSocket JSON-RPC proxy for {{ mcp_name | capitalize }} agent (A2A disabled).
"""
import asyncio
import json
import logging
from typing import Any, Dict

from langchain_core.messages.base import messages_to_dict
from langfuse import get_client
from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler

import websockets
from websockets.server import serve

from agent import create_agent

logger = logging.getLogger(__name__)

async def handle_ws(websocket):
    """
    Very small JSON-RPC 2.0 over WebSocket handler compatible with the proxy.
    The proxy sends one JSON-RPC request; this server streams back LangGraph
    values payloads serialized to JSON.
    """
    msg = await websocket.recv()
    try:
        req = json.loads(msg)
    except Exception:
        req = {}

    params = req.get("params") or {}
    message = params.get("message") or {}

    # Extract user text & context id
    query = ""
    parts = message.get("parts") or []
    for p in parts:
        if isinstance(p, dict) and p.get("kind") == "text" and "text" in p:
            query = p["text"]
            break
    context_id = message.get("contextId") or message.get("context_id") or "ctx-1"

    inputs = {"messages": [("user", query)]}
    config = {"configurable": {"thread_id": context_id}}

    agent, _ = await create_agent()
    lf = get_client()
    lf_handler = None
    try:
        lf_handler = LangfuseCallbackHandler()
    except Exception:
        pass

    with lf.start_as_current_span(
        name="{{ mcp_name }}-query",
        input={"query": query, "context_id": context_id},
    ) as root_span:
        root_span.update_trace(tags=["{{ mcp_name }}-ws-proxy"], session_id=context_id)
        async for item in agent.astream(
            inputs,
            {**config, "callbacks": ([lf_handler] if lf_handler else [])},
            stream_mode="values",
        ):
            if isinstance(item, dict) and "messages" in item:
                msgs = item["messages"]
                try:
                    out = {"messages": messages_to_dict(msgs)}
                except Exception:
                    out = {"messages": [str(m) for m in msgs]}
            else:
                out = item
            await websocket.send(json.dumps(out))
        # Optional: set final output summary on trace
        try:
            state = agent.get_state(config)
            output_msg = state.values.get("messages", [])[-1]
            root_span.update_trace(output={"response": getattr(output_msg, "content", str(output_msg))})
        except Exception:
            pass


def main(host: str = "0.0.0.0", port: int = 8000) -> None:
    logging.basicConfig(level=logging.INFO)

    async def _serve():
        async with serve(handle_ws, host, port):
            logger.info("WebSocket proxy listening on ws://%s:%d", host, port)
            await asyncio.Future()  # run forever

    asyncio.run(_serve())


if __name__ == "__main__":
    main()
