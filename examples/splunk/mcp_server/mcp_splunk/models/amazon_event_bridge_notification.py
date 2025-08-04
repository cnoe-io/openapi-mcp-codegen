"""Model for Amazoneventbridgenotification"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Amazoneventbridgenotification(BaseModel):
  """Properties of an Amazon EventBridge notification integration"""


class AmazoneventbridgenotificationResponse(APIResponse):
  """Response model for Amazoneventbridgenotification"""

  data: Optional[Amazoneventbridgenotification] = None


class AmazoneventbridgenotificationListResponse(APIResponse):
  """List response model for Amazoneventbridgenotification"""

  data: List[Amazoneventbridgenotification] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
