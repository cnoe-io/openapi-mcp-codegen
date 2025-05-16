"""Tools for /incident_workflows/actions operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listIncidentWorkflowActions() -> Dict[str, Any]:
    """
    List Actions

    List Incident Workflow Actions

Scoped OAuth requires: `incident_workflows.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /incident_workflows/actions")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incident_workflows/actions",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
