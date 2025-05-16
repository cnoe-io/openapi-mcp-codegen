"""Tools for /priorities operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listPriorities() -> Dict[str, Any]:
    """
    List priorities

    List existing priorities, in order (most to least severe).

A priority is a label representing the importance and impact of an incident. This feature is only available on Standard and Enterprise plans.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#priorities)

Scoped OAuth requires: `priorities.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /priorities")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/priorities",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
