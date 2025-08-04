"""Model for Jiranotification"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Jiranotification(BaseModel):
  """Properties of a Jira notification service integration"""


class JiranotificationResponse(APIResponse):
  """Response model for Jiranotification"""

  data: Optional[Jiranotification] = None


class JiranotificationListResponse(APIResponse):
  """List response model for Jiranotification"""

  data: List[Jiranotification] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
