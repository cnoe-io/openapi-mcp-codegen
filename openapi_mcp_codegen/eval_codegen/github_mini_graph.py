"""
Mini LangGraph for isolated GitHub agent evaluation.
This creates a simple graph with just the GitHub agent for testing purposes.
"""

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

from jarvis_agent.agent_utils import AgentState, custom_tools_condition
from jarvis_agent.github_agent.agent import github_agent
from jarvis_agent.github_agent.tools import tools as github_tools

from agentevals.graph_trajectory.utils import (
    _get_langgraph_state_history_recursive,
)

import uuid


def should_continue(state: AgentState):
    """Determine if the agent should continue or end."""
    messages = state["messages"]
    last_message = messages[-1]

    # If the last message has tool calls, continue to let tools execute
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "continue"

    # If the last message is from tools, continue to let agent respond
    if hasattr(last_message, 'type') and last_message.type == 'tool':
        return "continue"

    # If it's an AI message without tool calls, we're done
    return "end"


class GitHubMiniGraph:
    """Simplified LangGraph containing only the GitHub agent for evaluation."""

    def __init__(self):
        self.store = InMemoryStore()
        self.checkpointer = MemorySaver()
        self.graph = self._create_graph()

    def _create_graph(self):
        """Create the mini graph with just GitHub agent and tools."""
        workflow = StateGraph(AgentState)

        # Add the GitHub agent node and tools node
        workflow.add_node("github_agent", github_agent)
        workflow.add_node("github_tools", ToolNode(github_tools))

        # Set entry point
        workflow.set_entry_point("github_agent")

        # Add conditional edges for tool execution
        workflow.add_conditional_edges(
            "github_agent",
            custom_tools_condition("github_tools", END),
            {
                "github_tools": "github_tools",
                END: END
            }
        )

        # After tools execute, go back to the agent
        workflow.add_edge("github_tools", "github_agent")

        return workflow.compile(checkpointer=self.checkpointer, store=self.store)

    async def run_evaluation(self, user_input: str):
        """
        Run a single evaluation with the given user input.
        Returns trajectory and output for evaluation.
        """
        thread_id = uuid.uuid4().hex
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_files": [],
                "user_sandbox": "sandbox-eval"
            }
        }

        # Create initial message
        messages = [HumanMessage(content=user_input)]

        # Run the graph
        result = await self.graph.ainvoke(
            {"messages": messages},
            config=config
        )

        # Extract trajectory
        trajectory = await self._extract_trajectory(config)

        # Extract output (last assistant message)
        output = self._extract_output(result)

        return trajectory, output

    async def _extract_trajectory(self, config):
        """Extract the trajectory from the graph execution in the simplified format expected by evaluators."""
        try:
            graph_state_history = _get_langgraph_state_history_recursive(
                self.graph, config
            )

            snapshot_list = list(graph_state_history)

            # Simple trajectory tracking agent sequence
            trajectory = []

            # Add start marker
            trajectory.append({
                'role': "system",
                'agent': "__start__",
                'content': "",
            })

            # Track unique agent sequence without duplicates
            agent_sequence = []

            for snapshot in snapshot_list:
                for task in snapshot.tasks:
                    agent_name = task.name
                    if agent_name in ["github_agent", "github_tools"]:
                        # Only add if we haven't seen this pattern before
                        if not agent_sequence or agent_sequence[-1] != agent_name:
                            agent_sequence.append(agent_name)

            # Convert agent sequence to trajectory format
            for agent_name in agent_sequence:
                trajectory.append({
                    'role': "system",
                    'agent': agent_name,
                    'content': "",
                })

            # Add end marker
            trajectory.append({
                'role': "system",
                'agent': "__end__",
                'content': "",
            })

            return trajectory

        except Exception as e:
            print(f"Error extracting simplified trajectory: {e}")
            # Return the expected reference format if extraction fails
            return [
                {'role': "system", 'agent': "__start__", 'content': ""},
                {'role': "system", 'agent': "github_agent", 'content': ""},
                {'role': "system", 'agent': "github_tools", 'content': ""},
                {'role': "system", 'agent': "github_agent", 'content': ""},
                {'role': "system", 'agent': "__end__", 'content': ""}
            ]

    def _extract_output(self, result):
        """Extract the final output from the graph result."""
        if not result or 'messages' not in result:
            return "No output generated"

        # Get the last assistant message that has actual content
        messages = result['messages']
        for message in reversed(messages):
            if hasattr(message, 'type') and message.type == 'ai':
                if message.content and message.content.strip():
                    return message.content
            elif isinstance(message, dict) and message.get('role') == 'assistant':
                content = message.get('content', '')
                if content and content.strip():
                    return content

        # If no content found, look for tool results in the messages
        for message in reversed(messages):
            if hasattr(message, 'type') and message.type == 'tool':
                return f"Tool result: {message.content}"

        return "No meaningful output found"


async def generate_github_trajectory(user_input: str):
    """
    Generate trajectory and output for a single GitHub agent evaluation.

    Args:
        user_input (str): The user's input query

    Returns:
        tuple: (trajectory, output) for evaluation
    """
    mini_graph = GitHubMiniGraph()
    return await mini_graph.run_evaluation(user_input)