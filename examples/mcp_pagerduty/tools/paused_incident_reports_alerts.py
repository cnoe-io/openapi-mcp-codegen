"""Tools for /paused_incident_reports/alerts operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def getPausedIncidentReportAlerts() -> Dict[str, Any]:
    """
    Get Paused Incident Reporting on Alerts

    Returns the 5 most recent alerts that were triggered after being paused and the 5 most recent alerts that were resolved after being paused for a given reporting period (maximum 6 months lookback period).  Note: This feature is currently available as part of the Event Intelligence package or Digital Operations plan only.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#paused-incident-reports)

Scoped OAuth requires: `incidents.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /paused_incident_reports/alerts")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/paused_incident_reports/alerts",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
