"""Tools for /webhook_subscriptions operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listWebhookSubscriptions() -> Dict[str, Any]:
    """
    List webhook subscriptions

    List existing webhook subscriptions.

The `filter_type` and `filter_id` query parameters may be used to only show subscriptions
for a particular _service_ or _team_.

For more information on webhook subscriptions and how they are used to configure v3 webhooks
see the [Webhooks v3 Developer Documentation](https://developer.pagerduty.com/docs/webhooks/v3-overview/).

Scoped OAuth requires: `webhook_subscriptions.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /webhook_subscriptions")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/webhook_subscriptions",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createWebhookSubscription() -> Dict[str, Any]:
    """
    Create a webhook subscription

    Creates a new webhook subscription.

For more information on webhook subscriptions and how they are used to configure v3 webhooks
see the [Webhooks v3 Developer Documentation](https://developer.pagerduty.com/docs/webhooks/v3-overview/).

Scoped OAuth requires: `webhook_subscriptions.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /webhook_subscriptions")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/webhook_subscriptions",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
