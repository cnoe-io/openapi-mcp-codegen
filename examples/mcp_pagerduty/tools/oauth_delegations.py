"""Tools for /oauth_delegations operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def deleteOauthDelegations() -> Dict[str, Any]:
    """
    Delete all OAuth delegations

    Delete all OAuth delegations as per provided query parameters.

An OAuth delegation represents an instance of a user or account's authorization to an app (via OAuth) to access their PagerDuty account.
Common apps include the PagerDuty mobile app, Slack, Microsoft Teams, and third-party apps.

Deleting an OAuth delegation will revoke that instance of an app's access to that user or account.
To grant access again, reauthorization/reauthentication may be required.

At this time, this endpoint only supports deleting mobile app OAuth delegations for a given user.
This is equivalent to signing users out of the mobile app.

This is an asynchronous API, the deletion request itself will be processed within 24 hours.

Scoped OAuth requires: `oauth_delegations.write`


    Returns:
        API response data
    """
    logger.debug(f"Making DELETE request to /oauth_delegations")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/oauth_delegations",
        method="DELETE",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
