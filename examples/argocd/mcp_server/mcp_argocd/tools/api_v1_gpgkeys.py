# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/gpgkeys operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def gpg_key_service__list(param_keyID: str = None) -> Dict[str, Any]:
    '''
    List all available repository certificates.

    Args:
        param_keyID (str, optional): The GPG key ID to query for. Defaults to None.

    Returns:
        Dict[str, Any]: The JSON response from the API call containing the list of GPG keys.

    Raises:
        Exception: If the API request fails or returns an error.
    '''
    logger.debug("Making GET request to /api/v1/gpgkeys")

    params = {}
    data = {}

    params["keyID"] = param_keyID

    success, response = await make_api_request("/api/v1/gpgkeys", method="GET", params=params, data=data)

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response


async def gpg_key_service__create(param_upsert: str = None) -> Dict[str, Any]:
    '''
    Create one or more GPG public keys in the server's configuration.

    Args:
        param_upsert (str, optional): Whether to upsert already existing public keys. Defaults to None.

    Returns:
        Dict[str, Any]: The JSON response from the API call.

    Raises:
        Exception: If the API request fails or returns an error.
    '''
    logger.debug("Making POST request to /api/v1/gpgkeys")

    params = {}
    data = {}

    params["upsert"] = param_upsert

    success, response = await make_api_request("/api/v1/gpgkeys", method="POST", params=params, data=data)

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response


async def gpg_key_service__delete(param_keyID: str = None) -> Dict[str, Any]:
    '''
    Delete specified GPG public key from the server's configuration.

    Args:
        param_keyID (str): The GPG key ID to query for.

    Returns:
        Dict[str, Any]: The JSON response from the API call.

    Raises:
        Exception: If the API request fails or returns an error.
    '''
    logger.debug("Making DELETE request to /api/v1/gpgkeys")

    params = {}
    data = {}

    params["keyID"] = param_keyID

    success, response = await make_api_request("/api/v1/gpgkeys", method="DELETE", params=params, data=data)

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response