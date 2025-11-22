"""
Search step for the Price Search Agent.
"""

from typing import TYPE_CHECKING, Any

from agents.price_search.tools import price_search_tool

if TYPE_CHECKING:
    from agents.price_search.state import PriceAgentState


def search_node(state: "PriceAgentState") -> dict[str, Any]:
    """
    Search for product prices in Chilean e-commerce sites.

    Takes the product name from state and executes the search.
    """
    product = state.get("product", "")

    if not product:
        return {"search_results": "No product provided"}

    search_results = price_search_tool.invoke({"product": product})

    return {"search_results": search_results}
