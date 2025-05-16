"""Tools for /incidents/types operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listIncidentTypes() -> Dict[str, Any]:
    """
    List incident types

    List the available incident types

Incident Types are a feature which will allow customers to categorize incidents, such as a security incident, a major incident, or a fraud incident.
These can be filtered by enabled or disabled types.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidentType)

Scoped OAuth requires: `incident_types.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /incidents/types")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incidents/types",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createIncidentType() -> Dict[str, Any]:
    """
    Create an Incident Type

    Create a new incident type.

Incident Types are a feature which will allow customers to categorize incidents, such as a security incident, a major incident, or a fraud incident.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#incidentType)

Scoped OAuth requires: `incident_types.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /incidents/types")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incidents/types",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
