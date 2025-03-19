"""
API routes for SEO functionality.
"""
import logging
from typing import Dict, List, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from pydantic import BaseModel

from app.services.seo import SeoService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize SEO service
seo_service = SeoService()

class KeywordResearchRequest(BaseModel):
    """Request model for keyword research."""
    topic: str

class ContentPlanRequest(BaseModel):
    """Request model for content plan creation."""
    topic: str
    num_articles: int = 10

class ContentOptimizationRequest(BaseModel):
    """Request model for content optimization."""
    content: str
    target_keyword: str

class MetaTagsRequest(BaseModel):
    """Request model for meta tags generation."""
    title: str
    content: str
    target_keyword: str

class UrlAnalysisRequest(BaseModel):
    """Request model for URL analysis."""
    url: str

@router.post("/keyword-research", response_model=Dict[str, Any])
async def research_keywords(request: KeywordResearchRequest):
    """
    Research keywords for a topic.
    """
    logger.info(f"Keyword research request for topic: {request.topic}")
    
    try:
        result = seo_service.research_keywords(request.topic)
        return result
    
    except Exception as e:
        logger.error(f"Error processing keyword research request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing keyword research: {str(e)}"
        )

@router.post("/content-plan", response_model=Dict[str, Any])
async def create_content_plan(request: ContentPlanRequest):
    """
    Create a content plan for a topic.
    """
    logger.info(f"Content plan request for topic: {request.topic} with {request.num_articles} articles")
    
    try:
        result = seo_service.create_content_plan(request.topic, request.num_articles)
        return result
    
    except Exception as e:
        logger.error(f"Error processing content plan request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating content plan: {str(e)}"
        )

@router.post("/analyze-competition", response_model=Dict[str, Any])
async def analyze_competition(request: KeywordResearchRequest):
    """
    Analyze competition for a topic.
    """
    logger.info(f"Competition analysis request for topic: {request.topic}")
    
    try:
        result = seo_service.analyze_competition(request.topic)
        return result
    
    except Exception as e:
        logger.error(f"Error processing competition analysis request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing competition: {str(e)}"
        )

@router.post("/optimize-content", response_model=Dict[str, Any])
async def optimize_content(request: ContentOptimizationRequest):
    """
    Optimize content for a target keyword.
    """
    logger.info(f"Content optimization request for keyword: {request.target_keyword}")
    
    try:
        result = seo_service.optimize_content(request.content, request.target_keyword)
        return result
    
    except Exception as e:
        logger.error(f"Error processing content optimization request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error optimizing content: {str(e)}"
        )

@router.post("/generate-meta-tags", response_model=Dict[str, str])
async def generate_meta_tags(request: MetaTagsRequest):
    """
    Generate SEO meta tags for content.
    """
    logger.info(f"Meta tags generation request for: {request.title}")
    
    try:
        result = seo_service.generate_meta_tags(request.title, request.content, request.target_keyword)
        return result
    
    except Exception as e:
        logger.error(f"Error processing meta tags generation request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating meta tags: {str(e)}"
        )

@router.post("/analyze-url", response_model=Dict[str, Any])
async def analyze_url(request: UrlAnalysisRequest):
    """
    Analyze a URL for SEO factors.
    """
    logger.info(f"URL analysis request for: {request.url}")
    
    try:
        result = seo_service.analyze_url(request.url)
        return result
    
    except Exception as e:
        logger.error(f"Error processing URL analysis request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing URL: {str(e)}"
        )
