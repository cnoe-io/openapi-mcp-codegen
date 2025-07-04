# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /pet/{petId} operations"""

import logging
from typing import Dict, Any
from mcp_petstore.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def get_pet_by_id(path_petId: int) -> Dict[str, Any]:
    '''
    Find pet by ID.

    Args:
        path_petId (int): The ID of the pet to retrieve.

    Returns:
        Dict[str, Any]: A dictionary containing the pet's details if found, or an error message if the request fails.

    Raises:
        Exception: If the API request fails or returns an error.
    '''
    logger.debug("Making GET request to /pet/{petId}")

    params = {}
    data = {}

    success, response = await make_api_request(f"/pet/{path_petId}", method="GET", params=params, data=data)

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response


async def update_pet_with_form(path_petId: int, param_name: str = None, param_status: str = None) -> Dict[str, Any]:
    '''
    Updates a pet in the store with form data.

    Args:
        path_petId (int): The ID of the pet to be updated.
        param_name (str, optional): The new name for the pet. Defaults to None.
        param_status (str, optional): The new status for the pet. Defaults to None.

    Returns:
        Dict[str, Any]: The JSON response from the API call, containing the updated pet information.

    Raises:
        Exception: If the API request fails or returns an error.
    '''
    logger.debug("Making POST request to /pet/{petId}")

    params = {}
    data = {}

    params["name"] = param_name
    params["status"] = param_status

    success, response = await make_api_request(f"/pet/{path_petId}", method="POST", params=params, data=data)

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response


async def delete_pet(path_petId: int) -> Dict[str, Any]:
    '''
    Deletes a pet.

    Args:
        path_petId (int): The ID of the pet to be deleted.

    Returns:
        Dict[str, Any]: The JSON response from the API call, which includes the status of the deletion operation.

    Raises:
        Exception: If the API request fails or returns an error, an exception is raised with the error details.
    '''
    logger.debug("Making DELETE request to /pet/{petId}")

    params = {}
    data = {}

    success, response = await make_api_request(f"/pet/{path_petId}", method="DELETE", params=params, data=data)

    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get("error", "Request failed")}
    return response