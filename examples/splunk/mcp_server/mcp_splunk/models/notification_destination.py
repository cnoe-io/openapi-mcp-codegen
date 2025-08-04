"""Model for Notificationdestination"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Notificationdestination(BaseModel):
  """Notification service"""


class NotificationdestinationResponse(APIResponse):
  """Response model for Notificationdestination"""

  data: Optional[Notificationdestination] = None


class NotificationdestinationListResponse(APIResponse):
  """List response model for Notificationdestination"""

  data: List[Notificationdestination] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
