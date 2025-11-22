from typing import TYPE_CHECKING, Any

from langchain_core.messages import AIMessage

from tools import tavily_search_tool

if TYPE_CHECKING:
    from agents.tavily_search.state import AgentState


def search_node(state: "AgentState") -> dict[str, Any]:
    """
    Execute web search based on the current query.

    This node extracts the search query from the conversation
    and performs a Tavily search.
    """
    messages = state.get("messages", [])

    # Get the last user message as the search query
    query = ""
    for message in reversed(messages):
        if hasattr(message, "type") and message.type == "human":
            query = message.content
            break
        elif isinstance(message, dict) and message.get("role") == "user":
            query = message.get("content", "")
            break

    if not query:
        return {"search_results": "No query provided"}

    # Execute search
    search_results = tavily_search_tool.invoke({"query": query})

    return {"search_results": search_results}
