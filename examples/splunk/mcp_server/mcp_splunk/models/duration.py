"""Model for Duration"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Duration(BaseModel):
  """Duration of the incident in milliseconds"""


class DurationResponse(APIResponse):
  """Response model for Duration"""

  data: Optional[Duration] = None


class DurationListResponse(APIResponse):
  """List response model for Duration"""

  data: List[Duration] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
