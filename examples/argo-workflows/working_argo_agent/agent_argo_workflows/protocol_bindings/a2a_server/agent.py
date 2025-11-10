# Copyright 2025 CNOE
# SPDX-License-Identifier: Apache-2.0

"""Argo Workflows Agent implementation using common A2A base classes."""

import os
from typing import Literal
from pydantic import BaseModel

from .base_langgraph_agent import BaseLangGraphAgent
from .prompt_templates import build_system_instruction, graceful_error_handling_template, SCOPE_LIMITED_GUIDELINES, STANDARD_RESPONSE_GUIDELINES, HUMAN_IN_LOOP_NOTES, LOGGING_NOTES, DATE_HANDLING_NOTES
from cnoe_agent_utils.tracing import trace_agent_stream


class ResponseFormat(BaseModel):
    """Respond to the user in this format."""

    status: Literal['input_required', 'completed', 'error'] = 'input_required'
    message: str


class ArgoWorkflowsAgent(BaseLangGraphAgent):
    """Argo Workflows Agent for managing workflow resources."""

    SYSTEM_INSTRUCTION = build_system_instruction(
        agent_name="ARGO WORKFLOWS AGENT",
        agent_purpose="You are an expert assistant for managing Argo Workflows resources. Your sole purpose is to help users create, manage, monitor, and troubleshoot Argo Workflows. Always return any workflow resource links in markdown format.",
        response_guidelines=SCOPE_LIMITED_GUIDELINES + STANDARD_RESPONSE_GUIDELINES + [
            "Only use the available Argo Workflows tools to interact with the Argo Workflows API",
            "Do not provide general guidance from your knowledge base unless explicitly asked",
            "Always send tool results directly to the user without analyzing or interpreting",
            "When querying workflows or resources with date-based filters, use the current date provided above as reference",
            "",
            "**CRITICAL - Tool Selection Strategy**:",
            "1. **ALWAYS prefer workflow-specific tools** for queries that:",
            "   - Search for workflows, templates, or cron workflows by name",
            "   - Filter by status, namespace, labels, or annotations",
            "   - Look for resources containing specific text (e.g., 'find workflows with ci', 'search for failed workflows')",
            "   - Need to search across multiple workflow types",
            "   ",
            "2. **Use list tools ONLY when**:",
            "   - User explicitly asks for 'all' or 'list all' resources",
            "   - User requests a complete inventory or full list",
            "   - User asks for a specific page (e.g., 'page 2 of workflows')",
            "   - No search criteria are provided",
            "",
            "3. **Examples of when to use specific workflow tools**:",
            "   - 'Show me failed workflows' → Use list/filter tools with status filters",
            "   - 'Find workflows named ci-*' → Use search or list with name filters",
            "   - 'Templates in the prod namespace' → Use template list with namespace filter",
            "   - 'Find data processing workflows' → Use search functionality",
            "",
            "4. **Examples of when to use list tools**:",
            "   - 'List all workflows' → Use workflow list tools",
            "   - 'Show me page 2 of templates' → Use template list with pagination",
            "   - 'Get a complete inventory of cron workflows' → Use cron workflow list",
            "",
            "**CRITICAL - Output Token Limits & Pagination**:",
            "You MUST follow these rules due to 16K output token limit to prevent stream disconnection:",
            "",
            "**For ANY list operation (workflows, templates, cron workflows, etc.):**",
            "",
            "1. If result contains >50 items:",
            "   a) ALWAYS start with: 'This is PAGE 1 of <total> items'",
            "   b) Add '## Summary' section with total count and relevant breakdowns",
            "   c) Add '## First 20 <ResourceType>' as a header",
            "   d) Create a markdown table with appropriate columns for the resource type:",
            "      - Workflows: | # | Name | Namespace | Status | Phase | Started | Duration |",
            "      - Templates: | # | Name | Namespace | Created | Description |",
            "      - Cron Workflows: | # | Name | Namespace | Schedule | Suspended | Last Run |",
            "   e) List EXACTLY the first 20 items from the tool output",
            "   f) End with: 'Showing 1-20 of <total>. Ask for \"page 2\" or use filters for more.'",
            "",
            "2. If result contains ≤50 items:",
            "   - Still mention: 'Showing all <total> items'",
            "   - List all in a table format",
            "",
            "3. NEVER attempt to list >50 items in detail - stream will disconnect",
            "4. Always inform user this is page 1 and pagination is available",
            "",
        ],
        important_notes=HUMAN_IN_LOOP_NOTES + LOGGING_NOTES + DATE_HANDLING_NOTES,
        graceful_error_handling=graceful_error_handling_template("Argo Workflows")
    )

    RESPONSE_FORMAT_INSTRUCTION: str = (
        'Select status as completed if the request is complete'
        'Select status as input_required if the input is a question to the user'
        'Set response status to error if the input indicates an error'
    )

    def get_agent_name(self) -> str:
        """Return the agent's name."""
        return "argo_workflows"

    def get_system_instruction(self) -> str:
        """Return the system instruction for the agent."""
        return self.SYSTEM_INSTRUCTION

    def get_response_format_instruction(self) -> str:
        """Return the response format instruction."""
        return self.RESPONSE_FORMAT_INSTRUCTION

    def get_response_format_class(self) -> type[BaseModel]:
        """Return the response format class."""
        return ResponseFormat

    def get_mcp_config(self, server_path: str) -> dict:
        """Return MCP configuration - not used for HTTP MCP."""
        # This method is for stdio MCP servers, not HTTP
        # For HTTP MCP, we use get_mcp_http_config() instead
        return {}

    def get_mcp_http_config(self) -> dict:
        """Return HTTP MCP configuration for Argo Workflows."""
        # Custom configuration for direct MCP server connection
        mcp_host = os.getenv("MCP_HOST", "localhost")
        mcp_port = os.getenv("MCP_PORT", "3001")

        return {
            "url": f"http://{mcp_host}:{mcp_port}/mcp",
            "headers": {
                "Content-Type": "application/json",
            }
        }

    def get_tool_working_message(self) -> str:
        """Return message shown when calling tools."""
        return 'Looking up Argo Workflows Resources...'

    def get_tool_processing_message(self) -> str:
        """Return message shown when processing tool results."""
        return 'Processing Argo Workflows Resources...'

    @trace_agent_stream("argo_workflows")
    async def stream(self, query: str, sessionId: str, trace_id: str = None):
        """
        Stream responses with argo workflows-specific tracing.

        Overrides the base stream method to add agent-specific tracing decorator.
        """
        async for event in super().stream(query, sessionId, trace_id):
            yield event