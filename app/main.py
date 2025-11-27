from fastapi import FastAPI
from .api import router as api_router

app = FastAPI(
    title="SEO Article Agent",
    description="Backend service to generate SEO-optimized articles from a topic.",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")
