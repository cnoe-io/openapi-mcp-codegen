"""Tools for /services/custom_fields operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def createServiceCustomField() -> Dict[str, Any]:
    """
    Create a Field

    <!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

Creates a new Custom Field for Services, along with the Field Options if provided.

Scoped OAuth requires: `custom_fields.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /services/custom_fields")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/services/custom_fields",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def listServiceCustomFields() -> Dict[str, Any]:
    """
    List Fields

    <!-- theme: warning -->
> ### Early Access
> This endpoint is in Early Access and may change at any time. You must pass in the `X-EARLY-ACCESS` header with `service-custom-fields-preview` to access it.

List Custom Fields available for Services.

Scoped OAuth requires: `custom_fields.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /services/custom_fields")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/services/custom_fields",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
