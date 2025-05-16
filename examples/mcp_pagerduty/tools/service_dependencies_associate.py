"""Tools for /service_dependencies/associate operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def createServiceDependency() -> Dict[str, Any]:
    """
    Associate service dependencies

    Create new dependencies between two services.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

A service can have a maximum of 2,000 dependencies with a depth limit of 100. If the limit is reached, the API will respond with an error.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /service_dependencies/associate")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/service_dependencies/associate",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
