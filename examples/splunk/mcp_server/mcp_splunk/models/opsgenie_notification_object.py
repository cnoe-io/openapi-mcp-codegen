"""Model for Opsgenienotificationobject"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Opsgenienotificationobject(BaseModel):
  """Notification properties for an Opsgenie notification integration"""


class OpsgenienotificationobjectResponse(APIResponse):
  """Response model for Opsgenienotificationobject"""

  data: Optional[Opsgenienotificationobject] = None


class OpsgenienotificationobjectListResponse(APIResponse):
  """List response model for Opsgenienotificationobject"""

  data: List[Opsgenienotificationobject] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
