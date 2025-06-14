# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/write-repocreds operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def repo_creds_service__list_write_repository_credentials(param_url: str = None) -> Dict[str, Any]:
    '''
    ListWriteRepositoryCredentials gets a list of all configured repository credential sets that have write access.

    Args:
        param_url (str, optional): Repo URL for query. Defaults to None.

    Returns:
        Dict[str, Any]: The JSON response from the API call containing the list of repository credentials with write access.

    Raises:
        Exception: If the API request fails or returns an error.
    '''
    logger.debug("Making GET request to /api/v1/write-repocreds")

    params = {}
    data = {}

    params["url"] = param_url

    success, response = await make_api_request("/api/v1/write-repocreds", method="GET", params=params, data=data)

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response


async def repo_creds_service__create_write_repository_credentials(param_upsert: str = None) -> Dict[str, Any]:
    '''
    CreateWriteRepositoryCredentials creates a new repository credential set with write access.

    Args:
        param_upsert (str, optional): Whether to create in upsert mode. Defaults to None.

    Returns:
        Dict[str, Any]: The JSON response from the API call, containing the details of the created repository credentials.

    Raises:
        Exception: If the API request fails or returns an error, an exception is raised with the error details.
    '''
    logger.debug("Making POST request to /api/v1/write-repocreds")

    params = {}
    data = {}

    params["upsert"] = param_upsert

    success, response = await make_api_request("/api/v1/write-repocreds", method="POST", params=params, data=data)

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response