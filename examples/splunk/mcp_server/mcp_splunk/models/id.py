"""Model for Id"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Id(BaseModel):
  """ID of a muting rule. Set by system."""


class IdResponse(APIResponse):
  """Response model for Id"""

  data: Optional[Id] = None


class IdListResponse(APIResponse):
  """List response model for Id"""

  data: List[Id] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
