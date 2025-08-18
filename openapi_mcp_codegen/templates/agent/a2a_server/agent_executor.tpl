{% if file_headers %}# {{ file_headers_copyright }}{% endif %}
"""AgentExecutor implementation that connects the {{ mcp_name | capitalize }} agent to A2A.

  Streams intermediate status updates while tools run and emits a final artifact
  when the agent completes. Uses DefaultRequestHandler + InMemoryTaskStore.
  """

import logging
from typing_extensions import override

from cnoe_agent_utils.tracing import disable_a2a_tracing
disable_a2a_tracing()  # Or import automatically disables A2A

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    InternalError,
    InvalidParamsError,
    Part,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError

from .agent import {{ mcp_name | capitalize }}Agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class {{ mcp_name | capitalize }}AgentExecutor(AgentExecutor):
    """Executes tasks using the generated {{ mcp_name | capitalize }} LangGraph agent."""

    def __init__(self) -> None:
        self.agent = {{ mcp_name | capitalize }}Agent()

    @override
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        error = self._validate_request(context)
        if error:
            raise ServerError(error=InvalidParamsError())

        query = context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)  # type: ignore
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        try:
            async for item in self.agent.stream(query, task.context_id, callbacks=None):
                is_task_complete = item["is_task_complete"]
                require_user_input = item["require_user_input"]

                if not is_task_complete and not require_user_input:
                    await updater.update_status(
                        TaskState.working,
                        new_agent_text_message(
                            item["content"],
                            task.context_id,
                            task.id,
                        ),
                    )
                elif require_user_input:
                    await updater.update_status(
                        TaskState.input_required,
                        new_agent_text_message(
                            item["content"],
                            task.context_id,
                            task.id,
                        ),
                        final=True,
                    )
                    break
                else:
                    await updater.add_artifact(
                        [Part(root=TextPart(text=item["content"]))],
                        name="result",
                    )
                    await updater.complete()
                    break
        except Exception as e:
            logger.error(f"An error occurred while streaming the response: {e}")
            raise ServerError(error=InternalError()) from e

    def _validate_request(self, context: RequestContext) -> bool:
        return False

    @override
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:  # noqa: D401
        raise ServerError(error=UnsupportedOperationError())
