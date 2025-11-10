{{ file_header }}

"""
Base agent executor for A2A agents.
Simplified version without ai_platform_engineering dependencies.
"""

import logging
import asyncio
import uuid
from typing import Dict, Any, AsyncIterator, Optional
from a2a.types import (
    SendStreamingMessageRequest,
    SendStreamingMessageResponse,
    SendStreamingMessageSuccessResponse,
    Message,
    Part,
    Role
)

logger = logging.getLogger(__name__)


class BaseLangGraphAgentExecutor:
    """
    Base class for agent executors that handle A2A streaming.
    Compatible with A2A framework expectations.
    """

    def __init__(self, agent):
        """Initialize with the agent instance."""
        self.agent = agent

    async def execute(self, request: SendStreamingMessageRequest, queue):
        """
        Execute agent with A2A framework integration.
        This matches the signature expected by the A2A framework.

        Args:
            request: The streaming message request from A2A framework
            queue: The response queue for streaming results
        """
        try:
            # Extract message from request
            message = ""
            if hasattr(request, 'message') and request.message:
                if hasattr(request.message, 'parts'):
                    for part in request.message.parts:
                        if hasattr(part, 'text'):
                            message += part.text
                        elif hasattr(part, 'root') and hasattr(part.root, 'text'):
                            message += part.root.text
                elif hasattr(request.message, 'text'):
                    message = request.message.text

            logger.info(f"Processing message: {message[:100]}...")

            # Invoke agent
            input_data = {"message": message}
            response = self.agent.invoke(input_data)

            # Create Message with agent response
            message_text = response.get("message", "")
            agent_message = Message(
                messageId=str(uuid.uuid4()),
                role=Role.agent,
                parts=[Part(text=message_text)]
            )

            # Enqueue the Message event directly
            await queue.enqueue_event(agent_message)

        except Exception as e:
            logger.error(f"Execution failed: {e}")
            # Create error message
            error_text = f"Error: {str(e)}"
            error_message = Message(
                messageId=str(uuid.uuid4()),
                role=Role.agent,
                parts=[Part(text=error_text)]
            )
            await queue.enqueue_event(error_message)

    async def execute_streaming(
        self,
        request: SendStreamingMessageRequest
    ) -> AsyncIterator[SendStreamingMessageResponse]:
        """
        Execute agent with streaming response.
        Alternative streaming interface.
        """
        try:
            # Extract message from request
            message = ""
            if hasattr(request, 'message') and request.message:
                if hasattr(request.message, 'parts'):
                    for part in request.message.parts:
                        if hasattr(part, 'text'):
                            message += part.text
                        elif hasattr(part, 'root') and hasattr(part.root, 'text'):
                            message += part.root.text
                elif hasattr(request.message, 'text'):
                    message = request.message.text

            logger.info(f"Processing streaming message: {message[:100]}...")

            # Invoke agent
            input_data = {"message": message}
            response = self.agent.invoke(input_data)

            # Create Message with agent response
            message_text = response.get("message", "")
            agent_message = Message(
                messageId=str(uuid.uuid4()),
                role=Role.agent,
                parts=[Part(text=message_text)]
            )

            # Yield streaming response with the Message
            yield SendStreamingMessageResponse(
                SendStreamingMessageSuccessResponse(result=agent_message)
            )

        except Exception as e:
            logger.error(f"Streaming execution failed: {e}")
            # Create error message
            error_text = f"Error: {str(e)}"
            error_message = Message(
                messageId=str(uuid.uuid4()),
                role=Role.agent,
                parts=[Part(text=error_text)]
            )
            # Yield error as a message (not using JSONRPCErrorResponse)
            yield SendStreamingMessageResponse(
                SendStreamingMessageSuccessResponse(result=error_message)
            )
