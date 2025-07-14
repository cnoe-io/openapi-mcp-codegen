# Copyright 2025 CNOE
"""AgentExecutor implementation that connects the Petstore agent to A2A."""

from typing_extensions import override

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.types import (
  TaskArtifactUpdateEvent,
  TaskState,
  TaskStatus,
  TaskStatusUpdateEvent,
)
from a2a.utils import new_agent_text_message, new_task, new_text_artifact

from .agent import PetstoreAgent


class PetstoreAgentExecutor(AgentExecutor):
  """Executes tasks using the generated Petstore LangGraph agent."""

  def __init__(self) -> None:
    self.agent = PetstoreAgent()

  @override
  async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
    query = context.get_user_input()
    task = context.current_task or new_task(context.message)
    if context.current_task is None:
      event_queue.enqueue_event(task)

    async for event in self.agent.stream(query, task.contextId):
      if event["is_task_complete"]:
        event_queue.enqueue_event(
          TaskArtifactUpdateEvent(
            append=False,
            contextId=task.contextId,
            taskId=task.id,
            lastChunk=True,
            artifact=new_text_artifact(
              name="result",
              description="Agent response",
              text=event["content"],
            ),
          )
        )
        event_queue.enqueue_event(
          TaskStatusUpdateEvent(
            final=True,
            contextId=task.contextId,
            taskId=task.id,
            status=TaskStatus(state=TaskState.completed),
          )
        )
      else:
        event_queue.enqueue_event(
          TaskStatusUpdateEvent(
            final=False,
            contextId=task.contextId,
            taskId=task.id,
            status=TaskStatus(
              state=TaskState.working,
              message=new_agent_text_message(event["content"], task.contextId, task.id),
            ),
          )
        )

  @override
  async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:  # noqa: D401
    raise Exception("cancel not supported")
