"""Model for Alertmutingfilter"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Alertmutingfilter(BaseModel):
  """Muting filter for a rule"""


class AlertmutingfilterResponse(APIResponse):
  """Response model for Alertmutingfilter"""

  data: Optional[Alertmutingfilter] = None


class AlertmutingfilterListResponse(APIResponse):
  """List response model for Alertmutingfilter"""

  data: List[Alertmutingfilter] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
