"""Model for Teamnotificationlists"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Teamnotificationlists(BaseModel):
  """Team notification policy"""


class TeamnotificationlistsResponse(APIResponse):
  """Response model for Teamnotificationlists"""

  data: Optional[Teamnotificationlists] = None


class TeamnotificationlistsListResponse(APIResponse):
  """List response model for Teamnotificationlists"""

  data: List[Teamnotificationlists] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
