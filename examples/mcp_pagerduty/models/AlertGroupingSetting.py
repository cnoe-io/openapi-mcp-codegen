"""Model for AlertGroupingSetting"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Alertgroupingsetting(BaseModel):
    """Defines how alerts will be automatically grouped into incidents based on the configurations defined. Note that the Alert Grouping Setting features are available only on certain plans.
"""

    id: Optional[str] = None
    name: Optional[str] = None
    """An optional short-form string that provides succinct information about an AlertGroupingSetting object suitable for primary labeling of the entity. It is not intended to be an identifier."""
    description: Optional[str] = None
    """An optional description in string that provides more information about an AlertGroupingSetting object."""
    type: Optional[str] = None
    config: Optional[str] = None
    services: Optional[List[str]] = None
    """The array of one or many Services with just ServiceID/name that the AlertGroupingSetting applies to. Type of content_based_intelligent allows for only one service in the array."""
    created_at: Optional[str] = None
    """The ISO8601 date/time an AlertGroupingSetting got created at."""
    updated_at: Optional[str] = None
    """The ISO8601 date/time an AlertGroupingSetting last got updated at."""

class AlertgroupingsettingResponse(APIResponse):
    """Response model for Alertgroupingsetting"""
    data: Optional[Alertgroupingsetting] = None

class AlertgroupingsettingListResponse(APIResponse):
    """List response model for Alertgroupingsetting"""
    data: List[Alertgroupingsetting] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
