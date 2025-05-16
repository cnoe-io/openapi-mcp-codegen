"""Tools for /incident_workflows operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listIncidentWorkflows() -> Dict[str, Any]:
    """
    List Incident Workflows

    List existing Incident Workflows.

This is the best method to use to list all Incident Workflows in your account. If your use case requires listing Incident Workflows associated with a particular Service, you can use the "List Triggers" method to find Incident Workflows configured to start for Incidents in a given Service.

An Incident Workflow is a sequence of configurable Steps and associated Triggers that can execute automated Actions for a given Incident.

Scoped OAuth requires: `incident_workflows.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /incident_workflows")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incident_workflows",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def postIncidentWorkflow() -> Dict[str, Any]:
    """
    Create an Incident Workflow

    Create a new Incident Workflow

An Incident Workflow is a sequence of configurable Steps and associated Triggers that can execute automated Actions for a given Incident.

Scoped OAuth requires: `incident_workflows.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /incident_workflows")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incident_workflows",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
