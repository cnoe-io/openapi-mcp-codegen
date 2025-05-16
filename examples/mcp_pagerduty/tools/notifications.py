"""Tools for /notifications operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listNotifications() -> Dict[str, Any]:
    """
    List notifications

    List notifications for a given time range, optionally filtered by type (sms_notification, email_notification, phone_notification, or push_notification).

A Notification is created when an Incident is triggered or escalated.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#notifications)

Scoped OAuth requires: `users:notifications.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /notifications")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/notifications",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
