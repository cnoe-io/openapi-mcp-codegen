"""Model for AlertGroupingParameters"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Alertgroupingparameters(BaseModel):
    """Defines how alerts on this service will be automatically grouped into incidents. Note that the alert grouping features are available only on certain plans. To turn grouping off set the type to null.
This attribute has been deprecated and configuration via [Alert Grouping Settings](https://developer.pagerduty.com/api-reference/587edbc8ff416-create-an-alert-grouping-setting) resource is encouraged.
"""

    type: Optional[str] = None
    config: Optional[str] = None

class AlertgroupingparametersResponse(APIResponse):
    """Response model for Alertgroupingparameters"""
    data: Optional[Alertgroupingparameters] = None

class AlertgroupingparametersListResponse(APIResponse):
    """List response model for Alertgroupingparameters"""
    data: List[Alertgroupingparameters] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
