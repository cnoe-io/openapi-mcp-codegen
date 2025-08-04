"""Tools for /incident operations"""

import logging
from typing import Any
from mcp_splunk.api.client import make_api_request, assemble_nested_body

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def retrieve__incidents(
  param_includeResolved: bool = False, param_limit: int = None, param_offset: int = None, param_query: str = None
) -> Any:
  """
      Retrieves information for the latest incidents in an organization

      OpenAPI Description:
          Retrieves the latest incidents in an organization


      Args:

          param_includeResolved (bool): Controls retrieval of the latest resolved incidents


          param_limit (int): Number of results to return from the result set


          param_offset (int): Index in result set at which the API starts returning results


          param_query (str): Controls which latest incidents to retrieve, based on descriptions and other filters. For example, to retrieve the latest incidents created by detectors linked to a team with the ID `FO1Vq3ABXYZ`, specify `teamId:FO1Vq3ABXYZ`.

  To search for latest incidents by specific values of a dimension or custom property, use `query=<name>:<value>`. If `<value>` contains non-alphanumeric characters, encode the non-alphanumeric characters and surround the value with double quotes. For example, the region custom property value `US East` must be passed in the parameter as `region:"US%20East"`.

  Here are examples of the `query` parameter used alone and with other available query parameters:

  - `https://app.{realm}.signalfx.com/v2/incident?query=teamId:FO1Vq3ABXYZ`
  - `https://app.{realm}.signalfx.com/v2/incident?query=region:"US%20East"&limit=5&offset=5`

  For information about how to link detectors to teams, see [Detectors linked to teams](https://quickdraw.splunk.com/redirect/?product=Observability&location=devdocs.getincidents.byteamid&version=current).



      Returns:
          Any: The JSON response from the API call.

      Raises:
          Exception: If the API request fails or returns an error.
  """
  logger.debug("Making GET request to /incident")

  params = {}
  data = {}

  if param_includeResolved is not None:
    params["includeResolved"] = str(param_includeResolved).lower() if isinstance(param_includeResolved, bool) else param_includeResolved

  if param_limit is not None:
    params["limit"] = str(param_limit).lower() if isinstance(param_limit, bool) else param_limit

  if param_offset is not None:
    params["offset"] = str(param_offset).lower() if isinstance(param_offset, bool) else param_offset

  if param_query is not None:
    params["query"] = str(param_query).lower() if isinstance(param_query, bool) else param_query

  flat_body = {}
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request("/incident", method="GET", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response
