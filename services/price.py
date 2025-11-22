"""
Service for price search operations.
"""

from agents.price_search import PriceSearchAgent, PriceSearchResponse
from exceptions import PriceSearchException


class PriceService:
    """
    Handles product price search business logic.

    Keeps the router clean by encapsulating agent interaction.
    """

    def __init__(self):
        self._agent = PriceSearchAgent()

    async def search_prices(self, product: str) -> PriceSearchResponse:
        """
        Search for product prices in Chilean stores.

        Args:
            product: Name of the product to search

        Returns:
            PriceSearchResponse with sorted prices

        Raises:
            PriceSearchException: If the search fails
        """
        try:
            return await self._agent.search(product)
        except Exception as e:
            raise PriceSearchException(f"Price search failed: {str(e)}")
