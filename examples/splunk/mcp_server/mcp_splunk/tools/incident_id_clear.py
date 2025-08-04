"""Tools for /incident/{id}/clear operations"""

import logging
from typing import Any
from mcp_splunk.api.client import make_api_request, assemble_nested_body

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def clear__single__incident(path_id: str) -> Any:
  """
  Clears an incident specified by the `{id}`path parameter

  OpenAPI Description:
      Clears an incident


  Args:

      path_id (str): ID of the incident you want to clear



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making PUT request to /incident/{id}/clear")

  params = {}
  data = {}

  flat_body = {}
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request(f"/incident/{path_id}/clear", method="PUT", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response
