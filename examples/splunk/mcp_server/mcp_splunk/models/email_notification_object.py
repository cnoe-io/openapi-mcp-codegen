"""Model for Emailnotificationobject"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Emailnotificationobject(BaseModel):
  """Email notification properties"""


class EmailnotificationobjectResponse(APIResponse):
  """Response model for Emailnotificationobject"""

  data: Optional[Emailnotificationobject] = None


class EmailnotificationobjectListResponse(APIResponse):
  """List response model for Emailnotificationobject"""

  data: List[Emailnotificationobject] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
