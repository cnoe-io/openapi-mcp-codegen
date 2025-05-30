
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


async def gpgkeyservice_list(keyID: str = None) -> Dict[str, Any]:
    '''
    List all available repository certificates.

    Args:
        keyID (str, optional): The ID of the GPG key to filter results. Defaults to None.

    Returns:
        Dict[str, Any]: A dictionary containing the list of available repository certificates or an error message.

    Raises:
        Exception: If the API request fails or returns an unexpected response.

    OpenAPI Specification:
      get:
        summary: List all available repository certificates
        description: Retrieve a list of all GPG keys (repository certificates) available in the system. Optionally filter by key ID.
        operationId: gpgkeyservice_list
        parameters:
          - in: query
            name: keyID
            schema:
              type: string
            required: false
            description: The ID of the GPG key to filter results.
        responses:
          '200':
            description: A list of available repository certificates.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    keys:
                      type: array
                      items:
                        type: object
          '400':
            description: Invalid request parameters.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
          '500':
            description: Internal server error.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
    '''
    logger.debug("Making GET request to /api/v1/gpgkeys")
    params = {}
    data = None

    success, response = await make_api_request(
        "/api/v1/gpgkeys",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response


async def gpgkeyservice_create(body: str, upsert: str = None) -> Dict[str, Any]:
    '''
    Create one or more GPG public keys in the server's configuration.

    Args:
        body (str): The GPG public key(s) to add, in ASCII-armored format.
        upsert (str, optional): If set, allows updating existing keys. Defaults to None.

    Returns:
        Dict[str, Any]: The response from the server, including details of the created or updated keys.

    Raises:
        ValueError: If the request body is invalid or missing required fields.
        RuntimeError: If the server returns an error or the request fails.

    OpenAPI Specification:
      post:
        summary: Create one or more GPG public keys in the server's configuration.
        operationId: gpgkeyservice_create
        requestBody:
          required: true
          content:
            text/plain:
              schema:
                type: string
                description: The GPG public key(s) in ASCII-armored format.
        parameters:
          - in: query
            name: upsert
            schema:
              type: string
            required: false
            description: If set, allows updating existing keys.
        responses:
          '200':
            description: Keys created or updated successfully.
            content:
              application/json:
                schema:
                  type: object
                  additionalProperties: true
          '400':
            description: Invalid request body or parameters.
          '500':
            description: Server error.
    '''
    logger.debug("Making POST request to /api/v1/gpgkeys")
    params = {}
    data = None

    # Add parameters to request
    if body is not None:
        data = body

    success, response = await make_api_request(
        "/api/v1/gpgkeys",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response


async def gpgkeyservice_delete(keyID: str = None) -> Dict[str, Any]:
    '''
    Delete the specified GPG public key from the server's configuration.

    Args:
        keyID (str, optional): The unique identifier of the GPG public key to delete. Defaults to None.

    Returns:
        Dict[str, Any]: The response from the server indicating the result of the delete operation.

    Raises:
        Exception: If the API request fails or the server returns an error.

    OpenAPI Specification:
      delete:
        summary: Delete a GPG public key
        description: Deletes the specified GPG public key from the server's configuration.
        operationId: gpgkeyservice_delete
        parameters:
          - in: query
            name: keyID
            schema:
              type: string
            required: false
            description: The unique identifier of the GPG public key to delete.
        responses:
          '200':
            description: GPG public key deleted successfully.
            content:
              application/json:
                schema:
                  type: object
                  additionalProperties: true
          '400':
            description: Invalid request or missing keyID.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
          '404':
            description: GPG public key not found.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
          '500':
            description: Server error.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
    '''
    logger.debug("Making DELETE request to /api/v1/gpgkeys")
    params = {}
    data = None

    success, response = await make_api_request(
        "/api/v1/gpgkeys",
        method="DELETE",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
