"""Model for Slacknotificationobject"""

from typing import List, Optional
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo


class Slacknotificationobject(BaseModel):
  """Properties of a Slack notification service integration"""


class SlacknotificationobjectResponse(APIResponse):
  """Response model for Slacknotificationobject"""

  data: Optional[Slacknotificationobject] = None


class SlacknotificationobjectListResponse(APIResponse):
  """List response model for Slacknotificationobject"""

  data: List[Slacknotificationobject] = Field(default_factory=list)
  pagination: Optional[PaginationInfo] = None
