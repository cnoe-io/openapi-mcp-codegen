"""Model for Servicenownotificationobject"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Servicenownotificationobject(BaseModel):
  """Properties of a ServiceNow notification service integration"""


class ServicenownotificationobjectResponse(APIResponse):
  """Response model for Servicenownotificationobject"""

  data: Optional[Servicenownotificationobject] = None


class ServicenownotificationobjectListResponse(APIResponse):
  """List response model for Servicenownotificationobject"""

  data: List[Servicenownotificationobject] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
