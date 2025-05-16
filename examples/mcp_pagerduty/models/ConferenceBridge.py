"""Model for ConferenceBridge"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Conferencebridge(BaseModel):
    """Conferencebridge model"""

    conference_number: Optional[str] = None
    """The phone number of the conference call for the conference bridge. Phone numbers should be formatted like +1 415-555-1212,,,,1234#, where a comma (,) represents a one-second wait and pound (#) completes access code input."""
    conference_url: Optional[str] = None
    """An URL for the conference bridge. This could be a link to a web conference or Slack channel."""

class ConferencebridgeResponse(APIResponse):
    """Response model for Conferencebridge"""
    data: Optional[Conferencebridge] = None

class ConferencebridgeListResponse(APIResponse):
    """List response model for Conferencebridge"""
    data: List[Conferencebridge] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
