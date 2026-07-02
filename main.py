"""
main.py

Entry point for running the FastAPI application.
Configures metadata, logging, middleware, and includes API routers.
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import router

# Logging Configuration
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Lifespan context manager (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
        logger.info("🚀 FastAPI application started")
        yield
        logger.info("🛑 FastAPI application shutting down")


# FastAPI App Configuration
app = FastAPI(
        title="Utility Knowledge API",
        description="API for equipment and maintenance data",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
)

# Middleware
# Note: allow_origins is intentionally restrictive.
# For production, replace with your actual frontend domain(s).
app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8080"],
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["*"],
)

# Routers
app.include_router(router)


# Application Entry Point
if __name__ == "__main__":
        import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"

    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
                "main:app",
                host=host,
                port=port,
                reload=reload,
                log_level="info",
    )
