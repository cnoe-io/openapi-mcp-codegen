"""Model for Pagerdutynotificationobject"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Pagerdutynotificationobject(BaseModel):
  """Properties of a PagerDuty notification service integration"""


class PagerdutynotificationobjectResponse(APIResponse):
  """Response model for Pagerdutynotificationobject"""

  data: Optional[Pagerdutynotificationobject] = None


class PagerdutynotificationobjectListResponse(APIResponse):
  """List response model for Pagerdutynotificationobject"""

  data: List[Pagerdutynotificationobject] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
