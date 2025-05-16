"""Tools for /users/me operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getCurrentUser() -> Dict[str, Any]:
    """
    Get the current user

    Get details about the current user.

This endpoint can only be used with a [user-level API key](https://support.pagerduty.com/docs/using-the-api#section-generating-a-personal-rest-api-key) or a key generated through an OAuth flow. This will not work if the request is made with an account-level access token.

Users are members of a PagerDuty account that have the ability to interact with Incidents and other data on the account.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#users)


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /users/me")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/users/me",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
