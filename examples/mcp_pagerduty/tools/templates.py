"""Tools for /templates operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getTemplates() -> Dict[str, Any]:
    """
    List templates

    Get a list of all the template on an account

Scoped OAuth requires: `templates.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /templates")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/templates",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createTemplate() -> Dict[str, Any]:
    """
    Create a template

    Create a new template

Scoped OAuth requires: `templates.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /templates")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/templates",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
