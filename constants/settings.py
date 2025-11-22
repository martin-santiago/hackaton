from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    tavily_api_key: str = ""
    openai_api_key: str = ""

    # LLM settings
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.0

    # Tavily settings
    tavily_max_results: int = 5
    tavily_include_answer: bool = True

    # API settings
    api_title: str = "LangGraph Agent API"
    api_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
