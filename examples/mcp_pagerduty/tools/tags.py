"""Tools for /tags operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listTags() -> Dict[str, Any]:
    """
    List tags

    List all of your account's tags.

A Tag is applied to Escalation Policies, Teams or Users and can be used to filter them.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#tags)

Scoped OAuth requires: `tags.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /tags")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/tags",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createTags() -> Dict[str, Any]:
    """
    Create a tag

    Create a Tag.

A Tag is applied to Escalation Policies, Teams or Users and can be used to filter them.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#tags)

Scoped OAuth requires: `tags.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /tags")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/tags",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
