"""Model for Bigpandanotificationobject"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Bigpandanotificationobject(BaseModel):
  """Properties of a BigPanda notification service integration"""


class BigpandanotificationobjectResponse(APIResponse):
  """Response model for Bigpandanotificationobject"""

  data: Optional[Bigpandanotificationobject] = None


class BigpandanotificationobjectListResponse(APIResponse):
  """List response model for Bigpandanotificationobject"""

  data: List[Bigpandanotificationobject] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
