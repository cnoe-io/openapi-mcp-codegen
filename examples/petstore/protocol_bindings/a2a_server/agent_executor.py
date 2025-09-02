# Copyright 2025 CNOE
"""AgentExecutor implementation that connects the Petstore agent to A2A.

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

from .agent import PetstoreAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PetstoreAgentExecutor(AgentExecutor):
  """Executes tasks using the generated Petstore LangGraph agent."""

  def __init__(self) -> None:
    self.agent = PetstoreAgent()

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
      # Log full traceback and execution context
      logger.error(
        "Streaming error (context_id=%s, task_id=%s): %s (%s)",
        getattr(task, "context_id", None),
        getattr(task, "id", None),
        str(e),
        e.__class__.__name__,
        exc_info=True,
      )
      # If this is an ExceptionGroup (e.g., from asyncio.TaskGroup), log nested exceptions too
      sub_excs = getattr(e, "exceptions", None)
      if isinstance(sub_excs, (list, tuple)):
        for idx, sub in enumerate(sub_excs):
          logger.error(
            "  └─ sub-exception[%d]: %s (%s)",
            idx,
            str(sub),
            sub.__class__.__name__,
            exc_info=True,
          )
      raise ServerError(error=InternalError()) from e

  def _validate_request(self, context: RequestContext) -> bool:
    return False

  @override
  async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:  # noqa: D401
    raise ServerError(error=UnsupportedOperationError())
