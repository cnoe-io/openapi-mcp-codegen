"""Tools for /services operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listServices() -> Dict[str, Any]:
    """
    List services

    List existing Services.

A service may represent an application, component, or team you wish to open incidents against.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /services")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/services",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createService() -> Dict[str, Any]:
    """
    Create a service

    Create a new service.

If `status` is included in the request, it must have a value of `active` when creating a new service. If a different status is required, make a second request to update the service.

A service may represent an application, component, or team you wish to open incidents against.

There is a limit of 25,000 services per account. If the limit is reached, the API will respond with an error. There is also a limit of 100,000 open Incidents per Service. If the limit is reached and `auto_resolve_timeout` is disabled (set to 0 or null), the `auto_resolve_timeout` property will automatically be set to  84600 (1 day).

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#services)

Scoped OAuth requires: `services.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /services")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/services",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
