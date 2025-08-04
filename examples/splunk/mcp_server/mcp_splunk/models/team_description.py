"""Model for Teamdescription"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Teamdescription(BaseModel):
  """Team description"""


class TeamdescriptionResponse(APIResponse):
  """Response model for Teamdescription"""

  data: Optional[Teamdescription] = None


class TeamdescriptionListResponse(APIResponse):
  """List response model for Teamdescription"""

  data: List[Teamdescription] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
