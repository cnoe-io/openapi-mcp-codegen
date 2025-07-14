{% if file_headers %}
# {{ file_headers_copyright }}
# {{ file_headers_license }}
# {{ file_headers_message }}
{% endif %}
"""Data-classes used by the A2A server."""

from enum import Enum
from typing import Optional, TypedDict, List
from pydantic import BaseModel, Field


class MsgType(Enum):
    human = "human"
    assistant = "assistant"


class Message(BaseModel):
    type: MsgType = Field(..., description="originator")
    content: str = Field(..., description="message text")


class InputState(BaseModel):
    messages: Optional[List[Message]] = None


class OutputState(BaseModel):
    messages: Optional[List[Message]] = None


class AgentState(BaseModel):
    input: InputState
    output: Optional[OutputState] = None
