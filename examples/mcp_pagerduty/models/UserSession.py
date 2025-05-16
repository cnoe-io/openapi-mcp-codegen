"""Model for UserSession"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Usersession(BaseModel):
    """Usersession model"""

    id: str
    user_id: str
    created_at: str
    """The date/time the user session was first created."""
    type: str
    """The type of the session"""
    summary: str
    """The summary of the session"""

class UsersessionResponse(APIResponse):
    """Response model for Usersession"""
    data: Optional[Usersession] = None

class UsersessionListResponse(APIResponse):
    """List response model for Usersession"""
    data: List[Usersession] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
