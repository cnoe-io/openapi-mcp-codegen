"""Tools for /extensions operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listExtensions() -> Dict[str, Any]:
    """
    List extensions

    List existing extensions.

Extensions are representations of Extension Schema objects that are attached to Services.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extensions)

Scoped OAuth requires: `extensions.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /extensions")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/extensions",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createExtension() -> Dict[str, Any]:
    """
    Create an extension

    Create a new Extension.

Extensions are representations of Extension Schema objects that are attached to Services.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extensions)

Scoped OAuth requires: `extensions.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /extensions")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/extensions",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
