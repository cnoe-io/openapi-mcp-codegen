"""Model for Ruleset"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Ruleset(BaseModel):
    """Ruleset model"""

    id: Optional[str] = None
    """ID of the Ruleset."""
    self: Optional[str] = None
    """the API show URL at which the object is accessible"""
    type: Optional[str] = None
    name: Optional[str] = None
    """Name of the Ruleset."""
    routing_keys: Optional[List[str]] = None
    """Routing keys routed to this Ruleset."""
    created_at: Optional[str] = None
    """The date the Ruleset was created at."""
    creator: Optional[Dict] = None
    """Reference to the user that has created the Ruleset."""
    updated_at: Optional[str] = None
    """The date the Ruleset was last updated."""
    updater: Optional[Dict] = None
    """Reference to the user that has updated the Ruleset last."""
    team: Optional[Dict] = None
    """Reference to the team that owns the Ruleset. If none is specified, only admins have access."""

class RulesetResponse(APIResponse):
    """Response model for Ruleset"""
    data: Optional[Ruleset] = None

class RulesetListResponse(APIResponse):
    """List response model for Ruleset"""
    data: List[Ruleset] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
