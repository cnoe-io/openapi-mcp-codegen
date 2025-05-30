
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/certificates operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def certificateservice_listcertificates(hostNamePattern: str = None, certType: str = None, certSubType: str = None) -> Dict[str, Any]:
    '''
    List all available repository certificates.

    Args:
        hostNamePattern (str, optional): Pattern to filter certificates by host name. Defaults to None.
        certType (str, optional): Type of certificate to filter by. Defaults to None.
        certSubType (str, optional): Subtype of certificate to filter by. Defaults to None.

    Returns:
        Dict[str, Any]: A dictionary containing the list of certificates or an error message.

    Raises:
        Exception: If the API request fails due to network issues or invalid responses.

    OpenAPI Specification:
      get:
        summary: List all available repository certificates
        operationId: certificateservice_listcertificates
        parameters:
          - in: query
            name: hostNamePattern
            schema:
              type: string
            required: false
            description: Pattern to filter certificates by host name.
          - in: query
            name: certType
            schema:
              type: string
            required: false
            description: Type of certificate to filter by.
          - in: query
            name: certSubType
            schema:
              type: string
            required: false
            description: Subtype of certificate to filter by.
        responses:
          '200':
            description: A list of available repository certificates.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    certificates:
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
    logger.debug("Making GET request to /api/v1/certificates")
    params = {}
    data = None

    success, response = await make_api_request(
        "/api/v1/certificates",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response


async def certificateservice_createcertificate(body: str, upsert: str = None) -> Dict[str, Any]:
    '''
    Creates repository certificates on the server.

    Args:
        body (str): The certificate data to be created, typically in JSON or PEM format.
        upsert (str, optional): If provided, indicates whether to update the certificate if it already exists. Defaults to None.

    Returns:
        Dict[str, Any]: The response from the server, including certificate details or error information.

    Raises:
        Exception: If the API request fails or returns an unexpected error.

    OpenAPI Specification:
      post:
        summary: Creates repository certificates on the server.
        operationId: certificateservice_createcertificate
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: string
              example: |
                {
                  "certificate": "-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----"
                }
        parameters:
          - in: query
            name: upsert
            schema:
              type: string
            required: false
            description: If provided, updates the certificate if it already exists.
        responses:
          '200':
            description: Certificate created successfully.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    certificateId:
                      type: string
                      description: The unique identifier of the created certificate.
                    status:
                      type: string
                      description: Status of the operation.
          '400':
            description: Invalid request or certificate data.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      description: Error message.
          '500':
            description: Server error.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    error:
                      type: string
                      description: Error message.
    '''
    logger.debug("Making POST request to /api/v1/certificates")
    params = {}
    data = None

    # Add parameters to request
    if body is not None:
        data = body

    success, response = await make_api_request(
        "/api/v1/certificates",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response


async def certificateservice_deletecertificate(hostNamePattern: str = None, certType: str = None, certSubType: str = None) -> Dict[str, Any]:
    '''
    Delete certificates matching the specified query parameters.

    Args:
        hostNamePattern (str, optional): Pattern to match the host name of certificates to delete. Defaults to None.
        certType (str, optional): Type of the certificate to delete. Defaults to None.
        certSubType (str, optional): Subtype of the certificate to delete. Defaults to None.

    Returns:
        Dict[str, Any]: Response from the API indicating the result of the delete operation.

    Raises:
        Exception: If the API request fails or returns an error.

    OpenAPI Specification:
      delete:
        summary: Delete certificates matching the specified query parameters.
        operationId: certificateservice_deletecertificate
        parameters:
          - in: query
            name: hostNamePattern
            schema:
              type: string
            required: false
            description: Pattern to match the host name of certificates to delete.
          - in: query
            name: certType
            schema:
              type: string
            required: false
            description: Type of the certificate to delete.
          - in: query
            name: certSubType
            schema:
              type: string
            required: false
            description: Subtype of the certificate to delete.
        responses:
          '200':
            description: Certificates deleted successfully.
            content:
              application/json:
                schema:
                  type: object
          '400':
            description: Invalid request parameters.
            content:
              application/json:
                schema:
                  type: object
          '500':
            description: Internal server error.
            content:
              application/json:
                schema:
                  type: object
        tags:
          - Certificates
    '''
    logger.debug("Making DELETE request to /api/v1/certificates")
    params = {}
    data = None

    success, response = await make_api_request(
        "/api/v1/certificates",
        method="DELETE",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
