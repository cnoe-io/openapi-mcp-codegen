# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/applications/{name}/links operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def application_service__list_links(
    path_name: str, param_namespace: str = None, param_project: str = None
) -> Dict[str, Any]:
    '''
    ListLinks returns the list of all application deep links.

    Args:
        path_name (str): The name of the application path for which to list deep links.
        param_namespace (str, optional): The namespace parameter for the API request. Defaults to None.
        param_project (str, optional): The project parameter for the API request. Defaults to None.

    Returns:
        Dict[str, Any]: The JSON response from the API call containing the list of application deep links.

    Raises:
        Exception: If the API request fails or returns an error.
    '''
    logger.debug("Making GET request to /api/v1/applications/{name}/links")

    params = {}
    data = {}

    params["namespace"] = param_namespace
    params["project"] = param_project

    success, response = await make_api_request(
        f"/api/v1/applications/{path_name}/links", method="GET", params=params, data=data
    )

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response