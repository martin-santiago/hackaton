"""
Price Search Agent - Main agent class.
"""

from langchain_core.messages import HumanMessage

from agents.price_search.graph import create_graph
from agents.price_search.schemas import PriceSearchResponse
from agents.price_search.state import PriceAgentState


class PriceSearchAgent:
    """
    Agent for searching product prices in Chilean e-commerce stores.

    Usage:
        agent = PriceSearchAgent()
        response = await agent.search("Pelota de futbol")
    """

    def __init__(self):
        self._graph = create_graph()

    async def search(self, product: str) -> PriceSearchResponse:
        """
        Search for product prices.

        Args:
            product: Name of the product to search

        Returns:
            PriceSearchResponse with prices sorted lowest to highest
        """
        initial_state: PriceAgentState = {
            "messages": [HumanMessage(content=product)],
            "product": product,
            "search_results": "",
            "prices": [],
        }

        result = await self._graph.ainvoke(initial_state)
        prices = result.get("prices", [])

        return PriceSearchResponse(
            product=product,
            prices=prices,
            total_results=len(prices),
        )
