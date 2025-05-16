"""Tools for /oauth_delegations/revocation_requests/status operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getOauthDelegationsRevocationRequestsStatus() -> Dict[str, Any]:
    """
    Get OAuth delegations revocation requests status

    Get the status of all OAuth delegations revocation requests for this account, specifically how many requests are still pending.

This endpoint is limited to account owners and admins.

Scoped OAuth requires: `oauth_delegations.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /oauth_delegations/revocation_requests/status")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/oauth_delegations/revocation_requests/status",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
