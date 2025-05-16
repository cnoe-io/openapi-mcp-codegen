"""Model for OrchestrationCacheVariableTriggerEventCount"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Orchestrationcachevariabletriggereventcount(BaseModel):
    """Orchestrationcachevariabletriggereventcount model"""


class OrchestrationcachevariabletriggereventcountResponse(APIResponse):
    """Response model for Orchestrationcachevariabletriggereventcount"""
    data: Optional[Orchestrationcachevariabletriggereventcount] = None

class OrchestrationcachevariabletriggereventcountListResponse(APIResponse):
    """List response model for Orchestrationcachevariabletriggereventcount"""
    data: List[Orchestrationcachevariabletriggereventcount] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
