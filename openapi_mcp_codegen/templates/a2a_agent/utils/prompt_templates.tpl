{{ file_header }}

"""
Prompt template utilities for A2A agents.
Simplified version without ai_platform_engineering dependencies.
"""

import datetime
from typing import List


def scope_limited_agent_instruction(
    service_name: str,
    service_operations: str,
    additional_guidelines: List[str] = None,
    include_error_handling: bool = True,
    include_date_handling: bool = True
) -> str:
    """
    Generate a scope-limited agent instruction for a specific service.
    
    Args:
        service_name: Name of the service (e.g., "GitHub", "Argo Workflows")
        service_operations: Description of what operations the service supports
        additional_guidelines: Extra guidelines specific to the service
        include_error_handling: Whether to include error handling instructions
        include_date_handling: Whether to include date handling instructions
    
    Returns:
        Formatted system instruction string
    """
    
    # Get current date for context
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Base instruction
    instruction = f"""You are a specialized AI assistant for {service_name}. Your primary function is to {service_operations}.

## Current Context
- Current date: {current_date}
- Service: {service_name}
- Mode: Tool-based operations through MCP server

## Core Responsibilities
1. **Tool Usage**: Use available tools to interact with {service_name}
2. **Parameter Validation**: Ensure all required parameters are provided before tool execution
3. **Clear Communication**: Provide clear, actionable responses
4. **Scope Adherence**: Focus exclusively on {service_name} operations

## Operational Guidelines
- Always validate required parameters before executing tools
- Provide helpful error messages when parameters are missing
- Use the most appropriate tool for each requested operation
- Maintain a professional and helpful tone"""

    # Add additional guidelines if provided
    if additional_guidelines:
        instruction += "\n\n## Service-Specific Guidelines\n"
        for i, guideline in enumerate(additional_guidelines, 1):
            instruction += f"{i}. {guideline}\n"

    # Add error handling section if requested
    if include_error_handling:
        instruction += """

## Error Handling
- If a tool call fails, provide a clear explanation of what went wrong
- Suggest alternative approaches when possible
- Ask for clarification if the user's request is ambiguous
- Never attempt operations outside your service scope"""

    # Add date handling section if requested
    if include_date_handling:
        instruction += """

## Date and Time Handling
- Use the current date provided above as reference for relative dates
- Convert relative dates (e.g., "yesterday", "last week") to absolute dates
- Always specify date ranges clearly when filtering by time periods"""

    instruction += """

## Response Format
- Provide clear, structured responses
- Use appropriate status indicators (completed, input_required, error)
- Include relevant details from tool responses
- Maintain context across multi-turn conversations"""

    return instruction.strip()


def get_basic_system_instruction(agent_name: str, capabilities: str) -> str:
    """
    Generate a basic system instruction for an agent.
    
    Args:
        agent_name: Name of the agent
        capabilities: Description of agent capabilities
    
    Returns:
        Basic system instruction
    """
    return f"""You are {agent_name}, an AI assistant specialized in {capabilities}.

Your role is to:
1. Understand user requests and respond helpfully
2. Use available tools when appropriate
3. Provide clear, accurate information
4. Ask for clarification when needed

Always maintain a professional and helpful demeanor."""


def format_tool_error(tool_name: str, error_message: str) -> str:
    """
    Format a tool error message consistently.
    
    Args:
        tool_name: Name of the tool that failed
        error_message: The error message
        
    Returns:
        Formatted error message
    """
    return f"❌ Tool '{tool_name}' failed: {error_message}"


def format_tool_success(tool_name: str, result_summary: str) -> str:
    """
    Format a tool success message consistently.
    
    Args:
        tool_name: Name of the tool that succeeded
        result_summary: Summary of the result
        
    Returns:
        Formatted success message
    """
    return f"✅ Tool '{tool_name}' completed successfully: {result_summary}"
