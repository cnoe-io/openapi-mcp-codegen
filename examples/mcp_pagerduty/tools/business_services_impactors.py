"""Tools for /business_services/impactors operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getBusinessServiceTopLevelImpactors() -> Dict[str, Any]:
    """
    List Impactors affecting Business Services

    Retrieve a list of Impactors for the top-level Business Services on the account. Impactors are currently limited to Incidents.

This endpoint does not return an exhaustive list of Impactors but rather provides access to the highest priority Impactors for the Business Services in question up to the limit of 200.

To get Impactors for a specific set of Business Services, use the `ids[]` parameter.

The returned Impactors are sorted first by priority and secondarily by their creation date.
Scoped OAuth requires: `services.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /business_services/impactors")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/business_services/impactors",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
