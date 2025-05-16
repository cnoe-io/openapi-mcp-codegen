"""Tools for /incidents/custom_fields operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def createCustomFieldsField() -> Dict[str, Any]:
    """
    Create a Field

    
<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields/post)

Creates a new Custom Field on the Base Incident Type, along with the Field Options if provided. \
An account may have up to 10 Fields.

Scoped OAuth requires: `custom_fields.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /incidents/custom_fields")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incidents/custom_fields",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def listCustomFieldsFields() -> Dict[str, Any]:
    """
    List Fields

    
<!-- theme: warning -->
> ### Deprecated
> This endpoint is deprecated and only works for fields on the Base Incident Type. \
> For more flexibility, we recommend using the Incident Types endpoint: \
> [/incidents/types/{type_id_or_name}/custom_fields](openapiv3.json/paths/~1incidents~1types~1{type_id_or_name}~1custom_fields/get)

List Custom Fields on the Base Incident Type.

Scoped OAuth requires: `custom_fields.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /incidents/custom_fields")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/incidents/custom_fields",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
