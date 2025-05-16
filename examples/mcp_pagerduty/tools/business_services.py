"""Tools for /business_services operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listBusinessServices() -> Dict[str, Any]:
    """
    List Business Services

    List existing Business Services.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /business_services")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/business_services",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createBusinessService() -> Dict[str, Any]:
    """
    Create a Business Service

    Create a new Business Service.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

There is a limit of 5,000 business services per account. If the limit is reached, the API will respond with an error.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /business_services")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/business_services",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
