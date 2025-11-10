# Copyright 2025 CNOE
"""Argo_rollouts LangGraph agent wrapper used by the A2A server.

This class inherits from BaseLangGraphAgent to leverage common A2A functionality
while providing argo_rollouts-specific configuration and MCP server bootstrap.
"""

import logging
import os
from typing import Any, List, Optional
from typing_extensions import override

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from cnoe_agent_utils.agents import BaseLangGraphAgent

logger = logging.getLogger(__name__)


class InputField(BaseModel):
  """Model for input field requirements extracted from tool responses"""

  field_name: str = Field(description="The name of the field that should be provided, extracted from the tool's specific request.")
  field_description: str = Field(
    description="A description of what this field represents, based on the tool's actual request for information."
  )
  field_type: Optional[str] = Field(
    default="text", description="The type of input field: 'text', 'number', 'email', 'password', 'textarea', 'select', 'boolean'"
  )
  field_required: Optional[bool] = Field(default=True, description="Whether this field is required")
  field_values: Optional[List[str]] = Field(default=None, description="Possible values for select/dropdown fields, if any")


class Metadata(BaseModel):
  """Model for response metadata"""

  user_input: bool = Field(description="Whether user input is required. Set to true when tools ask for specific information from user.")
  input_fields: Optional[List[InputField]] = Field(
    default=None, description="List of input fields extracted from the tool's specific request, if any"
  )


class PlatformEngineerResponse(BaseModel):
  """Structured response format matching ai-platform-engineering pattern"""

  is_task_complete: bool = Field(description="Whether the task is complete. Set to false if tools ask for more information.")
  require_user_input: bool = Field(
    description="Whether user input is required. Set to true if tools request specific information from user."
  )
  content: str = Field(
    description="The main response content in markdown format. When tools ask for information, preserve their exact message without rewriting."
  )
  metadata: Optional[Metadata] = Field(default=None, description="Additional metadata about the response")


class Argo_rolloutsAgent(BaseLangGraphAgent):
  """Argo_rollouts agent that inherits streaming and A2A protocol handling from BaseLangGraphAgent."""

  @override
  async def _bootstrap_agent(self) -> Any:
    """Bootstrap the argo_rollouts MCP server and return a LangGraph React agent."""
    load_dotenv()
    token = os.getenv("ARGO_ROLLOUTS_TOKEN")
    api_url = os.getenv("ARGO_ROLLOUTS_API_URL")

    if not token or not api_url:
      raise EnvironmentError("Both ARGO_ROLLOUTS_API_URL and ARGO_ROLLOUTS_TOKEN must be set")

    # Import and create the agent
    from agent import create_agent  # noqa: E402

    agent, _ = await create_agent()

    return agent

  @override
  def _get_trace_tags(self) -> list[str]:
    """Return trace tags specific to argo_rollouts."""
    return ["argo_rollouts-a2a"]

  @override
  def _get_trace_name(self) -> str:
    """Return trace name for argo_rollouts queries."""
    return "argo_rollouts-query"

  @override
  def _should_request_user_input(self, final_message_content: str) -> bool:
    """
    Determine if user input is required based on the final message content.

    Override this method to customize when the agent requests user input.
    """
    # Check for common phrases that indicate the agent needs clarification
    clarification_phrases = [
      "please provide",
      "need more info",
      "could you clarify",
      "what would you like",
      "please specify",
      "need additional details",
    ]

    return any(phrase in final_message_content.lower() for phrase in clarification_phrases)

  @override
  def get_agent_name(self) -> str:
    """Return the agent name for identification."""
    return "argo_rollouts-agent"

  @override
  def get_system_instruction(self) -> str:
    """Return the system instruction for the agent."""

    return """You are an expert Argo Rollouts assistant that helps users manage progressive delivery and advanced deployment strategies in Kubernetes.

# CORE CAPABILITIES
You can help with:
- 🚀 **Rollout Management**: Create, deploy, and manage progressive delivery rollouts
- 📊 **Analysis & Validation**: Set up automated analysis templates and monitoring
- 🧪 **Experimentation**: Configure A/B tests and traffic splitting experiments
- 📈 **Progressive Delivery**: Manage canary, blue-green, and custom deployment strategies
- 🔍 **Monitoring**: Track rollout progress, metrics, and health status
- 🛠️ **Troubleshooting**: Debug failed rollouts, analysis issues, and deployment problems

# INTERACTION GUIDELINES
🎯 **Be Specific**: When asking for rollout operations, provide:
- Rollout names and namespaces
- Deployment strategy (canary, blue-green, etc.)
- Traffic routing requirements
- Analysis and validation criteria

💡 **Example Requests**:
- "List all rollouts in namespace 'production'"
- "Create a canary rollout for application 'web-frontend' with 20% traffic split"
- "Promote rollout 'api-service' to the next canary step"
- "Set up analysis template for success rate validation using Prometheus"
- "Abort rollout 'failed-deployment' and revert to stable version"
- "Create an A/B test experiment for feature 'new-checkout-flow'"

# ROLLOUT CREATION TIPS
When creating rollouts, I'll guide you through:
- Deployment strategy selection (canary, blue-green, custom)
- Traffic routing configuration (Istio, NGINX, ALB, etc.)
- Analysis templates and success criteria
- Rollback and abort policies
- Resource specifications and scaling

# COMMON PATTERNS
- For **new rollouts**: I'll ask for strategy, traffic routing, and validation requirements
- For **monitoring**: I'll help track progress, metrics, and analysis results
- For **troubleshooting**: I'll examine rollout status, events, and analysis failures
- For **experiments**: I'll help configure A/B tests and traffic splitting

# PROGRESSIVE DELIVERY BEST PRACTICES
I'll help you implement progressive delivery patterns:
- Gradual traffic shifting with automated validation
- Comprehensive analysis and success criteria
- Automated rollback on failure detection
- Integration with monitoring and observability tools
- Safe deployment practices with minimal blast radius

Ask me anything about Argo Rollouts - I'm here to help you implement safe, progressive deployments!"""

  @override
  def get_response_format_instruction(self) -> str:
    """Return instructions for response formatting."""
    return """CRITICAL: You MUST respond ONLY with a valid JSON object matching the PlatformEngineerResponse schema.

Use this exact JSON structure:
{
  "is_task_complete": true,
  "require_user_input": false,
  "content": "Your complete response content in markdown format",
  "metadata": null
}

RULES:
1. Set "is_task_complete": false if tools ask for more information
2. Set "require_user_input": true if tools request specific information from user
3. When tools ask for input, preserve their exact message in "content" field
4. Use "metadata" field when tools request user input:
   {
     "user_input": true,
     "input_fields": [
       {
         "field_name": "parameter_name",
         "field_description": "Description of what this field represents",
         "field_type": "text",
         "field_required": true,
         "field_values": ["option1", "option2"] or null
       }
     ]
   }

Do NOT include any text before or after the JSON. The "content" field contains your complete, helpful response."""

  @override
  def get_response_format_class(self) -> type[BaseModel]:
    """Return the Pydantic model class for response formatting."""
    return PlatformEngineerResponse

  @override
  def get_tool_working_message(self) -> str:
    """Return message displayed when tools are being executed."""
    return "🔄 Working with Argo_rollouts..."

  @override
  def get_tool_processing_message(self) -> str:
    """Return message displayed when processing tool results."""
    return "📊 Processing argo_rollouts data..."
