"""Model for AgentReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Agentreference(BaseModel):
    """Agentreference model"""


class AgentreferenceResponse(APIResponse):
    """Response model for Agentreference"""
    data: Optional[Agentreference] = None

class AgentreferenceListResponse(APIResponse):
    """List response model for Agentreference"""
    data: List[Agentreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
