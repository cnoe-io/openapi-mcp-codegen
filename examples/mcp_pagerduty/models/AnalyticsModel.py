"""Model for AnalyticsModel"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Analyticsmodel(BaseModel):
    """Analyticsmodel model"""

    filters: Optional[Dict] = None
    """Accepts a set of filters to apply to the Incidents before aggregating.  Any incidents that do not match the included filters will be omitted from the results."""
    time_zone: Optional[str] = None
    """The time zone to use for the results and grouping. Must be in tzdata format. See list of accepted values [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)."""
    order: Optional[str] = None
    """The order in which the results were sorted; asc for ascending, desc for descending."""
    order_by: Optional[str] = None
    """The column that was used for ordering the results."""
    aggregate_unit: Optional[str] = None
    """The time unit to aggregate metrics by.  If no value is provided, the metrics will be aggregated for the entire period."""

class AnalyticsmodelResponse(APIResponse):
    """Response model for Analyticsmodel"""
    data: Optional[Analyticsmodel] = None

class AnalyticsmodelListResponse(APIResponse):
    """List response model for Analyticsmodel"""
    data: List[Analyticsmodel] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
