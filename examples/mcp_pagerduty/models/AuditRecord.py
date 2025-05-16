"""Model for AuditRecord"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Auditrecord(BaseModel):
    """An Audit Trail record"""

    id: str
    self: Optional[str] = None
    """Record URL."""
    execution_time: str
    """The date/time the action executed, in ISO8601 format and millisecond precision."""
    execution_context: Optional[Dict] = None
    """Action execution context"""
    actors: Optional[List[str]] = None
    method: Dict
    """The method information"""
    root_resource: str
    action: str
    details: Optional[Dict] = None
    """Additional details to provide further information about the action or
the resource that has been audited.
"""

class AuditrecordResponse(APIResponse):
    """Response model for Auditrecord"""
    data: Optional[Auditrecord] = None

class AuditrecordListResponse(APIResponse):
    """List response model for Auditrecord"""
    data: List[Auditrecord] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
