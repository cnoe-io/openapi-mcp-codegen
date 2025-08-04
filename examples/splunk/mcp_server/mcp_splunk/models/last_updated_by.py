"""Model for Lastupdatedby"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Lastupdatedby(BaseModel):
  """ID of user who last updated the chart. This field is read-only, and the system always sets the value."""


class LastupdatedbyResponse(APIResponse):
  """Response model for Lastupdatedby"""

  data: Optional[Lastupdatedby] = None


class LastupdatedbyListResponse(APIResponse):
  """List response model for Lastupdatedby"""

  data: List[Lastupdatedby] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
