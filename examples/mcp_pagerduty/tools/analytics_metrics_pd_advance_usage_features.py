"""Tools for /analytics/metrics/pd_advance_usage/features operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getAnalyticsMetricsPdAdvanceUsageFeatures() -> Dict[str, Any]:
    """
    Get aggregated PD Advance usage data

    Provides aggregated metrics for the usage of PD Advance.
<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /analytics/metrics/pd_advance_usage/features")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/analytics/metrics/pd_advance_usage/features",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
