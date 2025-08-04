"""Tools for /incident/clear operations"""

import logging
from typing import Any, List
from mcp_splunk.api.client import make_api_request, assemble_nested_body

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def clear__incidents(body_filters: List[str] = None) -> Any:
  """
  Clears specified incidents

  OpenAPI Description:
      Clears alerts specified in the request body


  Args:

      body_filters (List[str]): List of rules that identify incidents



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making PUT request to /incident/clear")

  params = {}
  data = {}

  flat_body = {}
  if body_filters is not None:
    flat_body["filters"] = body_filters
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request("/incident/clear", method="PUT", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response
