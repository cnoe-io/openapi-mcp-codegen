"""Model for Webhooknotificationobject"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Webhooknotificationobject(BaseModel):
  """Properties of a Webhook notification service integration"""


class WebhooknotificationobjectResponse(APIResponse):
  """Response model for Webhooknotificationobject"""

  data: Optional[Webhooknotificationobject] = None


class WebhooknotificationobjectListResponse(APIResponse):
  """List response model for Webhooknotificationobject"""

  data: List[Webhooknotificationobject] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
