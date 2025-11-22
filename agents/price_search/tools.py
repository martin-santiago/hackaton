"""
Tools for the Price Search Agent.
"""

from typing import Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from tavily import TavilyClient

from constants import settings


class PriceSearchInput(BaseModel):
    """Input schema for price search tool."""

    product: str = Field(description="The product name to search for prices")
    max_results: Optional[int] = Field(
        default=None, description="Maximum number of results to return"
    )


# Chilean e-commerce domains to search
CHILEAN_DOMAINS = [
    "mercadolibre.cl",
    "falabella.com",
    "ripley.cl",
    "paris.cl",
    "lider.cl",
    "sodimac.cl",
    "easy.cl",
    "pcfactory.cl",
    "abcdin.cl",
    "hites.com",
    "lapolar.cl",
    "jumbo.cl",
    "tottus.cl",
    "knasta.cl",
    "solotodo.cl",
    "spdigital.cl",
    "walmart.cl",
    "microplay.cl",
    "weplay.cl",
    "zmart.cl",
]


def get_tavily_client() -> TavilyClient:
    """Get Tavily client instance."""
    return TavilyClient(api_key=settings.tavily_api_key)


@tool(args_schema=PriceSearchInput)
def price_search_tool(product: str, max_results: Optional[int] = None) -> str:
    """
    Search for product prices in Chilean e-commerce websites.

    Use this tool to find the best prices for a product in Chile.
    Returns search results from Chilean online stores with prices.
    """
    client = get_tavily_client()

    # Build search query optimized for Chilean price search
    search_query = f"{product} precio Chile comprar"

    results = client.search(
        query=search_query,
        max_results=max_results or 10,
        include_answer=True,
        include_domains=CHILEAN_DOMAINS,
    )

    # Format results for price extraction
    output_parts = []

    if results.get("answer"):
        output_parts.append(f"Summary: {results['answer']}\n")

    output_parts.append("Search Results:")
    for idx, result in enumerate(results.get("results", []), 1):
        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        content = result.get("content", "No content")
        output_parts.append(
            f"\n{idx}. Title: {title}\n   URL: {url}\n   Content: {content}"
        )

    return "\n".join(output_parts)
