
# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0
# Generated by CNOE OpenAPI MCP Codegen tool

"""Tools for /api/v1/stream/applications operations"""

import logging
from typing import Dict, Any
from agent_argocd.protocol_bindings.mcp_server.mcp_argocd.api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def applicationservice_watch(name: str = None, refresh: str = None, projects: str = None, resourceVersion: str = None, selector: str = None, repo: str = None, appNamespace: str = None, project: str = None) -> Dict[str, Any]:
    """
    Watch returns stream of application change events
    """
    logger.debug("Making GET request to /api/v1/stream/applications")
    params = {}
    
    if name is not None:
      params["name"] = name
    
    if refresh is not None:
      params["refresh"] = refresh
    
    if projects is not None:
      params["projects"] = projects
    
    if resourceVersion is not None:
      params["resourceVersion"] = resourceVersion
    
    if selector is not None:
      params["selector"] = selector
    
    if repo is not None:
      params["repo"] = repo
    
    if appNamespace is not None:
      params["appNamespace"] = appNamespace
    
    if project is not None:
      params["project"] = project
    
    data = None

    success, response = await make_api_request(
        "/api/v1/stream/applications",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

