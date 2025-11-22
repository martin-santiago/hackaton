"""
Router for Chilean product price search.
"""

from fastapi import APIRouter, HTTPException, status

from agents.price_search import PriceSearchRequest, PriceSearchResponse
from exceptions import PriceSearchException
from services import PriceService

router = APIRouter(prefix="/prices", tags=["Price Search"])


@router.post(
    "/search",
    response_model=PriceSearchResponse,
    summary="Search product prices in Chile",
)
async def search_prices(request: PriceSearchRequest) -> PriceSearchResponse:
    """
    Search for product prices in Chilean online stores.

    - **product**: Name of the product (e.g., "Pelota de futbol")

    Returns prices sorted from lowest to highest.
    """
    service = PriceService()

    try:
        return await service.search_prices(request.product)
    except PriceSearchException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message,
        )


@router.get("/health", summary="Health check")
async def health_check() -> dict:
    """Check if the price search service is running."""
    return {"status": "healthy", "service": "price-search"}
