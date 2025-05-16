"""Tools for /schedules operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listSchedules() -> Dict[str, Any]:
    """
    List schedules

    List the on-call schedules.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /schedules")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/schedules",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createSchedule() -> Dict[str, Any]:
    """
    Create a schedule

    Create a new on-call schedule.

A Schedule determines the time periods that users are On-Call.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#schedules)

Scoped OAuth requires: `schedules.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /schedules")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/schedules",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
