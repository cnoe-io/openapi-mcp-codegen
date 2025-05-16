"""Tools for /service_dependencies/disassociate operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def deleteServiceDependency() -> Dict[str, Any]:
    """
    Disassociate service dependencies

    Disassociate dependencies between two services.

Business services model capabilities that span multiple technical services and that may be owned by several different teams.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#business-services)

Scoped OAuth requires: `services.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /service_dependencies/disassociate")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/service_dependencies/disassociate",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
