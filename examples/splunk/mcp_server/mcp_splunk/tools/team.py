"""Tools for /team operations"""

import logging
from typing import Any, List
from mcp_splunk.api.client import make_api_request, assemble_nested_body

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def retrieve__teams_by__name(
  param_limit: int = None, param_offset: float = None, param_name: str = None, param_order_by: str = None
) -> Any:
  """
  Retrieves teams using a name search

  OpenAPI Description:
      Retrieves teams using a name search


  Args:

      param_limit (int): Number of results to return


      param_offset (float): Index in result set at which the API should start returning results


      param_name (str): Team name filter


      param_order_by (str): Property on which the API should sort results



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making GET request to /team")

  params = {}
  data = {}

  if param_limit is not None:
    params["limit"] = str(param_limit).lower() if isinstance(param_limit, bool) else param_limit

  if param_offset is not None:
    params["offset"] = str(param_offset).lower() if isinstance(param_offset, bool) else param_offset

  if param_name is not None:
    params["name"] = str(param_name).lower() if isinstance(param_name, bool) else param_name

  if param_order_by is not None:
    params["order_by"] = str(param_order_by).lower() if isinstance(param_order_by, bool) else param_order_by

  flat_body = {}
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request("/team", method="GET", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response


async def create__single__team(
  body_description: str = None,
  body_members: List[str] = None,
  body_name: str = None,
  body_notificationLists_default: List[str] = None,
  body_notificationLists_critical: List[str] = None,
  body_notificationLists_warning: List[str] = None,
  body_notificationLists_major: List[str] = None,
  body_notificationLists_minor: List[str] = None,
  body_notificationLists_info: List[str] = None,
) -> Any:
  """
  Creates a team

  OpenAPI Description:
      Creates a team


  Args:

      body_description (str): Team description


      body_members (List[str]): List of user IDs that belong to a team


      body_name (str): Team name


      body_notificationLists_default (List[str]): Notification services to use for undefined alerts


      body_notificationLists_critical (List[str]): Notification services to use for critical alerts


      body_notificationLists_warning (List[str]): Notification services to use for warning alerts


      body_notificationLists_major (List[str]): Notification services to use for major alerts


      body_notificationLists_minor (List[str]): Notification services to use for minor alerts


      body_notificationLists_info (List[str]): Notification services to use for information alerts



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making POST request to /team")

  params = {}
  data = {}

  flat_body = {}
  if body_description is not None:
    flat_body["description"] = body_description
  if body_members is not None:
    flat_body["members"] = body_members
  if body_name is not None:
    flat_body["name"] = body_name
  if body_notificationLists_default is not None:
    flat_body["notificationLists_default"] = body_notificationLists_default
  if body_notificationLists_critical is not None:
    flat_body["notificationLists_critical"] = body_notificationLists_critical
  if body_notificationLists_warning is not None:
    flat_body["notificationLists_warning"] = body_notificationLists_warning
  if body_notificationLists_major is not None:
    flat_body["notificationLists_major"] = body_notificationLists_major
  if body_notificationLists_minor is not None:
    flat_body["notificationLists_minor"] = body_notificationLists_minor
  if body_notificationLists_info is not None:
    flat_body["notificationLists_info"] = body_notificationLists_info
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request("/team", method="POST", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response
