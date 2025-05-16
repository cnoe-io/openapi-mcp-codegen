"""Tools for /incidents operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listIncidents() -> Dict[str, Any]:
    """
    List incidents

    List existing incidents.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /incidents")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incidents",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def updateIncidents() -> Dict[str, Any]:
    """
    Manage incidents

    Acknowledge, resolve, escalate or reassign one or more incidents.

An incident represents a problem or an issue that needs to be addressed and resolved.

A maximum of 250 incidents may be updated at a time. If more than this number of incidents are given, the API will respond with status 413 (Request Entity Too Large).

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`

This API operation has operation specific rate limits. See the [Rate Limits](https://developer.pagerduty.com/docs/72d3b724589e3-rest-api-rate-limits) page for more information.


    Returns:
        API response data
    """
    logger.debug(f"Making PUT request to /incidents")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incidents",
        method="PUT",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createIncident() -> Dict[str, Any]:
    """
    Create an Incident

    Create an incident synchronously without a corresponding event from a monitoring service.

An incident represents a problem or an issue that needs to be addressed and resolved.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidents)

Scoped OAuth requires: `incidents.write`

This API operation has operation specific rate limits. See the [Rate Limits](https://developer.pagerduty.com/docs/72d3b724589e3-rest-api-rate-limits) page for more information.


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /incidents")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incidents",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
