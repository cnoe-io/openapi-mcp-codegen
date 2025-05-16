"""Tools for /business_services/impacts operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getBusinessServiceImpacts() -> Dict[str, Any]:
    """
    List Business Services sorted by impacted status

    Retrieve a list top-level Business Services sorted by highest Impact with `status` included.
When called without the `ids[]` parameter, this endpoint does not return an exhaustive list of Business Services but rather provides access to the most impacted up to the limit of 200.

The returned Business Services are sorted first by Impact, secondarily by most recently impacted, and finally by name.

To get impact information about a specific set of Business Services, use the `ids[]` parameter.
Scoped OAuth requires: `services.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /business_services/impacts")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/business_services/impacts",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
