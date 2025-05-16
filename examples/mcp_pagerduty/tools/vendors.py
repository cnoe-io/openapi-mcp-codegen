"""Tools for /vendors operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listVendors() -> Dict[str, Any]:
    """
    List vendors

    List all vendors.

A PagerDuty Vendor represents a specific type of integration. AWS Cloudwatch, Splunk, Datadog are all examples of vendors

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#vendors)

Scoped OAuth requires: `vendors.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /vendors")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/vendors",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
