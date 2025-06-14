# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/applications/{name}/spec operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def application_service__update_spec(
    path_name: str, param_validate: str = None, param_appNamespace: str = None, param_project: str = None
) -> Dict[str, Any]:
    '''
    UpdateSpec updates an application spec.

    Args:
        path_name (str): The name of the application path to update the spec for.
        param_validate (str, optional): Validation parameter for the request. Defaults to None.
        param_appNamespace (str, optional): The namespace of the application. Defaults to None.
        param_project (str, optional): The project associated with the application. Defaults to None.

    Returns:
        Dict[str, Any]: The JSON response from the API call, containing the updated application spec.

    Raises:
        Exception: If the API request fails or returns an error.
    '''
    logger.debug("Making PUT request to /api/v1/applications/{name}/spec")

    params = {}
    data = {}

    params["validate"] = param_validate
    params["appNamespace"] = param_appNamespace
    params["project"] = param_project

    success, response = await make_api_request(
        f"/api/v1/applications/{path_name}/spec", method="PUT", params=params, data=data
    )

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response