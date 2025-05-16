"""Tools for /rulesets operations"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from ..api.client import make_api_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def listRulesets() -> Dict[str, Any]:
    """
    List Rulesets

    List all Rulesets
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Scoped OAuth requires: `event_rules.read`


    Returns:
        API response data
    """
    logger.debug(f"Making GET request to /rulesets")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/rulesets",
        method="GET",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response

async def createRuleset() -> Dict[str, Any]:
    """
    Create a Ruleset

    Create a new Ruleset.
<!-- theme: warning -->
> ### End-of-life
> Rulesets and Event Rules will end-of-life soon. We highly recommend that you [migrate to Event Orchestration](https://support.pagerduty.com/docs/migrate-to-event-orchestration) as soon as possible so you can take advantage of the new functionality, such as improved UI, rule creation, APIs and Terraform support, advanced conditions, and rule nesting.

Rulesets allow you to route events to an endpoint and create collections of Event Rules, which define sets of actions to take based on event content.

For more information see the [API Concepts Document](../../api-reference/ZG9jOjI3NDc5Nzc-api-concepts#rulesets)

Scoped OAuth requires: `event_rules.write`


    Returns:
        API response data
    """
    logger.debug(f"Making POST request to /rulesets")
    params = {}
    data = None
    # Add parameters to request
    
    success, response = await make_api_request(
        "/rulesets",
        method="POST",
        params=params,
        data=data
    )
    if not success:
        logger.error(f"Request failed: {response.get('error')}")
        return {"error": response.get('error', 'Request failed')}
    return response
