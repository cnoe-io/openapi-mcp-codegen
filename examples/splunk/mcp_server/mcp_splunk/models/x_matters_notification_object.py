"""Model for Xmattersnotificationobject"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Xmattersnotificationobject(BaseModel):
  """Properties of a xMatters notification service integration"""


class XmattersnotificationobjectResponse(APIResponse):
  """Response model for Xmattersnotificationobject"""

  data: Optional[Xmattersnotificationobject] = None


class XmattersnotificationobjectListResponse(APIResponse):
  """List response model for Xmattersnotificationobject"""

  data: List[Xmattersnotificationobject] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
