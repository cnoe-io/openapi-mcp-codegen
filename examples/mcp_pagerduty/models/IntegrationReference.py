"""Model for IntegrationReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Integrationreference(BaseModel):
    """Integrationreference model"""


class IntegrationreferenceResponse(APIResponse):
    """Response model for Integrationreference"""
    data: Optional[Integrationreference] = None

class IntegrationreferenceListResponse(APIResponse):
    """List response model for Integrationreference"""
    data: List[Integrationreference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
