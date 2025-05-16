"""Model for RelatedIncidentServiceDependencyBase"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Relatedincidentservicedependencybase(BaseModel):
    """Relatedincidentservicedependencybase model"""

    id: Optional[str] = None
    """The ID of the Service referenced."""
    type: Optional[str] = None
    """The type of the related Service."""
    self: Optional[str] = None
    """The API show URL at which the object is accessible."""

class RelatedincidentservicedependencybaseResponse(APIResponse):
    """Response model for Relatedincidentservicedependencybase"""
    data: Optional[Relatedincidentservicedependencybase] = None

class RelatedincidentservicedependencybaseListResponse(APIResponse):
    """List response model for Relatedincidentservicedependencybase"""
    data: List[Relatedincidentservicedependencybase] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
