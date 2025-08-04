"""Tools for /alertmuting operations"""

import logging
from typing import Any, List
from mcp_splunk.api.client import make_api_request, assemble_nested_body

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def retrieve__muting__rules__using__query(
  param_include: str = None, param_limit: int = None, param_offset: int = None, param_order_by: str = None, param_query: str = None
) -> Any:
  """
  Retrieves muting rules based on search criteria

  OpenAPI Description:
      Retrieves notification muting rules based on query parameters


  Args:

      param_include (str): Type of muting rules you want to retrieve


      param_limit (int): Number of results to return from the result set


      param_offset (int): Index in the result set from which the API starts returning results


      param_order_by (str): Metadata property on which the API sorts the results


      param_query (str): Query that specifies the muting rules you want to retrieve



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making GET request to /alertmuting")

  params = {}
  data = {}

  if param_include is not None:
    params["include"] = str(param_include).lower() if isinstance(param_include, bool) else param_include

  if param_limit is not None:
    params["limit"] = str(param_limit).lower() if isinstance(param_limit, bool) else param_limit

  if param_offset is not None:
    params["offset"] = str(param_offset).lower() if isinstance(param_offset, bool) else param_offset

  if param_order_by is not None:
    params["order_by"] = str(param_order_by).lower() if isinstance(param_order_by, bool) else param_order_by

  if param_query is not None:
    params["query"] = str(param_query).lower() if isinstance(param_query, bool) else param_query

  flat_body = {}
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request("/alertmuting", method="GET", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response


async def create__single__muting__rule(
  param_resolveMatchingActiveAlerts: bool = False,
  body_created: int = None,
  body_creator: str = None,
  body_description: str = None,
  body_filters: List[str] = None,
  body_id: str = None,
  body_lastUpdated: int = None,
  body_lastUpdatedBy: str = None,
  body_recurrence_unit: str = None,
  body_recurrence_value: int = None,
  body_linkedTeams: List[str] = None,
  body_sendAlertsOnceMutingPeriodHasEnded: bool = None,
  body_startTime: int = None,
  body_stopTime: int = None,
) -> Any:
  """
  Creates a new muting rule

  OpenAPI Description:
      Creates a new notification muting rule


  Args:

      param_resolveMatchingActiveAlerts (bool): Indicates that Splunk Observability Cloud should resolve alerts for the matched rules


      body_created (int): Team creation time, in *nix format. This field is read-only, and the system always sets the value.


      body_creator (str): User ID of team creator. This field is read-only, and the system always sets the value.


      body_description (str): Description of the muting rule


      body_filters (List[str]): List of muting filters for this rule


      body_id (str): ID of a muting rule. Set by system.


      body_lastUpdated (int): Team last updated time, in *nix format. This field is read-only, and the system always sets the value.


      body_lastUpdatedBy (str): ID of user who last updated the chart. This field is read-only, and the system always sets the value.


      body_recurrence_unit (str): Unit of the period. Can be days (`d`) or weeks (`w`)

      body_recurrence_value (int): Amount of time, expressed as an integer applicable to the unit


      body_linkedTeams (List[str]): IDs of teams linked to the detector that created the incident. If the incident is created by a detector that is not linked to a team, the value is `null`. This is a JSON array of strings, where each string is a team ID. This property is read-only; it's always set by the system. For information about how to link detectors to teams, see [Detectors linked to teams](https://quickdraw.splunk.com/redirect/?product=Observability&location=devdocs.getincidents.byteamid&version=current).


      body_sendAlertsOnceMutingPeriodHasEnded (bool): Controls notifications after the muting period ends


      body_startTime (int): Starting timestamp of a muting rule, in *nix time in milliseconds


      body_stopTime (int): Ending timestamp of a muting rule, in *nix time in milliseconds



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making POST request to /alertmuting")

  params = {}
  data = {}

  if param_resolveMatchingActiveAlerts is not None:
    params["resolveMatchingActiveAlerts"] = (
      str(param_resolveMatchingActiveAlerts).lower()
      if isinstance(param_resolveMatchingActiveAlerts, bool)
      else param_resolveMatchingActiveAlerts
    )

  flat_body = {}
  if body_created is not None:
    flat_body["created"] = body_created
  if body_creator is not None:
    flat_body["creator"] = body_creator
  if body_description is not None:
    flat_body["description"] = body_description
  if body_filters is not None:
    flat_body["filters"] = body_filters
  if body_id is not None:
    flat_body["id"] = body_id
  if body_lastUpdated is not None:
    flat_body["lastUpdated"] = body_lastUpdated
  if body_lastUpdatedBy is not None:
    flat_body["lastUpdatedBy"] = body_lastUpdatedBy
  if body_recurrence_unit is not None:
    flat_body["recurrence_unit"] = body_recurrence_unit
  if body_recurrence_value is not None:
    flat_body["recurrence_value"] = body_recurrence_value
  if body_linkedTeams is not None:
    flat_body["linkedTeams"] = body_linkedTeams
  if body_sendAlertsOnceMutingPeriodHasEnded is not None:
    flat_body["sendAlertsOnceMutingPeriodHasEnded"] = body_sendAlertsOnceMutingPeriodHasEnded
  if body_startTime is not None:
    flat_body["startTime"] = body_startTime
  if body_stopTime is not None:
    flat_body["stopTime"] = body_stopTime
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request("/alertmuting", method="POST", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response
