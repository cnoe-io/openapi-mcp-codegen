"""Model for Starttime"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Starttime(BaseModel):
  """Starting timestamp of a muting rule, in *nix time in milliseconds"""


class StarttimeResponse(APIResponse):
  """Response model for Starttime"""

  data: Optional[Starttime] = None


class StarttimeListResponse(APIResponse):
  """List response model for Starttime"""

  data: List[Starttime] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
