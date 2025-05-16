"""Model for AutoPauseNotificationsParameters"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Autopausenotificationsparameters(BaseModel):
    """Defines how alerts on this service are automatically suspended for a period of time before triggering, when identified as likely being transient. Note that automatically pausing notifications is only available on certain plans."""

    enabled: Optional[bool] = None
    """Indicates whether alerts should be automatically suspended when identified as transient"""
    timeout: Optional[int] = None
    """Indicates in seconds how long alerts should be suspended before triggering. To automatically select the recommended timeout for a service, set this value to `0`."""
    recommended_timeout: Optional[int] = None
    """The recommended timeout setting for this service based on prior alert patterns."""

class AutopausenotificationsparametersResponse(APIResponse):
    """Response model for Autopausenotificationsparameters"""
    data: Optional[Autopausenotificationsparameters] = None

class AutopausenotificationsparametersListResponse(APIResponse):
    """List response model for Autopausenotificationsparameters"""
    data: List[Autopausenotificationsparameters] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
