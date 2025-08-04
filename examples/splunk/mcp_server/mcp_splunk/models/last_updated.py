"""Model for Lastupdated"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Lastupdated(BaseModel):
  """Team last updated time, in *nix format. This field is read-only, and the system always sets the value."""


class LastupdatedResponse(APIResponse):
  """Response model for Lastupdated"""

  data: Optional[Lastupdated] = None


class LastupdatedListResponse(APIResponse):
  """List response model for Lastupdated"""

  data: List[Lastupdated] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
