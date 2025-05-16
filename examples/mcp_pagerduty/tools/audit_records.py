"""Tools for /audit/records operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listAuditRecords() -> Dict[str, Any]:
    """
    List audit records

    List audit trail records matching provided query params or default criteria.

The returned records are sorted by the `execution_time` from newest to oldest.

See [`Cursor-based pagination`](https://developer.pagerduty.com/docs/rest-api-v2/pagination/) for instructions on how to paginate through the result set.

Only admins, account owners, or global API tokens on PagerDuty account [pricing plans](https://www.pagerduty.com/pricing) with the "Audit Trail" feature can access this endpoint.

For other role based access to audit records by resource ID, see the resource's API documentation.

For more information see the [Audit API Document](https://developer.pagerduty.com/docs/rest-api-v2/audit-records-api/).

Scoped OAuth requires: `audit_records.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /audit/records")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/audit/records",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
