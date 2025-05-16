"""Model for ResponderRequestTargetReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Responderrequesttargetreference(BaseModel):
    """Responderrequesttargetreference model"""

    type: Optional[str] = None
    """The type of target (either a user or an escalation policy)"""
    id: Optional[str] = None
    """The id of the user or escalation policy"""
    summary: Optional[str] = None
    incident_responders: Optional[List[str]] = None
    """An array of responders associated with the specified incident"""

class ResponderrequesttargetreferenceResponse(APIResponse):
    """Response model for Responderrequesttargetreference"""
    data: Optional[Responderrequesttargetreference] = None

class ResponderrequesttargetreferenceListResponse(APIResponse):
    """List response model for Responderrequesttargetreference"""
    data: List[Responderrequesttargetreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
