"""Model for Orchestration"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestration(BaseModel):
    """Orchestration model"""

    id: Optional[str] = None
    """ID of the Orchestration."""
    self: Optional[str] = None
    """The API show URL at which the object is accessible"""
    name: Optional[str] = None
    """Name of the Orchestration."""
    description: Optional[str] = None
    """A description of this Orchestration's purpose."""
    team: Optional[Dict] = None
    """Reference to the team that owns the Orchestration. If none is specified, only admins have access."""
    integrations: Optional[List[str]] = None
    routes: Optional[int] = None
    """Number of different Service Orchestration being routed to"""
    created_at: Optional[str] = None
    """The date the Orchestration was created at."""
    created_by: Optional[Dict] = None
    """Reference to the user that has created the Orchestration."""
    updated_at: Optional[str] = None
    """The date the Orchestration was last updated."""
    updated_by: Optional[Dict] = None
    """Reference to the user that has updated the Orchestration last."""
    version: Optional[str] = None
    """Version of the Orchestration."""

class OrchestrationResponse(APIResponse):
    """Response model for Orchestration"""
    data: Optional[Orchestration] = None

class OrchestrationListResponse(APIResponse):
    """List response model for Orchestration"""
    data: List[Orchestration] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
