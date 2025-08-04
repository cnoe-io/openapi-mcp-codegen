"""Model for Alertmutingrule"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Alertmutingrule(BaseModel):
  """Properties of a muting rule"""


class AlertmutingruleResponse(APIResponse):
  """Response model for Alertmutingrule"""

  data: Optional[Alertmutingrule] = None


class AlertmutingruleListResponse(APIResponse):
  """List response model for Alertmutingrule"""

  data: List[Alertmutingrule] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
