"""
SEO Data Aggregator for combining data from different tools.
"""
import logging
from typing import Dict, Any, List, Optional
import json

from app.services.seo.free_tools.keyword_planner import GoogleKeywordPlannerService
from app.services.seo.free_tools.serp_analyzer import SerpAnalyzerService
from app.services.seo.free_tools.nlp_analyzer import NlpKeywordAnalyzer

logger = logging.getLogger(__name__)

class SeoDataAggregator:
    """
    Service for aggregating data from different SEO tools and providing consolidated results.
    """
    
    def __init__(self):
        """Initialize the SEO Data Aggregator service."""
        self.keyword_planner = GoogleKeywordPlannerService()
        self.serp_analyzer = SerpAnalyzerService()
        self.nlp_analyzer = NlpKeywordAnalyzer()
    
    def get_comprehensive_keyword_data(self, seed_keyword: str) -> Dict[str, Any]:
        """
        Get comprehensive keyword data from all available sources.
        
        Args:
            seed_keyword: Seed keyword to research
            
        Returns:
            Dict: Comprehensive keyword data
        """
        logger.info(f"Getting comprehensive keyword data for: {seed_keyword}")
        
        try:
            # Get keyword ideas from Keyword Planner
            keyword_ideas = self.keyword_planner.get_keyword_ideas(seed_keyword)
            
            # Analyze SERP for the seed keyword
            serp_analysis = self.serp_analyzer.analyze_serp(seed_keyword)
            
            # Generate related keywords with NLP
            related_keywords = self.nlp_analyzer.generate_related_keywords(seed_keyword)
            
            # Combine data
            result = {
                "seed_keyword": seed_keyword,
                "keyword_ideas": keyword_ideas,
                "related_keywords": [{"text": kw} for kw in related_keywords],
                "serp_analysis": {
                    "common_words": serp_analysis.get("common_words", []),
                    "common_phrases": serp_analysis.get("common_phrases", []),
                    "title_patterns": serp_analysis.get("title_patterns", {}),
                    "content_structure": serp_analysis.get("content_structure", {})
                },
                "top_ranking_urls": [result.get("url") for result in serp_analysis.get("results", [])]
            }
            
            logger.info(f"Successfully aggregated keyword data for: {seed_keyword}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting comprehensive keyword data: {str(e)}")
            return {
                "seed_keyword": seed_keyword,
                "error": str(e),
                "keyword_ideas": [],
                "related_keywords": [],
                "serp_analysis": {},
                "top_ranking_urls": []
            }
    
    def analyze_topic(self, topic: str) -> Dict[str, Any]:
        """
        Perform a comprehensive topic analysis for content planning.
        
        Args:
            topic: Topic to analyze
            
        Returns:
            Dict: Topic analysis results
        """
        logger.info(f"Analyzing topic: {topic}")
        
        try:
            # Get keyword data
            keyword_data = self.get_comprehensive_keyword_data(topic)
            
            # Generate subtopics
            subtopics = self._generate_subtopics(topic, keyword_data)
            
            # Analyze competition
            competition_analysis = self._analyze_competition(keyword_data.get("top_ranking_urls", [])[:5])
            
            # Generate content recommendations
            content_recommendations = self._generate_content_recommendations(
                topic,
                subtopics,
                keyword_data,
                competition_analysis
            )
            
            # Create final analysis
            analysis = {
                "topic": topic,
                "subtopics": subtopics,
                "primary_keywords": [
                    kw.get("text", "") for kw in keyword_data.get("keyword_ideas", [])[:10]
                ],
                "related_keywords": [
                    kw.get("text", "") for kw in keyword_data.get("related_keywords", [])[:20]
                ],
                "competition": {
                    "top_urls": keyword_data.get("top_ranking_urls", [])[:5],
                    "analysis": competition_analysis
                },
                "content_recommendations": content_recommendations
            }
            
            logger.info(f"Successfully analyzed topic: {topic}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing topic: {str(e)}")
            return {
                "topic": topic,
                "error": str(e),
                "subtopics": [],
                "primary_keywords": [],
                "related_keywords": [],
                "competition": {},
                "content_recommendations": {}
            }
    
    def create_content_plan(self, topic: str, num_articles: int = 10) -> Dict[str, Any]:
        """
        Create a comprehensive content plan for a topic.
        
        Args:
            topic: Main topic for content plan
            num_articles: Number of articles to include in the plan
            
        Returns:
            Dict: Content plan
        """
        logger.info(f"Creating content plan for topic: {topic} with {num_articles} articles")
        
        try:
            # Analyze topic
            topic_analysis = self.analyze_topic(topic)
            
            # Extract subtopics and keywords
            subtopics = topic_analysis.get("subtopics", [])
            primary_keywords = topic_analysis.get("primary_keywords", [])
            related_keywords = topic_analysis.get("related_keywords", [])
            
            # Create pillar content plan
            pillar_content = {
                "title": f"The Complete Guide to {topic.title()}",
                "type": "pillar",
                "target_keyword": topic,
                "description": f"Comprehensive guide covering all aspects of {topic}",
                "estimated_word_count": 3000,
                "sections": [
                    {"heading": f"What is {topic.title()}", "word_count": 300},
                    {"heading": f"Why {topic.title()} Matters", "word_count": 300},
                    {"heading": f"Types of {topic.title()}", "word_count": 500},
                    {"heading": f"How to Choose the Right {topic.title()}", "word_count": 500},
                    {"heading": f"Top {topic.title()} Options", "word_count": 800},
                    {"heading": f"{topic.title()} Tips and Best Practices", "word_count": 400},
                    {"heading": f"Common {topic.title()} Mistakes to Avoid", "word_count": 300},
                    {"heading": f"{topic.title()} FAQs", "word_count": 400}
                ],
                "monetization": "multiple_affiliate_links"
            }
            
            # Create cluster content plans
            cluster_content = []
            
            # Calculate how many articles to create per content type
            import math
            num_how_to = math.ceil(num_articles * 0.3)  # 30% how-to guides
            num_reviews = math.ceil(num_articles * 0.3)  # 30% reviews
            num_list = math.ceil(num_articles * 0.2)     # 20% listicles
            num_comparison = num_articles - num_how_to - num_reviews - num_list  # remaining for comparisons
            
            # Create how-to articles
            for i in range(min(num_how_to, len(subtopics))):
                if i < len(subtopics):
                    subtopic = subtopics[i]
                    cluster_content.append({
                        "title": f"How to {subtopic.title()}: Step-by-Step Guide",
                        "type": "how_to",
                        "target_keyword": f"how to {subtopic}",
                        "description": f"Step-by-step guide on how to {subtopic}",
                        "estimated_word_count": 1800,
                        "sections": [
                            {"heading": f"Why Learn How to {subtopic.title()}", "word_count": 200},
                            {"heading": "What You'll Need", "word_count": 200},
                            {"heading": "Step 1", "word_count": 200},
                            {"heading": "Step 2", "word_count": 200},
                            {"heading": "Step 3", "word_count": 200},
                            {"heading": "Step 4", "word_count": 200},
                            {"heading": "Step 5", "word_count": 200},
                            {"heading": f"Tips for Success with {subtopic.title()}", "word_count": 200},
                            {"heading": "Troubleshooting Common Issues", "word_count": 200},
                            {"heading": "Conclusion", "word_count": 200}
                        ],
                        "monetization": "product_recommendations"
                    })
            
            # Create review articles
            for i in range(min(num_reviews, len(primary_keywords))):
                if i < len(primary_keywords):
                    keyword = primary_keywords[i]
                    if "best" not in keyword and "top" not in keyword:
                        keyword = f"best {keyword}"
                    cluster_content.append({
                        "title": f"{keyword.title()}: Complete Review & Buying Guide",
                        "type": "review",
                        "target_keyword": keyword,
                        "description": f"Comprehensive review and buying guide for {keyword}",
                        "estimated_word_count": 2000,
                        "sections": [
                            {"heading": "Introduction", "word_count": 200},
                            {"heading": "Top Picks at a Glance", "word_count": 200},
                            {"heading": "How We Evaluated", "word_count": 200},
                            {"heading": "Best Overall: Product Name", "word_count": 300},
                            {"heading": "Best Budget Option: Product Name", "word_count": 300},
                            {"heading": "Best Premium Choice: Product Name", "word_count": 300},
                            {"heading": "Best for Beginners: Product Name", "word_count": 300},
                            {"heading": "Buying Guide: What to Look For", "word_count": 300},
                            {"heading": "Frequently Asked Questions", "word_count": 200}
                        ],
                        "monetization": "affiliate_product_reviews"
                    })
            
            # Create list articles
            for i in range(min(num_list, len(related_keywords))):
                if i < len(related_keywords):
                    keyword = related_keywords[i]
                    if not any(x in keyword for x in ["tips", "ideas", "examples", "ways"]):
                        keyword = f"{topic} tips"
                    cluster_content.append({
                        "title": f"10 Essential {keyword.title()} You Need to Know",
                        "type": "listicle",
                        "target_keyword": keyword,
                        "description": f"Essential list of {keyword} with expert insights",
                        "estimated_word_count": 1500,
                        "sections": [
                            {"heading": "Introduction", "word_count": 200},
                            {"heading": "Why These Tips Matter", "word_count": 100},
                            {"heading": "#1", "word_count": 120},
                            {"heading": "#2", "word_count": 120},
                            {"heading": "#3", "word_count": 120},
                            {"heading": "#4", "word_count": 120},
                            {"heading": "#5", "word_count": 120},
                            {"heading": "#6", "word_count": 120},
                            {"heading": "#7", "word_count": 120},
                            {"heading": "#8", "word_count": 120},
                            {"heading": "#9", "word_count": 120},
                            {"heading": "#10", "word_count": 120},
                            {"heading": "Conclusion", "word_count": 120}
                        ],
                        "monetization": "affiliate_links_per_item"
                    })
            
            # Create comparison articles
            for i in range(min(num_comparison, len(primary_keywords) - 1)):
                if i + 1 < len(primary_keywords):
                    keyword1 = primary_keywords[i]
                    keyword2 = primary_keywords[i + 1]
                    cluster_content.append({
                        "title": f"{keyword1.title()} vs {keyword2.title()}: Which is Better?",
                        "type": "comparison",
                        "target_keyword": f"{keyword1} vs {keyword2}",
                        "description": f"Detailed comparison of {keyword1} and {keyword2} to help you decide",
                        "estimated_word_count": 1800,
                        "sections": [
                            {"heading": "Introduction", "word_count": 200},
                            {"heading": "Quick Comparison", "word_count": 200},
                            {"heading": f"About {keyword1.title()}", "word_count": 200},
                            {"heading": f"About {keyword2.title()}", "word_count": 200},
                            {"heading": "Features Comparison", "word_count": 300},
                            {"heading": "Performance", "word_count": 200},
                            {"heading": "Pricing", "word_count": 200},
                            {"heading": "Pros and Cons", "word_count": 200},
                            {"heading": "Which Should You Choose?", "word_count": 200},
                            {"heading": "Conclusion", "word_count": 100}
                        ],
                        "monetization": "affiliate_links_for_both"
                    })
            
            # Create content calendar
            import datetime
            start_date = datetime.datetime.now()
            calendar = []
            
            # Add pillar content first
            calendar.append({
                "content": pillar_content,
                "publish_date": start_date.strftime("%Y-%m-%d"),
                "status": "planned"
            })
            
            # Add cluster content
            for i, content in enumerate(cluster_content):
                publish_date = start_date + datetime.timedelta(days=(i + 1) * 7)  # Weekly publishing
                calendar.append({
                    "content": content,
                    "publish_date": publish_date.strftime("%Y-%m-%d"),
                    "status": "planned"
                })
            
            # Create final content plan
            content_plan = {
                "topic": topic,
                "pillar_content": pillar_content,
                "cluster_content": cluster_content,
                "content_calendar": calendar,
                "estimated_total_word_count": pillar_content["estimated_word_count"] + sum(c["estimated_word_count"] for c in cluster_content),
                "total_articles": 1 + len(cluster_content)  # Pillar + cluster
            }
            
            logger.info(f"Successfully created content plan for topic: {topic}")
            return content_plan
            
        except Exception as e:
            logger.error(f"Error creating content plan: {str(e)}")
            return {
                "topic": topic,
                "error": str(e),
                "pillar_content": {},
                "cluster_content": [],
                "content_calendar": []
            }
    
    def _generate_subtopics(self, topic: str, keyword_data: Dict[str, Any]) -> List[str]:
        """
        Generate subtopics from keyword data.
        
        Args:
            topic: Main topic
            keyword_data: Keyword data from comprehensive analysis
            
        Returns:
            List: List of subtopics
        """
        subtopics = []
        
        # Extract from keyword ideas
        for keyword in keyword_data.get("keyword_ideas", []):
            kw_text = keyword.get("text", "")
            if kw_text and kw_text != topic and len(kw_text.split()) >= 2:
                subtopics.append(kw_text)
        
        # Extract from common phrases
        for phrase in keyword_data.get("serp_analysis", {}).get("common_phrases", []):
            phrase_text = phrase.get("phrase", "")
            if phrase_text and phrase_text != topic and len(phrase_text.split()) >= 2:
                subtopics.append(phrase_text)
        
        # Extract from related keywords
        for keyword in keyword_data.get("related_keywords", []):
            kw_text = keyword.get("text", "")
            if kw_text and kw_text != topic and len(kw_text.split()) >= 2:
                subtopics.append(kw_text)
        
        # Remove duplicates
        subtopics = list(dict.fromkeys(subtopics))
        
        # Sort by relevance (length as a simple proxy)
        subtopics.sort(key=len)
        
        return subtopics[:20]  # Return top 20
    
    def _analyze_competition(self, urls: List[str]) -> Dict[str, Any]:
        """
        Analyze competition based on top-ranking URLs.
        
        Args:
            urls: List of top-ranking URLs
            
        Returns:
            Dict: Competition analysis
        """
        if not urls:
            return {
                "competition_level": "unknown",
                "content_gaps": [],
                "content_length": {"min": 0, "max": 0, "avg": 0},
                "domain_authority": "unknown"
            }
        
        # In a real implementation, we would fetch and analyze each URL
        # For now, we'll return simplified mock data
        
        # Mock data
        return {
            "competition_level": "medium",  # low, medium, high
            "content_gaps": [
                "Detailed how-to guides",
                "Video tutorials",
                "Case studies",
                "Expert interviews"
            ],
            "content_length": {
                "min": 1200,
                "max": 3500,
                "avg": 2100
            },
            "domain_authority": "mixed",  # low, medium, high, mixed
            "note": "This is simplified competition analysis. In a real implementation, each URL would be fetched and analyzed."
        }
    
    def _generate_content_recommendations(
        self,
        topic: str,
        subtopics: List[str],
        keyword_data: Dict[str, Any],
        competition_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate content recommendations based on analysis.
        
        Args:
            topic: Main topic
            subtopics: List of subtopics
            keyword_data: Keyword data
            competition_analysis: Competition analysis
            
        Returns:
            Dict: Content recommendations
        """
        # Content type recommendation based on competition level
        competition_level = competition_analysis.get("competition_level", "medium")
        
        content_types = []
        if competition_level == "high":
            content_types = ["long-form guides", "detailed case studies", "expert roundups", "original research"]
        elif competition_level == "medium":
            content_types = ["how-to guides", "listicles", "reviews", "comparisons"]
        else:  # low
            content_types = ["basic guides", "listicles", "news", "quick tips"]
        
        # Word count recommendation based on competition
        content_length = competition_analysis.get("content_length", {})
        avg_length = content_length.get("avg", 1500)
        
        if competition_level == "high":
            recommended_length = max(avg_length + 500, 2500)
        elif competition_level == "medium":
            recommended_length = max(avg_length, 1800)
        else:  # low
            recommended_length = 1200
        
        # Extract content gaps
        content_gaps = competition_analysis.get("content_gaps", [])
        
        # Generate content ideas based on subtopics
        content_ideas = []
        
        # How-to ideas
        how_to_ideas = [f"How to {subtopic}" for subtopic in subtopics[:5]]
        
        # List ideas
        list_subtopics = subtopics[5:10] if len(subtopics) > 5 else subtopics
        list_ideas = [f"10 Best {subtopic} Tips" for subtopic in list_subtopics]
        
        # Guide ideas
        guide_subtopics = subtopics[10:15] if len(subtopics) > 10 else subtopics
        guide_ideas = [f"The Complete Guide to {subtopic}" for subtopic in guide_subtopics]
        
        # Combine ideas
        content_ideas = how_to_ideas + list_ideas + guide_ideas
        
        # Create recommendations
        recommendations = {
            "recommended_content_types": content_types,
            "recommended_word_count": recommended_length,
            "content_gaps_to_address": content_gaps,
            "content_ideas": content_ideas,
            "pillar_topic": topic,
            "cluster_topics": subtopics[:10]
        }
        
        return recommendations
