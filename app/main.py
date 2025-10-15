"""FastAPI application initialization."""
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Intelligent Claims QA Service",
    description="Microservice for extracting and analyzing medical claim sheets",
    version="1.0.0"
)

# Include API routes
app.include_router(router)
