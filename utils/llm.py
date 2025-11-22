from functools import lru_cache

from langchain_openai import ChatOpenAI

from constants import settings


@lru_cache
def get_llm() -> ChatOpenAI:
    """Get cached LLM instance."""
    return ChatOpenAI(
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        api_key=settings.openai_api_key,
    )
