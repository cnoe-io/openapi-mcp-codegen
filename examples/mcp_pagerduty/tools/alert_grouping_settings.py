"""Tools for /alert_grouping_settings operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listAlertGroupingSettings() -> Dict[str, Any]:
    """
    List alert grouping settings

    List all of your alert grouping settings including both single service settings and global content based settings.

The settings part of Alert Grouper service allows us to create Alert Grouping Settings and configs that are required to be used during grouping of the alerts.

Scoped OAuth requires: `services.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /alert_grouping_settings")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/alert_grouping_settings",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def postAlertGroupingSettings() -> Dict[str, Any]:
    """
    Create an Alert Grouping Setting

    Create a new Alert Grouping Setting.

The settings part of Alert Grouper service allows us to create Alert Grouping Settings and configs that are required to be used during grouping of the alerts.

This endpoint will be used to create an instance of AlertGroupingSettings for either one service or many services that are in the alert group setting.

Scoped OAuth requires: `services.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /alert_grouping_settings")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/alert_grouping_settings",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
