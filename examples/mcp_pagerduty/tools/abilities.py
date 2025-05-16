"""Tools for /abilities operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listAbilities() -> Dict[str, Any]:
    """
    List abilities

    List all of your account's abilities, by name.

"Abilities" describes your account's capabilities by feature name. For example `"teams"`.

An ability may be available to your account based on things like your pricing plan or account state.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#abilities)

Scoped OAuth requires: `abilities.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /abilities")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/abilities",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
