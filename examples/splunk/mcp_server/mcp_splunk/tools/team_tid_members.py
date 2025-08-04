"""Tools for /team/{tid}/members operations"""

import logging
from typing import Any, List
from mcp_splunk.api.client import make_api_request, assemble_nested_body

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def add__team__member__list(path_tid: str, body_members: List[str] = None) -> Any:
  """
  Adds team members

  OpenAPI Description:
      Adds new members to the team specified by the `{tid}` path parameter.


  Args:

      path_tid (str): Team ID


      body_members (List[str]): List of one or more Splunk Observability Cloud-assigned user IDs to add to the team



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making PUT request to /team/{tid}/members")

  params = {}
  data = {}

  flat_body = {}
  if body_members is not None:
    flat_body["members"] = body_members
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request(f"/team/{path_tid}/members", method="PUT", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response


async def delete__team__members__list(path_tid: str, body_members: List[str] = None) -> Any:
  """
  Deletes one or more members from a team

  OpenAPI Description:
      Deletes one or more members from the team specified by the {tid} path parameter


  Args:

      path_tid (str): Team ID


      body_members (List[str]): List of members



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making DELETE request to /team/{tid}/members")

  params = {}
  data = {}

  flat_body = {}
  if body_members is not None:
    flat_body["members"] = body_members
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request(f"/team/{path_tid}/members", method="DELETE", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response
