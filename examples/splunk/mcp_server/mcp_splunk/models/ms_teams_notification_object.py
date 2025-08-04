"""Model for Msteamsnotificationobject"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Msteamsnotificationobject(BaseModel):
  """Properties of a Microsoft Teams notification service integration"""


class MsteamsnotificationobjectResponse(APIResponse):
  """Response model for Msteamsnotificationobject"""

  data: Optional[Msteamsnotificationobject] = None


class MsteamsnotificationobjectListResponse(APIResponse):
  """List response model for Msteamsnotificationobject"""

  data: List[Msteamsnotificationobject] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
