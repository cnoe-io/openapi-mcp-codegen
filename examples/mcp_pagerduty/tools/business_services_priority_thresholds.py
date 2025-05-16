"""Tools for /business_services/priority_thresholds operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getBusinessServicePriorityThresholds() -> Dict[str, Any]:
    """
    Get the global priority threshold for a Business Service to be considered impacted by an Incident

    Retrieves the priority threshold information for an account.  Currently, there is a `global_threshold` that can be set for the account.  Incidents that have a priority meeting or exceeding this threshold will be considered impacting on any Business Service that depends on the Service to which the Incident belongs.
Scoped OAuth requires: `services.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /business_services/priority_thresholds")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/business_services/priority_thresholds",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def deleteBusinessServicePriorityThresholds() -> Dict[str, Any]:
    """
    Deletes the account-level priority threshold for Business Service impact

    Clears the Priority Threshold for the account.  If the priority threshold is cleared, any Incident with a Priority set will be able to impact Business Services.
Scoped OAuth requires: `services.write`


    Returns:
        API response data
    """
    logger.debug(f"Making DELETE request to /business_services/priority_thresholds")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/business_services/priority_thresholds",
        method="DELETE",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def putBusinessServicePriorityThresholds() -> Dict[str, Any]:
    """
    Set the Account-level priority threshold for Business Service impact.

    Set the Account-level priority threshold for Business Service.
Scoped OAuth requires: `services.write`


    Returns:
        API response data
    """
    logger.debug(f"Making PUT request to /business_services/priority_thresholds")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/business_services/priority_thresholds",
        method="PUT",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
