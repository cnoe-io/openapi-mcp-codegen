"""Model for ResponderRequest"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Responderrequest(BaseModel):
    """Responderrequest model"""

    incident: Optional[str] = None
    requester: Optional[str] = None
    requested_at: Optional[str] = None
    """The time the request was made"""
    message: Optional[str] = None
    """The message sent with the responder request"""
    responder_request_targets: Optional[List[str]] = None
    """The array of targets the responder request is being sent to"""

class ResponderrequestResponse(APIResponse):
    """Response model for Responderrequest"""
    data: Optional[Responderrequest] = None

class ResponderrequestListResponse(APIResponse):
    """List response model for Responderrequest"""
    data: List[Responderrequest] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
