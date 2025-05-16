"""Model for AuditMetadata"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Auditmetadata(BaseModel):
    """Auditmetadata model"""

    messages: Optional[List[str]] = None

class AuditmetadataResponse(APIResponse):
    """Response model for Auditmetadata"""
    data: Optional[Auditmetadata] = None

class AuditmetadataListResponse(APIResponse):
    """List response model for Auditmetadata"""
    data: List[Auditmetadata] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
