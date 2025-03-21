from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uvicorn
import os

from app.api.routes import projects, clients, analytics, blog_generator, seo
from app.config import settings
from app.db.session import engine, Base, get_db
from app.utils.logger import setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle event handler for startup and shutdown events.
    """
    # Startup event
    logger.info("Starting SEO Blog Builder application")
    
    # Create database tables on startup if they don't exist
    Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown event
    logger.info("Shutting down SEO Blog Builder application")

# Initialize FastAPI app
app = FastAPI(
    title="SEO Blog Builder API",
    description="API for creating customized SEO-optimized blog sites for marketing.",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

# Include API routes
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(blog_generator.router, prefix="/api/blog", tags=["blog_generator"])
app.include_router(seo.router, prefix="/api/seo", tags=["seo"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to SEO Blog Builder API",
        "version": "0.1.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.APP_ENV
    }

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
