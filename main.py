"""
LangGraph Agent API

A FastAPI application that provides AI-powered search capabilities:
- General web search with AI synthesis
- Chilean product price search
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from constants import settings
from exceptions import AgentException
from routers import agent_router, price_router
from utils import load_env

# Load environment variables
load_env()

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="""
## AI-Powered Search API

This API provides two main capabilities:

### 1. Web Search (`/agent/search`)
Search the web and get AI-synthesized responses.

### 2. Price Search (`/prices/search`)
Find product prices across Chilean e-commerce stores.

---
Built with FastAPI + LangGraph + Tavily
    """,
)


# Global exception handler for agent errors
@app.exception_handler(AgentException)
async def agent_exception_handler(request: Request, exc: AgentException):
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message, "success": False},
    )


# Include routers
app.include_router(agent_router)
app.include_router(price_router)


@app.get("/", tags=["Root"])
def root():
    """API root endpoint with welcome message."""
    return {
        "message": "LangGraph Agent API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Root"])
def health():
    """Global health check endpoint."""
    return {"status": "healthy", "version": settings.api_version}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
