"""
SEO service as the main interface for SEO operations.
"""
import logging
from typing import Dict, Any, List, Optional

from app.services.seo.free_tools import SeoDataAggregator
from app.config import settings

logger = logging.getLogger(__name__)

class SeoService:
    """
    Main service interface for SEO operations.
    This service provides access to all SEO tools and functionality.
    """
    
    def __init__(self):
        """Initialize the SEO service."""
        self.seo_aggregator = SeoDataAggregator()
    
    def research_keywords(self, topic: str) -> Dict[str, Any]:
        """
        Research keywords for a topic.
        
        Args:
            topic: Topic to research keywords for
            
        Returns:
            Dict: Keyword research results
        """
        logger.info(f"Researching keywords for topic: {topic}")
        
        try:
            # Get comprehensive keyword data
            keyword_data = self.seo_aggregator.get_comprehensive_keyword_data(topic)
            
            return {
                "topic": topic,
                "keyword_ideas": keyword_data.get("keyword_ideas", []),
                "related_keywords": keyword_data.get("related_keywords", []),
                "common_phrases": keyword_data.get("serp_analysis", {}).get("common_phrases", []),
                "top_ranking_urls": keyword_data.get("top_ranking_urls", [])
            }
            
        except Exception as e:
            logger.error(f"Error researching keywords: {str(e)}")
            return {
                "topic": topic,
                "error": str(e),
                "keyword_ideas": [],
                "related_keywords": [],
                "common_phrases": [],
                "top_ranking_urls": []
            }
    
    def create_content_plan(self, topic: str, num_articles: int = 10) -> Dict[str, Any]:
        """
        Create a content plan for a topic.
        
        Args:
            topic: Topic to create a content plan for
            num_articles: Number of articles to include in the plan
            
        Returns:
            Dict: Content plan
        """
        logger.info(f"Creating content plan for topic: {topic}")
        
        try:
            # Create content plan
            content_plan = self.seo_aggregator.create_content_plan(topic, num_articles)
            
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
    
    def analyze_competition(self, topic: str) -> Dict[str, Any]:
        """
        Analyze competition for a topic.
        
        Args:
            topic: Topic to analyze competition for
            
        Returns:
            Dict: Competition analysis
        """
        logger.info(f"Analyzing competition for topic: {topic}")
        
        try:
            # Analyze topic
            topic_analysis = self.seo_aggregator.analyze_topic(topic)
            
            # Extract competition analysis
            competition = topic_analysis.get("competition", {})
            
            return {
                "topic": topic,
                "competition_level": competition.get("analysis", {}).get("competition_level", "unknown"),
                "content_gaps": competition.get("analysis", {}).get("content_gaps", []),
                "top_competitors": competition.get("top_urls", []),
                "content_length": competition.get("analysis", {}).get("content_length", {}),
                "domain_authority": competition.get("analysis", {}).get("domain_authority", "unknown")
            }
            
        except Exception as e:
            logger.error(f"Error analyzing competition: {str(e)}")
            return {
                "topic": topic,
                "error": str(e),
                "competition_level": "unknown",
                "content_gaps": [],
                "top_competitors": [],
                "content_length": {},
                "domain_authority": "unknown"
            }
    
    def optimize_content(self, content: str, target_keyword: str) -> Dict[str, Any]:
        """
        Optimize content for a target keyword.
        
        Args:
            content: Content to optimize
            target_keyword: Target keyword to optimize for
            
        Returns:
            Dict: Optimization recommendations
        """
        logger.info(f"Optimizing content for keyword: {target_keyword}")
        
        try:
            # Analyze content with NLP
            content_analysis = self.seo_aggregator.nlp_analyzer.analyze_text(content)
            
            # Get keyword data
            keyword_data = self.seo_aggregator.get_comprehensive_keyword_data(target_keyword)
            
            # Check keyword presence
            keyword_present = target_keyword.lower() in content.lower()
            keyword_in_first_para = target_keyword.lower() in content.lower().split("\n")[0]
            
            # Check for related keywords
            related_keywords = [kw.get("text", "").lower() for kw in keyword_data.get("related_keywords", [])]
            included_related = [kw for kw in related_keywords if kw in content.lower()]
            
            # Calculate keyword density
            words = content.lower().split()
            keyword_count = content.lower().count(target_keyword.lower())
            keyword_density = (keyword_count / len(words)) * 100 if words else 0
            
            # Check headings (simplified)
            import re
            headings = re.findall(r'#+\s+(.*)', content)
            keyword_in_headings = sum(1 for h in headings if target_keyword.lower() in h.lower())
            
            # Check content length
            min_recommended_length = 1000
            ideal_length = 1500
            content_length = len(words)
            length_assessment = "too_short" if content_length < min_recommended_length else "good" if content_length >= ideal_length else "adequate"
            
            # Generate recommendations
            recommendations = []
            
            if not keyword_present:
                recommendations.append("Add the target keyword to the content")
            
            if not keyword_in_first_para:
                recommendations.append("Include the target keyword in the first paragraph")
            
            if keyword_in_headings == 0:
                recommendations.append("Include the target keyword in at least one heading")
            
            if keyword_density < 0.5:
                recommendations.append("Increase keyword density slightly (aim for 0.5-2%)")
            elif keyword_density > 3:
                recommendations.append("Reduce keyword density (currently too high)")
            
            if len(included_related) < 3:
                recommendations.append("Include more related keywords to improve semantic relevance")
            
            if content_length < min_recommended_length:
                recommendations.append(f"Increase content length to at least {min_recommended_length} words")
            
            if "flesch_reading_ease" in content_analysis.get("readability", {}) and content_analysis["readability"]["flesch_reading_ease"] < 40:
                recommendations.append("Simplify language to improve readability")
            
            # Create optimization result
            optimization = {
                "target_keyword": target_keyword,
                "content_length": content_length,
                "keyword_present": keyword_present,
                "keyword_in_first_paragraph": keyword_in_first_para,
                "keyword_in_headings": keyword_in_headings > 0,
                "keyword_density": round(keyword_density, 2),
                "related_keywords_included": included_related,
                "related_keywords_missing": [kw for kw in related_keywords[:10] if kw not in included_related],
                "readability": content_analysis.get("readability", {}),
                "length_assessment": length_assessment,
                "recommendations": recommendations,
                "optimization_score": self._calculate_optimization_score(
                    keyword_present,
                    keyword_in_first_para,
                    keyword_in_headings > 0,
                    0.5 <= keyword_density <= 3,
                    len(included_related) >= 3,
                    content_length >= min_recommended_length
                )
            }
            
            logger.info(f"Content optimization completed for keyword: {target_keyword}")
            return optimization
            
        except Exception as e:
            logger.error(f"Error optimizing content: {str(e)}")
            return {
                "target_keyword": target_keyword,
                "error": str(e),
                "recommendations": ["Error analyzing content"],
                "optimization_score": 0
            }
    
    def _calculate_optimization_score(
        self,
        keyword_present: bool,
        keyword_in_first_para: bool,
        keyword_in_headings: bool,
        good_keyword_density: bool,
        has_related_keywords: bool,
        good_length: bool
    ) -> int:
        """
        Calculate content optimization score.
        
        Args:
            keyword_present: Whether target keyword is present
            keyword_in_first_para: Whether target keyword is in first paragraph
            keyword_in_headings: Whether target keyword is in headings
            good_keyword_density: Whether keyword density is good
            has_related_keywords: Whether related keywords are included
            good_length: Whether content length is good
            
        Returns:
            int: Optimization score (0-100)
        """
        score = 0
        
        # Essential factors
        if keyword_present:
            score += 20
        
        if keyword_in_first_para:
            score += 15
        
        if keyword_in_headings:
            score += 15
        
        # Important factors
        if good_keyword_density:
            score += 15
        
        if has_related_keywords:
            score += 15
        
        if good_length:
            score += 20
        
        return score
    
    def generate_meta_tags(self, title: str, content: str, target_keyword: str) -> Dict[str, str]:
        """
        Generate SEO meta tags for content.
        
        Args:
            title: Content title
            content: Content body
            target_keyword: Target keyword
            
        Returns:
            Dict: Generated meta tags
        """
        logger.info(f"Generating meta tags for content: {title}")
        
        try:
            # Extract first paragraph or first 200 characters
            paragraphs = content.split('\n\n')
            first_para = paragraphs[0] if paragraphs else content[:200]
            
            # Clean and truncate
            import re
            first_para = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', first_para)
            
            # Generate meta description
            meta_description = first_para
            if len(meta_description) > 155:
                meta_description = meta_description[:155].rsplit(' ', 1)[0] + '...'
            
            # Ensure target keyword is in meta description
            if target_keyword.lower() not in meta_description.lower():
                # Try to add it naturally
                if len(meta_description) < 120:
                    meta_description += f" Learn more about {target_keyword}."
                else:
                    # Replace part of the description to include keyword
                    words = meta_description.split()
                    if len(words) > 5:
                        start_phrase = ' '.join(words[:3])
                        middle_replacement = f" {target_keyword} "
                        end_phrase = ' '.join(words[4:])
                        meta_description = start_phrase + middle_replacement + end_phrase
            
            # Generate meta title
            meta_title = title
            
            # Ensure target keyword is in meta title
            if target_keyword.lower() not in meta_title.lower():
                # Try to add it naturally
                if len(meta_title) < 50:
                    meta_title += f" - {target_keyword.title()}"
                else:
                    # Create new title
                    meta_title = f"{target_keyword.title()}: {title[:40]}..."
            
            # Truncate meta title if too long
            if len(meta_title) > 60:
                meta_title = meta_title[:60].rsplit(' ', 1)[0] + '...'
            
            # Extract keywords
            import string
            words = content.lower().translate(str.maketrans('', '', string.punctuation)).split()
            
            # Count word frequency
            from collections import Counter
            word_counts = Counter(words)
            
            # Remove common stop words
            stop_words = {'the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it'}
            for stop_word in stop_words:
                if stop_word in word_counts:
                    del word_counts[stop_word]
            
            # Get top keywords
            keywords = [kw for kw, _ in word_counts.most_common(5)]
            
            # Ensure target keyword is included
            if target_keyword.lower() not in keywords:
                keywords.insert(0, target_keyword.lower())
            
            # Format keywords
            meta_keywords = ', '.join(keywords)
            
            return {
                "title": meta_title,
                "description": meta_description,
                "keywords": meta_keywords
            }
            
        except Exception as e:
            logger.error(f"Error generating meta tags: {str(e)}")
            return {
                "title": title,
                "description": f"Learn about {target_keyword} in this comprehensive guide.",
                "keywords": target_keyword
            }
    
    def suggest_internal_links(self, content: str, site_content: List[Dict[str, Any]], max_links: int = 5) -> List[Dict[str, Any]]:
        """
        Suggest internal links for content.
        
        Args:
            content: Content to suggest links for
            site_content: List of existing site content
            max_links: Maximum number of links to suggest
            
        Returns:
            List: Suggested internal links
        """
        logger.info(f"Suggesting internal links for content")
        
        try:
            # Extract content keywords
            content_analysis = self.seo_aggregator.nlp_analyzer.analyze_text(content)
            content_keywords = [kw["word"] for kw in content_analysis.get("keywords", [])]
            
            # Match keywords with existing content
            suggestions = []
            
            for article in site_content:
                title = article.get("title", "")
                url = article.get("url", "")
                keywords = article.get("keywords", [])
                
                if not title or not url:
                    continue
                
                # Check for keyword matches
                matches = set(content_keywords) & set(keywords)
                
                if matches:
                    suggestions.append({
                        "title": title,
                        "url": url,
                        "matching_keywords": list(matches),
                        "relevance_score": len(matches)
                    })
            
            # Sort by relevance score
            suggestions.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return suggestions[:max_links]
            
        except Exception as e:
            logger.error(f"Error suggesting internal links: {str(e)}")
            return []
    
    def analyze_url(self, url: str) -> Dict[str, Any]:
        """
        Analyze a URL for SEO factors.
        
        Args:
            url: URL to analyze
            
        Returns:
            Dict: URL analysis
        """
        logger.info(f"Analyzing URL: {url}")
        
        try:
            # Parse URL
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            
            # Extract parts
            domain = parsed_url.netloc
            path = parsed_url.path
            
            # Analyze path
            path_segments = [segment for segment in path.split('/') if segment]
            path_length = len(path)
            has_keyword_in_path = any(len(segment) > 3 for segment in path_segments)
            
            # Check URL structure
            is_clean_url = (
                '?' not in url and  # No query parameters
                '__' not in url and  # No double underscores
                not any(c.isupper() for c in url)  # No uppercase letters
            )
            
            # Slugify check
            import re
            has_special_chars = bool(re.search(r'[^a-z0-9\-/\.]', url.lower()))
            
            return {
                "url": url,
                "domain": domain,
                "path": path,
                "path_segments": path_segments,
                "path_length": path_length,
                "has_keyword_in_path": has_keyword_in_path,
                "is_clean_url": is_clean_url,
                "has_special_chars": has_special_chars,
                "is_seo_friendly": is_clean_url and not has_special_chars,
                "recommendations": self._get_url_recommendations(
                    url, is_clean_url, has_special_chars, path_length, has_keyword_in_path
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing URL: {str(e)}")
            return {
                "url": url,
                "error": str(e),
                "is_seo_friendly": False,
                "recommendations": ["Error analyzing URL"]
            }
    
    def _get_url_recommendations(
        self,
        url: str,
        is_clean_url: bool,
        has_special_chars: bool,
        path_length: int,
        has_keyword_in_path: bool
    ) -> List[str]:
        """
        Get URL recommendations.
        
        Args:
            url: URL to get recommendations for
            is_clean_url: Whether URL is clean
            has_special_chars: Whether URL has special characters
            path_length: Length of URL path
            has_keyword_in_path: Whether URL path contains keywords
            
        Returns:
            List: URL recommendations
        """
        recommendations = []
        
        if not is_clean_url:
            recommendations.append("Remove query parameters and use clean URL structure")
        
        if has_special_chars:
            recommendations.append("Remove special characters from URL")
        
        if path_length > 100:
            recommendations.append("Shorten URL path (too long)")
        
        if not has_keyword_in_path:
            recommendations.append("Include relevant keywords in URL path")
        
        if any(c.isupper() for c in url):
            recommendations.append("Use lowercase letters in URL")
        
        return recommendations
