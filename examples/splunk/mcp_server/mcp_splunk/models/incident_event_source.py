"""Model for Incidenteventsource"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Incidenteventsource(BaseModel):
  """Value that matched a detector rule and triggered an incident"""


class IncidenteventsourceResponse(APIResponse):
  """Response model for Incidenteventsource"""

  data: Optional[Incidenteventsource] = None


class IncidenteventsourceListResponse(APIResponse):
  """List response model for Incidenteventsource"""

  data: List[Incidenteventsource] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
