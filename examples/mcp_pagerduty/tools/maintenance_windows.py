"""Tools for /maintenance_windows operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listMaintenanceWindows() -> Dict[str, Any]:
    """
    List maintenance windows

    List existing maintenance windows, optionally filtered by service and/or team, or whether they are from the past, present or future.

A Maintenance Window is used to temporarily disable one or more Services for a set period of time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#maintenance-windows)

Scoped OAuth requires: `services.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /maintenance_windows")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/maintenance_windows",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createMaintenanceWindow() -> Dict[str, Any]:
    """
    Create a maintenance window

    Create a new maintenance window for the specified services. No new incidents will be created for a service that is in maintenance.

A Maintenance Window is used to temporarily disable one or more Services for a set period of time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#maintenance-windows)

Scoped OAuth requires: `services.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /maintenance_windows")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/maintenance_windows",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
