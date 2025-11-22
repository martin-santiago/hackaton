from typing import TYPE_CHECKING, Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from prompts import SEARCH_AGENT_SYSTEM_PROMPT
from utils import get_llm

if TYPE_CHECKING:
    from agents.tavily_search.state import AgentState


def generate_node(state: "AgentState") -> dict[str, Any]:
    """
    Generate a response based on search results.

    This node takes the search results and generates a
    comprehensive answer using the LLM.
    """
    llm = get_llm()
    messages = state.get("messages", [])
    search_results = state.get("search_results", "")

    # Build the context message
    context_message = f"""Based on the following search results, provide a helpful answer:

Search Results:
{search_results}

Provide a clear, well-structured response that addresses the user's question.
Include relevant information from the search results and cite sources when appropriate.
"""

    # Prepare messages for LLM
    llm_messages = [
        SystemMessage(content=SEARCH_AGENT_SYSTEM_PROMPT),
    ]

    # Add conversation history
    for message in messages:
        if hasattr(message, "type"):
            if message.type == "human":
                llm_messages.append(HumanMessage(content=message.content))
            elif message.type == "ai":
                llm_messages.append(AIMessage(content=message.content))
        elif isinstance(message, dict):
            role = message.get("role", "")
            content = message.get("content", "")
            if role == "user":
                llm_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                llm_messages.append(AIMessage(content=content))

    # Add context with search results
    llm_messages.append(HumanMessage(content=context_message))

    # Generate response
    response = llm.invoke(llm_messages)

    return {
        "messages": messages + [AIMessage(content=response.content)],
        "final_answer": response.content,
    }
