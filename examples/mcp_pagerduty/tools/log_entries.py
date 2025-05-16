"""Tools for /log_entries operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listLogEntries() -> Dict[str, Any]:
    """
    List log entries

    List all of the incident log entries across the entire account.

A log of all the events that happen to an Incident, and these are exposed as Log Entries.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#log-entries)

Scoped OAuth requires: `incidents.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /log_entries")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/log_entries",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
