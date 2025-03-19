"""
Google Keyword Planner service for keyword research.
"""
import logging
import json
import time
import os
from typing import Dict, Any, List, Optional
import requests

from app.config import settings
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

logger = logging.getLogger(__name__)

class GoogleKeywordPlannerService:
    """
    Service for interacting with Google Keyword Planner API.
    This service provides keyword ideas, search volumes, and competition metrics.
    
    Note: Requires a Google Ads account (free to create)
    """
    
    def __init__(self):
        """Initialize the Google Keyword Planner service."""
        self.use_mock_data = settings.USE_MOCK_DATA or not settings.GOOGLE_ADS_CREDENTIALS
        
        if not self.use_mock_data:
            try:
                self.client = GoogleAdsClient.load_from_dict(settings.GOOGLE_ADS_CREDENTIALS)
                self.customer_id = settings.GOOGLE_ADS_CUSTOMER_ID
            except Exception as e:
                logger.error(f"Failed to initialize Google Ads client: {str(e)}")
                logger.info("Falling back to mock data mode")
                self.use_mock_data = True
    
    def get_keyword_ideas(self, seed_keyword: str, location_id: int = 2840) -> List[Dict[str, Any]]:
        """
        Get keyword ideas based on a seed keyword.
        
        Args:
            seed_keyword: Seed keyword to generate ideas from
            location_id: Google Ads location ID (default: 2840 for United States)
            
        Returns:
            List: List of keyword ideas with metrics
        """
        logger.info(f"Getting keyword ideas for: {seed_keyword}")
        
        if self.use_mock_data:
            return self._get_mock_keyword_ideas(seed_keyword)
        
        try:
            # Create a keyword plan ideas service client
            keyword_plan_idea_service = self.client.get_service("KeywordPlanIdeaService")
            
            # Create the request object
            request = self.client.get_type("GenerateKeywordIdeasRequest")
            request.customer_id = self.customer_id
            request.language = self.client.get_service("GoogleAdsService").language_constant_path("1000")  # English
            request.geo_target_constants = [f"geoTargetConstants/{location_id}"]
            request.keyword_seed.keywords.append(seed_keyword)
            request.page_size = 50
            
            # Execute the request
            response = keyword_plan_idea_service.generate_keyword_ideas(request=request)
            
            # Process the results
            keyword_ideas = []
            for idea in response.results:
                keyword_ideas.append({
                    "text": idea.text,
                    "avg_monthly_searches": idea.keyword_idea_metrics.avg_monthly_searches,
                    "competition": str(idea.keyword_idea_metrics.competition),
                    "competition_index": idea.keyword_idea_metrics.competition_index,
                    "low_top_of_page_bid_micros": idea.keyword_idea_metrics.low_top_of_page_bid_micros / 1000000,
                    "high_top_of_page_bid_micros": idea.keyword_idea_metrics.high_top_of_page_bid_micros / 1000000
                })
            
            # Sort by average monthly searches
            keyword_ideas.sort(key=lambda x: x['avg_monthly_searches'], reverse=True)
            
            logger.info(f"Found {len(keyword_ideas)} keyword ideas for {seed_keyword}")
            return keyword_ideas
            
        except GoogleAdsException as e:
            logger.error(f"Google Ads API error: {e}")
            return self._get_mock_keyword_ideas(seed_keyword)
        except Exception as e:
            logger.error(f"Error getting keyword ideas: {str(e)}")
            return self._get_mock_keyword_ideas(seed_keyword)
    
    def get_keyword_metrics(self, keywords: List[str], location_id: int = 2840) -> Dict[str, Dict[str, Any]]:
        """
        Get metrics for specific keywords.
        
        Args:
            keywords: List of keywords to get metrics for
            location_id: Google Ads location ID (default: 2840 for United States)
            
        Returns:
            Dict: Dictionary mapping keywords to their metrics
        """
        logger.info(f"Getting metrics for {len(keywords)} keywords")
        
        if self.use_mock_data:
            return self._get_mock_keyword_metrics(keywords)
        
        try:
            # Create a keyword plan service client
            keyword_plan_service = self.client.get_service("KeywordPlanService")
            keyword_plan_idea_service = self.client.get_service("KeywordPlanIdeaService")
            
            # Create a keyword plan
            keyword_plan = self.client.get_type("KeywordPlan")
            keyword_plan.name = f"Keyword Plan {int(time.time())}"
            operation = self.client.get_type("KeywordPlanOperation")
            operation.create = keyword_plan
            
            # Create a forecast
            response = keyword_plan_service.mutate_keyword_plans(
                customer_id=self.customer_id,
                operations=[operation]
            )
            
            # Get metrics
            request = self.client.get_type("GenerateKeywordIdeaMetricsRequest")
            request.customer_id = self.customer_id
            request.language = self.client.get_service("GoogleAdsService").language_constant_path("1000")  # English
            request.geo_target_constants = [f"geoTargetConstants/{location_id}"]
            request.keywords.extend(keywords)
            
            response = keyword_plan_idea_service.generate_keyword_idea_metrics(request=request)
            
            # Process results
            result = {}
            for i, metric in enumerate(response.metrics):
                keyword = keywords[i]
                result[keyword] = {
                    "avg_monthly_searches": metric.avg_monthly_searches,
                    "competition": str(metric.competition),
                    "competition_index": metric.competition_index,
                    "low_top_of_page_bid_micros": metric.low_top_of_page_bid_micros / 1000000,
                    "high_top_of_page_bid_micros": metric.high_top_of_page_bid_micros / 1000000
                }
            
            return result
            
        except GoogleAdsException as e:
            logger.error(f"Google Ads API error: {e}")
            return self._get_mock_keyword_metrics(keywords)
        except Exception as e:
            logger.error(f"Error getting keyword metrics: {str(e)}")
            return self._get_mock_keyword_metrics(keywords)
    
    def _get_mock_keyword_ideas(self, seed_keyword: str) -> List[Dict[str, Any]]:
        """
        Get mock keyword ideas for development and testing.
        
        Args:
            seed_keyword: Seed keyword to generate ideas from
            
        Returns:
            List: List of mock keyword ideas
        """
        logger.info(f"Using mock data for keyword ideas for: {seed_keyword}")
        
        # Generate mock data based on the seed keyword
        base_variations = [
            f"best {seed_keyword}",
            f"{seed_keyword} guide",
            f"how to {seed_keyword}",
            f"{seed_keyword} for beginners",
            f"{seed_keyword} tips",
            f"{seed_keyword} vs",
            f"cheap {seed_keyword}",
            f"premium {seed_keyword}",
            f"{seed_keyword} review",
            f"top {seed_keyword}",
            f"{seed_keyword} for sale",
            f"{seed_keyword} near me",
            f"{seed_keyword} online",
            f"{seed_keyword} 2023",
            f"{seed_keyword} 2024",
        ]
        
        # Create mock keyword ideas
        keyword_ideas = []
        for i, variation in enumerate(base_variations):
            # Create some variety in the metrics
            monthly_searches = max(500, 10000 - (i * 500) + (i % 3) * 200)
            competition_index = min(100, 20 + (i * 5))
            
            keyword_ideas.append({
                "text": variation,
                "avg_monthly_searches": monthly_searches,
                "competition": "HIGH" if competition_index > 70 else "MEDIUM" if competition_index > 40 else "LOW",
                "competition_index": competition_index,
                "low_top_of_page_bid_micros": 0.5 + (i * 0.1),
                "high_top_of_page_bid_micros": 1.5 + (i * 0.2)
            })
        
        return keyword_ideas
    
    def _get_mock_keyword_metrics(self, keywords: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get mock keyword metrics for development and testing.
        
        Args:
            keywords: List of keywords to get metrics for
            
        Returns:
            Dict: Dictionary mapping keywords to their mock metrics
        """
        logger.info(f"Using mock data for keyword metrics for {len(keywords)} keywords")
        
        import random
        result = {}
        
        for keyword in keywords:
            # Generate metrics based on keyword length as a simple heuristic
            word_count = len(keyword.split())
            char_count = len(keyword)
            
            # Longer keywords typically have lower search volume but less competition
            base_searches = max(100, 5000 - (word_count * 1000) - (char_count * 10))
            monthly_searches = int(base_searches * random.uniform(0.8, 1.2))
            
            competition_index = max(10, 100 - (word_count * 10))
            
            result[keyword] = {
                "avg_monthly_searches": monthly_searches,
                "competition": "HIGH" if competition_index > 70 else "MEDIUM" if competition_index > 40 else "LOW",
                "competition_index": competition_index,
                "low_top_of_page_bid_micros": 0.5 + (word_count * 0.1),
                "high_top_of_page_bid_micros": 1.0 + (word_count * 0.3)
            }
        
        return result
