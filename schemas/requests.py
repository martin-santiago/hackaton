from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Request schema for search endpoint."""

    query: str = Field(
        ...,
        description="The search query to process",
        min_length=1,
        max_length=1000,
        examples=["What are the latest AI developments?"],
    )


class SearchResponse(BaseModel):
    """Response schema for search endpoint."""

    query: str = Field(description="The original query")
    response: str = Field(description="The agent's response")
    success: bool = Field(default=True, description="Whether the request succeeded")


class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str = Field(description="Error message")
    success: bool = Field(default=False)
