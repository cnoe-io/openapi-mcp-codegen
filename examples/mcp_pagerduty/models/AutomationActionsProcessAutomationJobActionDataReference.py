"""Model for AutomationActionsProcessAutomationJobActionDataReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsprocessautomationjobactiondatareference(BaseModel):
    """Automationactionsprocessautomationjobactiondatareference model"""

    process_automation_job_id: str
    process_automation_job_arguments: Optional[str] = None
    """Arguments to pass to the Process Automation job. The maxLength value is specified in bytes."""
    process_automation_node_filter: Optional[str] = None
    """Node filter for the Process Automation job. The maxLength value is specified in bytes. Filter syntax: https://docs.rundeck.com/docs/manual/11-node-filters.html#node-filter-syntax"""

class AutomationactionsprocessautomationjobactiondatareferenceResponse(APIResponse):
    """Response model for Automationactionsprocessautomationjobactiondatareference"""
    data: Optional[Automationactionsprocessautomationjobactiondatareference] = None

class AutomationactionsprocessautomationjobactiondatareferenceListResponse(APIResponse):
    """List response model for Automationactionsprocessautomationjobactiondatareference"""
    data: List[Automationactionsprocessautomationjobactiondatareference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
