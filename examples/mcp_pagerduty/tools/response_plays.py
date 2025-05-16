"""Tools for /response_plays operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listResponsePlays() -> Dict[str, Any]:
    """
    List Response Plays

    List all of the existing Response Plays.

Response Plays allow you to create packages of Incident Actions that can be applied during an Incident's life cycle.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#response-plays)

When using a Global API token, the `From` header is required.

Scoped OAuth requires: `response_plays.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /response_plays")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/response_plays",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createResponsePlay() -> Dict[str, Any]:
    """
    Create a Response Play

    Creates a new Response Plays.

Response Plays allow you to create packages of Incident Actions that can be applied during an Incident's life cycle.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#response-plays)

Scoped OAuth requires: `response_plays.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /response_plays")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/response_plays",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
