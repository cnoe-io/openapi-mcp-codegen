"""Model for ContentBasedIntelligentAlertGroupingConfiguration"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Contentbasedintelligentalertgroupingconfiguration(BaseModel):
    """The configuration for Content Based Intelligent Alert Grouping"""

    aggregate: Optional[str] = None
    """Whether Alerts should be grouped if `all` or `any` specified fields match. If `all` is selected, an exact match on every specified field name must occur for Alerts to be grouped. If `any` is selected, Alerts will be grouped when there is an exact match on at least one of the specified fields."""
    fields: Optional[List[str]] = None
    """An array of strings which represent the fields with which to group against. Depending on the aggregate, Alerts will group if some or all the fields match."""
    time_window: Optional[int] = None
    """The maximum amount of time allowed between Alerts. Any Alerts arriving greater than `time_window` seconds apart will not be grouped together. This is a rolling time window up to 24 hours and is counted from the most recently grouped alert. The window is extended every time a new alert is added to the group, up to 24 hours (24 hours only applies to single-service settings). To use the "recommended_time_window," set the value to 0, otherwise the value must be between 300 <= time_window <= 3600."""
    recommended_time_window: Optional[int] = None
    """In order to ensure your Service has the optimal grouping window, we use data science to calculate your Service's average Alert inter-arrival time. We encourage customer's to use this value, please set `time_window` to 0 to use the `recommended_time_window`."""

class ContentbasedintelligentalertgroupingconfigurationResponse(APIResponse):
    """Response model for Contentbasedintelligentalertgroupingconfiguration"""
    data: Optional[Contentbasedintelligentalertgroupingconfiguration] = None

class ContentbasedintelligentalertgroupingconfigurationListResponse(APIResponse):
    """List response model for Contentbasedintelligentalertgroupingconfiguration"""
    data: List[Contentbasedintelligentalertgroupingconfiguration] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
