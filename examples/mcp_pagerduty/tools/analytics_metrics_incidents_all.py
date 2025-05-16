"""Tools for /analytics/metrics/incidents/all operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getAnalyticsMetricsIncidentsAll() -> Dict[str, Any]:
    """
    Get aggregated incident data

    Provides aggregated enriched metrics for incidents.

The provided metrics are aggregated by day, week, month using the aggregate_unit parameter, or for the entire period if no aggregate_unit is provided.

<!-- theme: info -->
> A `team_ids` or `service_ids` filter is required for [user-level API keys](https://support.pagerduty.com/docs/using-the-api#section-generating-a-personal-rest-api-key) or keys generated through an OAuth flow. Account-level API keys do not have this requirement.
<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /analytics/metrics/incidents/all")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/analytics/metrics/incidents/all",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
