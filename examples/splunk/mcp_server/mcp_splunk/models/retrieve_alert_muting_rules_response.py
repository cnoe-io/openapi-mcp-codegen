"""Model for Retrievealertmutingrulesresponse"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Retrievealertmutingrulesresponse(BaseModel):
  """Properties of the notification muting rule retrieval object"""


class RetrievealertmutingrulesresponseResponse(APIResponse):
  """Response model for Retrievealertmutingrulesresponse"""

  data: Optional[Retrievealertmutingrulesresponse] = None


class RetrievealertmutingrulesresponseListResponse(APIResponse):
  """List response model for Retrievealertmutingrulesresponse"""

  data: List[Retrievealertmutingrulesresponse] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
