"""Model for Teammembersarray"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Teammembersarray(BaseModel):
  """List of user IDs that belong to a team"""


class TeammembersarrayResponse(APIResponse):
  """Response model for Teammembersarray"""

  data: Optional[Teammembersarray] = None


class TeammembersarrayListResponse(APIResponse):
  """List response model for Teammembersarray"""

  data: List[Teammembersarray] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
