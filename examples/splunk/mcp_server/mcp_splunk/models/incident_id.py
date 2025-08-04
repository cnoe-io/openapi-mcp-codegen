"""Model for Incidentid"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Incidentid(BaseModel):
  """ID of an incident. Set by system."""


class IncidentidResponse(APIResponse):
  """Response model for Incidentid"""

  data: Optional[Incidentid] = None


class IncidentidListResponse(APIResponse):
  """List response model for Incidentid"""

  data: List[Incidentid] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
