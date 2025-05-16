"""Tools for /change_events operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listChangeEvents() -> Dict[str, Any]:
    """
    List Change Events

    List all of the existing Change Events.

Scoped OAuth requires: `change_events.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /change_events")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/change_events",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createChangeEvent() -> Dict[str, Any]:
    """
    Create a Change Event

    Sending Change Events is documented as part of the V2 Events API. See [`Send Change Event`](https://developer.pagerduty.com/api-reference/b3A6Mjc0ODI2Ng-send-change-events-to-the-pager-duty-events-api).


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /change_events")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/change_events",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
