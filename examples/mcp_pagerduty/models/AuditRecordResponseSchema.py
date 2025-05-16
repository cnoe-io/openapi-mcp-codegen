"""Model for AuditRecordResponseSchema"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Auditrecordresponseschema(BaseModel):
    """Auditrecordresponseschema model"""


class AuditrecordresponseschemaResponse(APIResponse):
    """Response model for Auditrecordresponseschema"""
    data: Optional[Auditrecordresponseschema] = None

class AuditrecordresponseschemaListResponse(APIResponse):
    """List response model for Auditrecordresponseschema"""
    data: List[Auditrecordresponseschema] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
