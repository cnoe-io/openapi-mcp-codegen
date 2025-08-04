"""Model for Teamrequestbody"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Teamrequestbody(BaseModel):
  """Request body"""


class TeamrequestbodyResponse(APIResponse):
  """Response model for Teamrequestbody"""

  data: Optional[Teamrequestbody] = None


class TeamrequestbodyListResponse(APIResponse):
  """List response model for Teamrequestbody"""

  data: List[Teamrequestbody] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
