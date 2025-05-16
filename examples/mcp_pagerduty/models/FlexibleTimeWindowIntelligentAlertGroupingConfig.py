"""Model for FlexibleTimeWindowIntelligentAlertGroupingConfig"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Flexibletimewindowintelligentalertgroupingconfig(BaseModel):
    """The configuration for Intelligent Alert Grouping. Note that this configuration is only available for certain plans."""

    time_window: Optional[int] = None
    """The maximum amount of time allowed between Alerts. Any Alerts arriving greater than `time_window` seconds apart will not be grouped together. This is a rolling time window and is counted from the most recently grouped alert. The window is extended every time a new alert is added to the group, up to 24 hours. To use the "recommended_time_window," set the value to 0, otherwise the value must be between 300 and 3600."""
    recommended_time_window: Optional[int] = None
    """In order to ensure your Service has the optimal grouping window, we use data science to calculate your Service`s average Alert inter-arrival time. We encourage customer`s to use this value, please set `time_window` to 0 to use the `recommended_time_window`."""

class FlexibletimewindowintelligentalertgroupingconfigResponse(APIResponse):
    """Response model for Flexibletimewindowintelligentalertgroupingconfig"""
    data: Optional[Flexibletimewindowintelligentalertgroupingconfig] = None

class FlexibletimewindowintelligentalertgroupingconfigListResponse(APIResponse):
    """List response model for Flexibletimewindowintelligentalertgroupingconfig"""
    data: List[Flexibletimewindowintelligentalertgroupingconfig] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
