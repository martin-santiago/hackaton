from typing import Optional

from langchain_core.messages import HumanMessage

from agents.tavily_search.graph import create_tavily_search_agent
from agents.tavily_search.state import AgentState


class TavilySearchAgent:
    """
    High-level wrapper for the Tavily Search Agent.

    Provides a simple interface for interacting with the agent.
    """

    def __init__(self) -> None:
        """Initialize the agent with compiled graph."""
        self._graph = create_tavily_search_agent()

    def invoke(self, query: str) -> str:
        """
        Run the agent with a query and return the response.

        Args:
            query: The user's search query

        Returns:
            The agent's response as a string
        """
        initial_state: AgentState = {
            "messages": [HumanMessage(content=query)],
            "search_results": "",
            "final_answer": "",
        }

        result = self._graph.invoke(initial_state)
        return result.get("final_answer", "No response generated")

    async def ainvoke(self, query: str) -> str:
        """
        Async version of invoke.

        Args:
            query: The user's search query

        Returns:
            The agent's response as a string
        """
        initial_state: AgentState = {
            "messages": [HumanMessage(content=query)],
            "search_results": "",
            "final_answer": "",
        }

        result = await self._graph.ainvoke(initial_state)
        return result.get("final_answer", "No response generated")

    def stream(self, query: str):
        """
        Stream the agent's execution for real-time updates.

        Args:
            query: The user's search query

        Yields:
            State updates as the agent progresses
        """
        initial_state: AgentState = {
            "messages": [HumanMessage(content=query)],
            "search_results": "",
            "final_answer": "",
        }

        for state in self._graph.stream(initial_state):
            yield state
