"""Tools for /users operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listUsers() -> Dict[str, Any]:
    """
    List users

    List users of your PagerDuty account, optionally filtered by a search query.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /users")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/users",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createUser() -> Dict[str, Any]:
    """
    Create a user

    Create a new user.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)

Scoped OAuth requires: `users.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /users")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/users",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
