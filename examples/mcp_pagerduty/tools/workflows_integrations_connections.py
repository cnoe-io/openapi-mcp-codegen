"""Tools for /workflows/integrations/connections operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listWorkflowIntegrationConnections() -> Dict[str, Any]:
    """
    List all Workflow Integration Connections

    List all Workflow Integration Connections.

Scoped OAuth requires: `workflow_integrations:connections.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /workflows/integrations/connections")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/workflows/integrations/connections",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
