"""Model for TimeBasedAlertGroupingConfiguration"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Timebasedalertgroupingconfiguration(BaseModel):
    """The configuration for Time Based Alert Grouping"""

    timeout: Optional[int] = None
    """The duration in minutes within which to automatically group incoming Alerts. To continue grouping Alerts until the Incident is resolved, set this value to 0."""

class TimebasedalertgroupingconfigurationResponse(APIResponse):
    """Response model for Timebasedalertgroupingconfiguration"""
    data: Optional[Timebasedalertgroupingconfiguration] = None

class TimebasedalertgroupingconfigurationListResponse(APIResponse):
    """List response model for Timebasedalertgroupingconfiguration"""
    data: List[Timebasedalertgroupingconfiguration] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
