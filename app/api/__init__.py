"""
API package for FastAPI routes.
"""
from fastapi import APIRouter
from app.api.routes import routers

# Create main API router
api_router = APIRouter()

# Include all route modules
for router in routers:
    api_router.include_router(router)
