# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/account/can-i/{resource}/{action}/{subresource} operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def account_service__can_i(path_resource: str, path_action: str, path_subresource: str) -> Dict[str, Any]:
    '''
    CanI checks if the current account has permission to perform an action.

    Args:
        path_resource (str): The resource path for which permission is being checked.
        path_action (str): The action to be performed on the resource.
        path_subresource (str): The subresource path related to the main resource.

    Returns:
        Dict[str, Any]: A dictionary containing the JSON response from the API call, indicating whether the action is permitted.

    Raises:
        Exception: If the API request fails or returns an error, an exception is raised with the error details.
    '''
    logger.debug("Making GET request to /api/v1/account/can-i/{resource}/{action}/{subresource}")

    params = {}
    data = {}

    success, response = await make_api_request(
        f"/api/v1/account/can-i/{path_resource}/{path_action}/{path_subresource}",
        method="GET",
        params=params,
        data=data,
    )

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response