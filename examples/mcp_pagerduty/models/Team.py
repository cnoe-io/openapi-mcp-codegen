"""Model for Team"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Team(BaseModel):
    """Team model"""


class TeamResponse(APIResponse):
    """Response model for Team"""
    data: Optional[Team] = None

class TeamListResponse(APIResponse):
    """List response model for Team"""
    data: List[Team] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
