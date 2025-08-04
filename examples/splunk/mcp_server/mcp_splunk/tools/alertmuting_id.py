"""Tools for /alertmuting/{id} operations"""

import logging
from typing import Any, List
from mcp_splunk.api.client import make_api_request, assemble_nested_body

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_tools")


async def retrieve__muting__rule_id(path_id: str) -> Any:
  """
  Retrieves the muting rule specified in the {id} path parameter

  OpenAPI Description:
      Retrieves a muting rule


  Args:

      path_id (str): ID of the muting rule you want



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making GET request to /alertmuting/{id}")

  params = {}
  data = {}

  flat_body = {}
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request(f"/alertmuting/{path_id}", method="GET", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response


async def update__single__muting__rule(
  path_id: str,
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
  Updates a muting rule

  OpenAPI Description:
      Updates a muting rule


  Args:

      path_id (str): ID of the muting rule you want to modify


      param_resolveMatchingActiveAlerts (bool): Indicates that you want Splunk Observability Cloud to resolve alerts for the rule


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
  logger.debug("Making PUT request to /alertmuting/{id}")

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

  success, response = await make_api_request(f"/alertmuting/{path_id}", method="PUT", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response


async def delete__single__muting__rule(path_id: str) -> Any:
  """
  Deletes a muting rule specified in the {id} path parameter

  OpenAPI Description:
      Deletes a muting rule


  Args:

      path_id (str): ID of the muting rule you want to delete



  Returns:
      Any: The JSON response from the API call.

  Raises:
      Exception: If the API request fails or returns an error.
  """
  logger.debug("Making DELETE request to /alertmuting/{id}")

  params = {}
  data = {}

  flat_body = {}
  data = assemble_nested_body(flat_body)

  success, response = await make_api_request(f"/alertmuting/{path_id}", method="DELETE", params=params, data=data)

  if not success:
    logger.error(f"Request failed: {response.get('error')}")
    return {"error": response.get("error", "Request failed")}
  return response
