"""Tools for /escalation_policies operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listEscalationPolicies() -> Dict[str, Any]:
    """
    List escalation policies

    List all of the existing escalation policies.

Escalation policies define which user should be alerted at which time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#escalation-policies)

Scoped OAuth requires: `escalation_policies.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /escalation_policies")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/escalation_policies",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createEscalationPolicy() -> Dict[str, Any]:
    """
    Create an escalation policy

    Creates a new escalation policy. At least one escalation rule must be provided.

Escalation policies define which user should be alerted at which time.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#escalation-policies)

Scoped OAuth requires: `escalation_policies.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /escalation_policies")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/escalation_policies",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
