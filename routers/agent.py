"""
Router for general web search agent endpoints.
"""

from fastapi import APIRouter, HTTPException, status

from exceptions import SearchException
from schemas import SearchRequest, SearchResponse
from services import SearchService

router = APIRouter(prefix="/agent", tags=["Search Agent"])


@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search the web",
    description="Execute a web search using AI agent and get a synthesized response.",
)
async def search(request: SearchRequest) -> SearchResponse:
    """
    Search the web for information.

    - **query**: What you want to search for (e.g., "Latest news about AI")

    Returns a synthesized response based on web search results.
    """
    service = SearchService()

    try:
        return await service.search(request.query)
    except SearchException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )


@router.get("/health", summary="Health check")
async def health_check() -> dict:
    """Check if the search agent service is running."""
    return {"status": "healthy", "service": "search-agent"}
