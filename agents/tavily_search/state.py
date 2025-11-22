from typing import Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """
    State schema for the Tavily Search Agent.

    Attributes:
        messages: Conversation history with add_messages reducer
        search_results: Results from the Tavily search
        final_answer: The generated response
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    search_results: str
    final_answer: str
