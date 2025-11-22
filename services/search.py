from agents import TavilySearchAgent
from exceptions import SearchException
from schemas import SearchResponse


class SearchService:
    """
    Service for handling web search operations.

    Encapsulates the business logic for web searches,
    keeping the router clean and focused on HTTP concerns.
    """

    def __init__(self):
        self._agent = TavilySearchAgent()

    async def search(self, query: str) -> SearchResponse:
        """
        Execute a web search and return formatted response.

        Args:
            query: The search query string

        Returns:
            SearchResponse with the agent's answer

        Raises:
            SearchException: If the search fails
        """
        try:
            response = await self._agent.ainvoke(query)
            return SearchResponse(
                query=query,
                response=response,
                success=True,
            )
        except Exception as e:
            raise SearchException(f"Search failed: {str(e)}")
