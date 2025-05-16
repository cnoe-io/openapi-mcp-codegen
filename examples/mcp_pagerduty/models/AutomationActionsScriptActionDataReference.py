"""Model for AutomationActionsScriptActionDataReference"""

from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import APIResponse, PaginationInfo

class Automationactionsscriptactiondatareference(BaseModel):
    """Automationactionsscriptactiondatareference model"""

    script: str
    """Body of the script to be executed on the Runner. To execute it, the Runner will write the content of the property into a temp file, make the file executable and execute it. It is assumed that the Runner has a properly configured environment to run the script as an executable file. This behaviour can be altered by providing the `invocation_command` property. The maxLength value is specified in bytes."""
    invocation_command: Optional[str] = None
    """The command to executed a script with. With the body of the script written into a temp file, the Runner will execute the `<invocation_command> <temp_file>` command. The maxLength value is specified in bytes."""

class AutomationactionsscriptactiondatareferenceResponse(APIResponse):
    """Response model for Automationactionsscriptactiondatareference"""
    data: Optional[Automationactionsscriptactiondatareference] = None

class AutomationactionsscriptactiondatareferenceListResponse(APIResponse):
    """List response model for Automationactionsscriptactiondatareference"""
    data: List[Automationactionsscriptactiondatareference] = Field(default_factory=list)
    pagination: Optional[PaginationInfo] = None
