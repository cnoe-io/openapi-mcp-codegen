"""Tools for /templates/fields operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getTemplateFields() -> Dict[str, Any]:
    """
    List template fields

    Get a list of fields that can be used on the account templates.

Scoped OAuth requires: `templates.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /templates/fields")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/templates/fields",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
