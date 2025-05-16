"""Tools for /analytics/metrics/incidents/services operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getAnalyticsMetricsIncidentsService() -> Dict[str, Any]:
    """
    Get aggregated service data

    Provides aggregated metrics for incidents aggregated into units of time by service.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#services-list).
Data can be aggregated by day, week or month in addition to by service, or provided just as a collection of aggregates for each service in the dataset for the entire period.  If a unit is provided, each row in the returned dataset will include a 'range_start' timestamp.

<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /analytics/metrics/incidents/services")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/analytics/metrics/incidents/services",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
