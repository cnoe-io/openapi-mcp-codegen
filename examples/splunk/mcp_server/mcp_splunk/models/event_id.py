"""Model for Eventid"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Eventid(BaseModel):
  """ID of the event. Set by system."""


class EventidResponse(APIResponse):
  """Response model for Eventid"""

  data: Optional[Eventid] = None


class EventidListResponse(APIResponse):
  """List response model for Eventid"""

  data: List[Eventid] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
