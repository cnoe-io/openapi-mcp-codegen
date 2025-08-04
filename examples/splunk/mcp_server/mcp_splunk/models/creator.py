"""Model for Creator"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Creator(BaseModel):
  """User ID of team creator. This field is read-only, and the system always sets the value."""


class CreatorResponse(APIResponse):
  """Response model for Creator"""

  data: Optional[Creator] = None


class CreatorListResponse(APIResponse):
  """List response model for Creator"""

  data: List[Creator] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
