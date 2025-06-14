# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /store/order/{orderId} operations"""

import logging
from typing import Dict, Any
from mcp_petstore.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def get_order_by_id(path_orderId: int) -> Dict[str, Any]:
    """
    Find purchase order by ID.

    OpenAPI Description:
        For valid response try integer IDs with value <= 5 or > 10. Other values will generate exceptions.

    Args:

        path_orderId (int): ID of order that needs to be fetched


    Returns:
        Dict[str, Any]: The JSON response from the API call.

    Raises:
        Exception: If the API request fails or returns an error.
    """
    logger.debug("Making GET request to /store/order/{orderId}")

    params = {}
    data = {}

    success, response = await make_api_request(f"/store/order/{path_orderId}", method="GET", params=params, data=data)

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response


async def delete_order(path_orderId: int) -> Dict[str, Any]:
    """
    Delete purchase order by identifier.

    OpenAPI Description:
        For valid response try integer IDs with value < 1000. Anything above 1000 or non-integers will generate API errors.

    Args:

        path_orderId (int): ID of the order that needs to be deleted


    Returns:
        Dict[str, Any]: The JSON response from the API call.

    Raises:
        Exception: If the API request fails or returns an error.
    """
    logger.debug("Making DELETE request to /store/order/{orderId}")

    params = {}
    data = {}

    success, response = await make_api_request(
        f"/store/order/{path_orderId}", method="DELETE", params=params, data=data
    )

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response
