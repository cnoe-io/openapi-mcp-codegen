"""Tools for /automation_actions/actions operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def createAutomationAction() -> Dict[str, Any]:
    """
    Create an Automation Action

    Create a Script, Process Automation, or Runbook Automation action


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /automation_actions/actions")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/automation_actions/actions",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def getAllAutomationActions() -> Dict[str, Any]:
    """
    List Automation Actions

    Lists Automation Actions matching provided query params.

The returned records are sorted by action name in alphabetical order.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /automation_actions/actions")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/automation_actions/actions",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
