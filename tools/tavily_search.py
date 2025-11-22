from typing import Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from tavily import TavilyClient

from constants import settings


class TavilySearchInput(BaseModel):
    """Input schema for Tavily search tool."""

    query: str = Field(description="The search query to look up on the web")
    max_results: Optional[int] = Field(
        default=None, description="Maximum number of results to return"
    )


def get_tavily_client() -> TavilyClient:
    """Get Tavily client instance."""
    return TavilyClient(api_key=settings.tavily_api_key)


@tool(args_schema=TavilySearchInput)
def tavily_search_tool(query: str, max_results: Optional[int] = None) -> str:
    """
    Search the web using Tavily API.

    Use this tool to find current information from the internet.
    Returns relevant search results with titles, URLs, and content snippets.
    """
    client = get_tavily_client()

    results = client.search(
        query=query,
        max_results=max_results or settings.tavily_max_results,
        include_answer=settings.tavily_include_answer,
    )

    # Format results for the agent
    output_parts = []

    if results.get("answer"):
        output_parts.append(f"Summary: {results['answer']}\n")

    output_parts.append("Sources:")
    for idx, result in enumerate(results.get("results", []), 1):
        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        content = result.get("content", "No content")[:300]
        output_parts.append(f"\n{idx}. {title}\n   URL: {url}\n   {content}...")

    return "\n".join(output_parts)
