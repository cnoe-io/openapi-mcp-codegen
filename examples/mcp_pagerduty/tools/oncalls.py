"""Tools for /oncalls operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listOnCalls() -> Dict[str, Any]:
    """
    List all of the on-calls

    List the on-call entries during a given time range.

An on-call represents a contiguous unit of time for which a User will be on call for a given Escalation Policy and Escalation Rules.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#on-calls)

Scoped OAuth requires: `oncalls.read`

This API operation has operation specific rate limits. See the [Rate Limits](https://developer.pagerduty.com/docs/72d3b724589e3-rest-api-rate-limits) page for more information.


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /oncalls")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/oncalls",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
