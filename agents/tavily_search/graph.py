from langgraph.graph import END, StateGraph

from agents.tavily_search.state import AgentState
from steps import generate_node, search_node


def create_tavily_search_agent() -> StateGraph:
    """
    Create and compile the Tavily Search Agent graph.

    The graph follows this flow:
    1. search: Execute web search using Tavily
    2. generate: Generate response based on search results
    3. END: Return final response

    Returns:
        Compiled StateGraph ready for invocation
    """
    # Initialize the graph with the state schema
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("search", search_node)
    workflow.add_node("generate", generate_node)

    # Define edges
    workflow.set_entry_point("search")
    workflow.add_edge("search", "generate")
    workflow.add_edge("generate", END)

    # Compile and return
    return workflow.compile()
