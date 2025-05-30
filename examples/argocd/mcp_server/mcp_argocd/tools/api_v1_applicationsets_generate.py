
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/applicationsets/generate operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def applicationsetservice_generate(body: str) -> Dict[str, Any]:
    '''
    Generates an ApplicationSet resource based on the provided input.

    Args:
        body (str): The request payload containing the ApplicationSet configuration.

    Returns:
        Dict[str, Any]: The generated ApplicationSet resource or an error message.

    Raises:
        Exception: If the API request fails or an unexpected error occurs.

    OpenAPI Specification:
      post:
        summary: Generate an ApplicationSet resource.
        description: Generates an ApplicationSet resource based on the provided configuration.
        operationId: applicationsetservice_generate
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: string
              example: '{"apiVersion": "argoproj.io/v1alpha1", "kind": "ApplicationSet", ...}'
        responses:
          '200':
            description: Successfully generated ApplicationSet resource.
            content:
              application/json:
                schema:
                  type: object
          '400':
            description: Invalid request payload.
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
    logger.debug("Making POST request to /api/v1/applicationsets/generate")
    params = {}
    data = None

    # Add parameters to request
    if body is not None:
        data = body

    success, response = await make_api_request(
        "/api/v1/applicationsets/generate",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
