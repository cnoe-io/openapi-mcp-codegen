
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/account/password operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def accountservice_updatepassword(body: str) -> Dict[str, Any]:
    '''
    Updates an account's password to a new value.

    Args:
        body (str): The new password or password update payload in string format.

    Returns:
        Dict[str, Any]: The response from the API, containing success status or error details.

    Raises:
        Exception: If the API request fails or returns an unexpected response.

    OpenAPI Specification:
      put:
        summary: Update an account's password.
        description: Updates the password for the authenticated account to a new value.
        operationId: accountservice_updatepassword
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: string
              example: '{"new_password": "MyN3wP@ssw0rd"}'
        responses:
          '200':
            description: Password updated successfully.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      example: Password updated successfully.
          '400':
            description: Invalid request or password format.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: Invalid password format.
          '401':
            description: Unauthorized. Authentication required.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: Authentication required.
          '500':
            description: Internal server error.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      example: Internal server error.
    '''
    logger.debug("Making PUT request to /api/v1/account/password")
    params = {}
    data = None

    # Add parameters to request
    if body is not None:
        data = body

    success, response = await make_api_request(
        "/api/v1/account/password",
        method="PUT",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
