from typing import Annotated, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from agents.price_search.schemas import PriceItem


class PriceAgentState(TypedDict):
    """
    State schema for the Price Search Agent.

    Attributes:
        messages: Conversation history with add_messages reducer
        product: The product being searched
        search_results: Raw results from the price search
        prices: Extracted list of prices
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    product: str
    search_results: str
    prices: list[PriceItem]
