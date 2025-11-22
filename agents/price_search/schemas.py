"""
Schemas for the Price Search Agent.
"""

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class PriceItem(BaseModel):
    """A single price item from search results."""

    product_name: str = Field(description="Name of the product")
    price: int = Field(description="Price in Chilean pesos (CLP)")
    store: str = Field(description="Store name where the price was found")
    url: Optional[str] = Field(default=None, description="URL to the product page")

    @field_validator("price", mode="before")
    @classmethod
    def parse_price(cls, v):
        """Parse price from various formats to integer."""
        if isinstance(v, int):
            return v
        if isinstance(v, float):
            return int(v)
        if isinstance(v, str):
            cleaned = v.replace("$", "").replace(".", "").replace(",", "").strip()
            cleaned = cleaned.replace("CLP", "").strip()
            try:
                return int(cleaned)
            except ValueError:
                return 0
        return 0

    @field_validator("store", mode="before")
    @classmethod
    def clean_store_name(cls, v):
        """Clean and normalize store name."""
        if not v:
            return "Unknown"
        return str(v).strip()


class PriceSearchRequest(BaseModel):
    """Request body for price search endpoint."""

    product: str = Field(
        ...,
        description="The product name to search for",
        min_length=1,
        max_length=200,
        examples=["Pelota de futbol", "iPhone 15", "Zapatillas Nike"],
    )


class PriceSearchResponse(BaseModel):
    """Response body for price search endpoint."""

    product: str = Field(description="The searched product")
    prices: list[PriceItem] = Field(
        description="List of found prices sorted by price ascending"
    )
    total_results: int = Field(description="Total number of prices found")

    @field_validator("prices", mode="after")
    @classmethod
    def sort_by_price(cls, v):
        """Sort prices from lowest to highest."""
        return sorted(v, key=lambda x: x.price)


class PriceExtractionOutput(BaseModel):
    """Schema for LLM price extraction output."""

    prices: list[PriceItem] = Field(
        description="List of extracted prices from search results"
    )
