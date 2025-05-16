"""Model for Channel"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Channel(BaseModel):
    """Polymorphic object representation of the means by which the action was channeled. Has different formats depending on type, indicated by channel[type]. Will be one of `auto`, `email`, `api`, `nagios`, or `timeout` if `agent[type]` is `service`. Will be one of `email`, `sms`, `website`, `web_trigger`, or `note` if `agent[type]` is `user`. See [below](https://developer.pagerduty.com/documentation/rest/log_entries/show#channel_types) for detailed information about channel formats."""

    type: str
    """type"""
    user: Optional[Dict] = None
    team: Optional[Dict] = None
    notification: Optional[str] = None
    channel: Optional[Dict] = None
    """channel"""
    changeset: Optional[Dict] = None
    """Changeset present in CustomFieldsValueChange and FieldValueChange log entries."""

class ChannelResponse(APIResponse):
    """Response model for Channel"""
    data: Optional[Channel] = None

class ChannelListResponse(APIResponse):
    """List response model for Channel"""
    data: List[Channel] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
