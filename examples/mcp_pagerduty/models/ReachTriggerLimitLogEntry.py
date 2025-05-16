"""Model for ReachTriggerLimitLogEntry"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Reachtriggerlimitlogentry(BaseModel):
    """Reachtriggerlimitlogentry model"""


class ReachtriggerlimitlogentryResponse(APIResponse):
    """Response model for Reachtriggerlimitlogentry"""
    data: Optional[Reachtriggerlimitlogentry] = None

class ReachtriggerlimitlogentryListResponse(APIResponse):
    """List response model for Reachtriggerlimitlogentry"""
    data: List[Reachtriggerlimitlogentry] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
