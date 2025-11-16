"""Main FastAPI application."""
from fastapi import FastAPI
from app.api import qa, health

app = FastAPI(
    title="Question-Answer API",
    version="1.0.0",
    description="Question-Answer API",
    docs_url="/docs",
)

# Include routers
app.include_router(qa.router)
app.include_router(health.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Question-Answer API",
        "version": "1.0.0",
        "status": "running"
    }

