"""Model for OrchestrationIntegration"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestrationintegration(BaseModel):
    """Orchestrationintegration model"""

    id: Optional[str] = None
    """ID of the Integration."""
    label: Optional[str] = None
    """Name of the Integration."""
    parameters: Optional[Dict] = None

class OrchestrationintegrationResponse(APIResponse):
    """Response model for Orchestrationintegration"""
    data: Optional[Orchestrationintegration] = None

class OrchestrationintegrationListResponse(APIResponse):
    """List response model for Orchestrationintegration"""
    data: List[Orchestrationintegration] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
