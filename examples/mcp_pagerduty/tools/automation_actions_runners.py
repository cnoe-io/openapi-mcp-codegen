"""Tools for /automation_actions/runners operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def createAutomationActionsRunner() -> Dict[str, Any]:
    """
    Create an Automation Action runner.

    Create a Process Automation or a Runbook Automation runner.


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /automation_actions/runners")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/automation_actions/runners",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def getAutomationActionsRunners() -> Dict[str, Any]:
    """
    List Automation Action runners

    Lists Automation Action runners matching provided query params.
The returned records are sorted by runner name in alphabetical order.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /automation_actions/runners")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/automation_actions/runners",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
