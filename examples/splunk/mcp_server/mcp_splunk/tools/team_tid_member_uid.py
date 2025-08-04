"""Tools for /team/{tid}/member/{uid} operations"""

import logging
from typing import Any
from mcp_splunk.api.client import make_api_request, assemble_nested_body

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def update__team__membership__user__id(path_tid: str, path_uid: str) -> Any:
  """
  Updates the team specified by {tid} by adding the user specified by {uid}


  OpenAPI Description:
      Updates a team by adding a user by ID


  Args:

      path_tid (str): Team ID


      path_uid (str): User ID



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making PUT request to /team/{tid}/member/{uid}")

  params = {}
  data = {}

  flat_body = {}
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request(f"/team/{path_tid}/member/{path_uid}", method="PUT", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response


async def delete__team__user__user__id(path_tid: str, path_uid: str) -> Any:
  """
  Deletes the user specified by {uid} from the team specified by {tid}


  OpenAPI Description:
      Deletes a user from a team


  Args:

      path_tid (str): Team ID


      path_uid (str): User ID



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making DELETE request to /team/{tid}/member/{uid}")

  params = {}
  data = {}

  flat_body = {}
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request(f"/team/{path_tid}/member/{path_uid}", method="DELETE", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response
