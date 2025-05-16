"""Tools for /incident_workflows/triggers operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listIncidentWorkflowTriggers() -> Dict[str, Any]:
    """
    List Triggers

    List existing Incident Workflow Triggers

Scoped OAuth requires: `incident_workflows.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /incident_workflows/triggers")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incident_workflows/triggers",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createIncidentWorkflowTrigger() -> Dict[str, Any]:
    """
    Create a Trigger

    Create new Incident Workflow Trigger

Scoped OAuth requires: `incident_workflows.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /incident_workflows/triggers")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incident_workflows/triggers",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
