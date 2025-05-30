
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/applications operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def applicationservice_list(name: str = None, refresh: str = None, projects: str = None, resourceVersion: str = None, selector: str = None, repo: str = None, appNamespace: str = None, project: str = None) -> Dict[str, Any]:
    '''
    Retrieves a list of applications with optional filtering parameters.

    Args:
        name (str, optional): Filter applications by name. Defaults to None.
        refresh (str, optional): If set, refreshes application data before listing. Defaults to None.
        projects (str, optional): Comma-separated list of project names to filter applications. Defaults to None.
        resourceVersion (str, optional): Filter by resource version. Defaults to None.
        selector (str, optional): Label selector to filter applications. Defaults to None.
        repo (str, optional): Filter applications by repository URL. Defaults to None.
        appNamespace (str, optional): Filter applications by namespace. Defaults to None.
        project (str, optional): Filter applications by project name. Defaults to None.

    Returns:
        Dict[str, Any]: A dictionary containing the list of applications or an error message.

    Raises:
        Exception: If the API request fails or returns an error.

    OpenAPI Specification:
      get:
        summary: List applications
        description: Retrieve a list of applications with optional filtering parameters.
        operationId: applicationservice_list
        parameters:
          - in: query
            name: name
            schema:
              type: string
            description: Filter applications by name.
          - in: query
            name: refresh
            schema:
              type: string
            description: If set, refreshes application data before listing.
          - in: query
            name: projects
            schema:
              type: string
            description: Comma-separated list of project names to filter applications.
          - in: query
            name: resourceVersion
            schema:
              type: string
            description: Filter by resource version.
          - in: query
            name: selector
            schema:
              type: string
            description: Label selector to filter applications.
          - in: query
            name: repo
            schema:
              type: string
            description: Filter applications by repository URL.
          - in: query
            name: appNamespace
            schema:
              type: string
            description: Filter applications by namespace.
          - in: query
            name: project
            schema:
              type: string
            description: Filter applications by project name.
        responses:
          '200':
            description: A list of applications.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    items:
                      type: array
                      items:
                        type: object
          '400':
            description: Invalid request parameters.
          '500':
            description: Internal server error.
    '''
    logger.debug("Making GET request to /api/v1/applications")
    params = {}
    data = None

    success, response = await make_api_request(
        "/api/v1/applications",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response


async def applicationservice_create(body: str, upsert: str = None, validate: str = None) -> Dict[str, Any]:
    '''
    Creates a new application.

    Args:
        body (str): The JSON string representing the application to create.
        upsert (str, optional): If set, allows upserting the application. Defaults to None.
        validate (str, optional): If set, validates the application without persisting. Defaults to None.

    Returns:
        Dict[str, Any]: The response from the API, including the created application details or an error message.

    Raises:
        Exception: If the API request fails or returns an unexpected error.

    OpenAPI Specification:
      post:
        summary: Create a new application
        operationId: applicationservice_create
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: string
        parameters:
          - in: query
            name: upsert
            schema:
              type: string
            required: false
            description: If set, allows upserting the application.
          - in: query
            name: validate
            schema:
              type: string
            required: false
            description: If set, validates the application without persisting.
        responses:
          '200':
            description: Application created successfully
            content:
              application/json:
                schema:
                  type: object
          '400':
            description: Invalid request or validation error
            content:
              application/json:
                schema:
                  type: object
          '500':
            description: Internal server error
            content:
              application/json:
                schema:
                  type: object
    '''
    logger.debug("Making POST request to /api/v1/applications")
    params = {}
    data = None

    # Add parameters to request
    if body is not None:
        data = body

    success, response = await make_api_request(
        "/api/v1/applications",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
