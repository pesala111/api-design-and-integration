"""
main.py

Entry point for running the FastAPI application. Configures metadata and
includes routers for API endpoints.
"""


from fastapi import FastAPI
from src.api import router

app = FastAPI(
    title="Utility Knowledge API",
    description="API for equipment and maintenance data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Endpoints
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
