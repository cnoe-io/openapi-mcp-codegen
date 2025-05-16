"""Tools for /event_orchestrations operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listEventOrchestrations() -> Dict[str, Any]:
    """
    List Event Orchestrations

    List all Global Event Orchestrations on an Account.

Global Event Orchestrations allow you define a set of Global Rules and Router Rules, so that when you ingest events using the Orchestration's Routing Key your events will have actions applied via the Global Rules & then routed to the correct Service by the Router Rules, based on the event's content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /event_orchestrations")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/event_orchestrations",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def postOrchestration() -> Dict[str, Any]:
    """
    Create an Orchestration

    Create a Global Event Orchestration.

Global Event Orchestrations allow you define a set of Global Rules and Router Rules, so that when you ingest events using the Orchestration's Routing Key your events will have actions applied via the Global Rules & then routed to the correct Service by the Router Rules, based on the event's content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#event-orchestrations)

Scoped OAuth requires: `event_orchestrations.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /event_orchestrations")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/event_orchestrations",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
