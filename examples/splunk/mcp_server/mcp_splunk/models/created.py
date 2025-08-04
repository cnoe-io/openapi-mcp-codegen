"""Model for Created"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Created(BaseModel):
  """Team creation time, in *nix format. This field is read-only, and the system always sets the value."""


class CreatedResponse(APIResponse):
  """Response model for Created"""

  data: Optional[Created] = None


class CreatedListResponse(APIResponse):
  """List response model for Created"""

  data: List[Created] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
