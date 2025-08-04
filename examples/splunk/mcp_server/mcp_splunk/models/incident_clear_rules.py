"""Model for Incidentclearrules"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Incidentclearrules(BaseModel):
  """Rules that identify incidents you want to clear"""


class IncidentclearrulesResponse(APIResponse):
  """Response model for Incidentclearrules"""

  data: Optional[Incidentclearrules] = None


class IncidentclearrulesListResponse(APIResponse):
  """List response model for Incidentclearrules"""

  data: List[Incidentclearrules] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
