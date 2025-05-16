"""Tools for /teams operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def createTeam() -> Dict[str, Any]:
    """
    Create a team

    Create a new Team.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /teams")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/teams",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def listTeams() -> Dict[str, Any]:
    """
    List teams

    List teams of your PagerDuty account, optionally filtered by a search query.

A team is a collection of Users and Escalation Policies that represent a group of people within an organization.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#teams)

Scoped OAuth requires: `teams.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /teams")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/teams",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
