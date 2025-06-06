
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
    """
    List all available repository certificates
    """
    logger.debug("Making GET request to /api/v1/certificates")
    params = {}
    
    if hostNamePattern is not None:
      params["hostNamePattern"] = hostNamePattern
    
    if certType is not None:
      params["certType"] = certType
    
    if certSubType is not None:
      params["certSubType"] = certSubType
    
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
    """
    Creates repository certificates on the server
    """
    logger.debug("Making POST request to /api/v1/certificates")
    params = {}
    
    if body is not None:
      params["body"] = body
    
    if upsert is not None:
      params["upsert"] = upsert
    
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
    """
    Delete the certificates that match the RepositoryCertificateQuery
    """
    logger.debug("Making DELETE request to /api/v1/certificates")
    params = {}
    
    if hostNamePattern is not None:
      params["hostNamePattern"] = hostNamePattern
    
    if certType is not None:
      params["certType"] = certType
    
    if certSubType is not None:
      params["certSubType"] = certSubType
    
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

