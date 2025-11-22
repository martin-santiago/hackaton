"""
LangGraph workflow for the Price Search Agent.
"""

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from agents.price_search.state import PriceAgentState
from agents.price_search.steps import extract_node, search_node


def create_graph() -> CompiledStateGraph:
    """
    Create the Price Search Agent graph.

    Flow:
    1. search: Search Chilean e-commerce sites
    2. extract: Extract prices using LLM
    3. END: Return results
    """
    workflow = StateGraph(PriceAgentState)

    workflow.add_node("search", search_node)
    workflow.add_node("extract", extract_node)

    workflow.set_entry_point("search")
    workflow.add_edge("search", "extract")
    workflow.add_edge("extract", END)

    return workflow.compile()
