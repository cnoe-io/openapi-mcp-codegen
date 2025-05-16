"""Tools for /extension_schemas operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listExtensionSchemas() -> Dict[str, Any]:
    """
    List extension schemas

    List all extension schemas.

A PagerDuty extension vendor represents a specific type of outbound extension such as Generic Webhook, Slack, ServiceNow.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#extension-schemas)

Scoped OAuth requires: `extension_schemas.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /extension_schemas")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/extension_schemas",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
