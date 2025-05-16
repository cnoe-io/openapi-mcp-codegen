"""Tools for /analytics/metrics/incidents/escalation_policies operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getAnalyticsMetricsIncidentsEscalationPolicy() -> Dict[str, Any]:
    """
    Get aggregated escalation policy data

    Provides aggregated metrics for incidents aggregated into units of time by escalation policy.

Example metrics include Seconds to Resolve, Seconds to Engage, Snoozed Seconds, and Sleep Hour Interruptions. Metric definitions can be found in our [Knowledge Base](https://support.pagerduty.com/docs/insights#escalation-policy-list).

<!-- theme: info -->
> **Note:** Analytics data is updated [periodically](https://support.pagerduty.com/main/docs/insights#:~:text=Data%20Update%20Schedule). It takes up to 24 hours before new incidents appear in the Analytics API.

Scoped OAuth requires: `analytics.read`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /analytics/metrics/incidents/escalation_policies")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/analytics/metrics/incidents/escalation_policies",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
