"""Tools for /license_allocations operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listLicenseAllocations() -> Dict[str, Any]:
    """
    List License Allocations

    List the Licenses allocated to Users within your Account

Scoped OAuth requires: `licenses.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /license_allocations")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/license_allocations",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
