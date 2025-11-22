"""
Price extraction step for the Price Search Agent.
"""

import json
from typing import TYPE_CHECKING, Any

from langchain_core.messages import HumanMessage, SystemMessage

from agents.price_search.prompts import EXTRACTION_PROMPT, SYSTEM_PROMPT
from agents.price_search.schemas import PriceExtractionOutput, PriceItem
from utils import get_llm

if TYPE_CHECKING:
    from agents.price_search.state import PriceAgentState


def extract_node(state: "PriceAgentState") -> dict[str, Any]:
    """
    Extract structured prices from search results using LLM.

    Parses the raw search results and extracts validated price data.
    """
    llm = get_llm()
    product = state.get("product", "")
    search_results = state.get("search_results", "")

    if not search_results or search_results == "No product provided":
        return {"prices": []}

    # Build extraction prompt
    extraction_prompt = EXTRACTION_PROMPT.format(
        product=product,
        search_results=search_results,
    )

    # Call LLM
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=extraction_prompt),
    ]
    response = llm.invoke(messages)

    # Parse response
    prices = _parse_response(response.content)

    return {"prices": prices}


def _parse_response(response_text: str) -> list[PriceItem]:
    """Parse LLM response into validated PriceItem list."""
    try:
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1

        if json_start == -1 or json_end == 0:
            return []

        json_str = response_text[json_start:json_end]
        data = json.loads(json_str)

        extraction = PriceExtractionOutput(**data)
        return extraction.prices

    except (json.JSONDecodeError, Exception):
        return []
