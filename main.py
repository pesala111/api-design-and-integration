"""
FastAPI application entry point.

This module contains the main FastAPI application instance with basic configuration.
"""

from fastapi import FastAPI
from src.api import router

# Create FastAPI instance with metadata
app = FastAPI(
    title="Utility Knowledge API",
    description="API for equipment and maintenance data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include your endpoints
app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
