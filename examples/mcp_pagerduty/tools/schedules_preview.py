"""Tools for /schedules/preview operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def createSchedulePreview() -> Dict[str, Any]:
    """
    Preview a schedule

    Preview what an on-call schedule would look like without saving it.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /schedules/preview")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/schedules/preview",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
