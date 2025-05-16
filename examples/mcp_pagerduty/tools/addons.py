"""Tools for /addons operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listAddon() -> Dict[str, Any]:
    """
    List installed Add-ons

    List all of the Add-ons installed on your account.

Addon's are pieces of functionality that developers can write to insert new functionality into PagerDuty's UI.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#add-ons)

Scoped OAuth requires: `addons.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /addons")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/addons",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createAddon() -> Dict[str, Any]:
    """
    Install an Add-on

    Install an Add-on for your account.

Addon's are pieces of functionality that developers can write to insert new functionality into PagerDuty's UI.

Given a configuration containing a `src` parameter, that URL will be embedded in an `iframe` on a page that's available to users from a drop-down menu.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#add-ons)

Scoped OAuth requires: `addons.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /addons")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/addons",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
