"""Tools for /status_pages operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listStatusPages() -> Dict[str, Any]:
    """
    List Status Pages

    List Status Pages.

Scoped OAuth requires: `status_pages.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /status_pages")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/status_pages",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
