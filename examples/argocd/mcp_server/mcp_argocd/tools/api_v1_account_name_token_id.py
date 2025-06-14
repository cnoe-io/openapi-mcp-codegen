# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/account/{name}/token/{id} operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def account_service__delete_token(path_name: str, path_id: str) -> Dict[str, Any]:
    '''
    Deletes a token associated with the specified account.

    Args:
        path_name (str): The name of the account from which the token will be deleted.
        path_id (str): The identifier of the token to be deleted.

    Returns:
        Dict[str, Any]: A dictionary containing the JSON response from the API call, which includes the status of the deletion operation.

    Raises:
        Exception: If the API request fails or returns an error, an exception is raised with details about the failure.
    '''
    logger.debug("Making DELETE request to /api/v1/account/{name}/token/{id}")

    params = {}
    data = {}

    success, response = await make_api_request(
        f"/api/v1/account/{path_name}/token/{path_id}", method="DELETE", params=params, data=data
    )

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response