"""
SERP Analyzer service for analyzing search engine results pages.
"""
import logging
import re
import time
import random
import json
from typing import Dict, Any, List, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote_plus

from app.config import settings

logger = logging.getLogger(__name__)

class SerpAnalyzerService:
    """
    Service for analyzing search engine results pages (SERPs).
    This service scrapes and analyzes top-ranking content for keywords.
    """
    
    def __init__(self):
        """Initialize the SERP analyzer service."""
        self.use_mock_data = settings.USE_MOCK_DATA
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        ]
        self.proxies = settings.SCRAPING_PROXIES or {}
    
    def analyze_serp(self, keyword: str, num_results: int = 10) -> Dict[str, Any]:
        """
        Analyze search results for a keyword.
        
        Args:
            keyword: Keyword to analyze
            num_results: Number of results to analyze
            
        Returns:
            Dict: SERP analysis results
        """
        logger.info(f"Analyzing SERP for keyword: {keyword}")
        
        if self.use_mock_data:
            return self._get_mock_serp_analysis(keyword, num_results)
        
        try:
            # Get search results
            search_results = self._get_search_results(keyword, num_results)
            
            # Analyze search results
            analysis = {
                "keyword": keyword,
                "num_results": len(search_results),
                "results": search_results,
                "common_words": self._extract_common_words(search_results),
                "common_phrases": self._extract_common_phrases(search_results),
                "title_patterns": self._analyze_title_patterns(search_results),
                "content_structure": self._analyze_content_structure(search_results),
                "content_length": self._analyze_content_length(search_results),
                "domains": self._analyze_domains(search_results)
            }
            
            logger.info(f"Completed SERP analysis for: {keyword}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing SERP: {str(e)}")
            return self._get_mock_serp_analysis(keyword, num_results)
    
    def analyze_competing_content(self, url: str) -> Dict[str, Any]:
        """
        Analyze a specific competing piece of content.
        
        Args:
            url: URL of the competing content
            
        Returns:
            Dict: Content analysis results
        """
        logger.info(f"Analyzing competing content: {url}")
        
        if self.use_mock_data:
            return self._get_mock_content_analysis(url)
        
        try:
            # Fetch the content
            content = self._fetch_url_content(url)
            if not content:
                logger.error(f"Failed to fetch content from {url}")
                return self._get_mock_content_analysis(url)
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract title
            title = soup.title.string if soup.title else ""
            
            # Extract main content (this is a simplistic approach)
            main_content = ""
            article = soup.find('article') or soup.find('main') or soup.find('div', {'class': ['content', 'main', 'post']})
            if article:
                main_content = article.get_text(separator=' ', strip=True)
            else:
                # Fallback: clean all text
                main_content = soup.get_text(separator=' ', strip=True)
            
            # Extract headings
            headings = []
            for i in range(1, 7):
                for heading in soup.find_all(f'h{i}'):
                    headings.append({
                        "level": i,
                        "text": heading.get_text(strip=True)
                    })
            
            # Extract links
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                # Only add absolute links or internal links that aren't empty
                if href and (href.startswith('http') or (href.startswith('/') and not href == '/')):
                    links.append({
                        "url": href,
                        "text": text,
                        "is_external": href.startswith('http') and not url.startswith(urlparse(url).netloc)
                    })
            
            # Extract images
            images = []
            for img in soup.find_all('img', src=True):
                src = img['src']
                alt = img.get('alt', '')
                images.append({
                    "src": src,
                    "alt": alt
                })
            
            # Word count
            word_count = len(main_content.split())
            
            # Extract meta data
            meta_description = ""
            meta_tags = soup.find_all('meta')
            for tag in meta_tags:
                if tag.get('name') == 'description' or tag.get('property') == 'og:description':
                    meta_description = tag.get('content', '')
                    break
            
            # Create analysis result
            analysis = {
                "url": url,
                "title": title,
                "meta_description": meta_description,
                "word_count": word_count,
                "headings": headings,
                "links_count": len(links),
                "external_links_count": sum(1 for link in links if link.get('is_external', False)),
                "images_count": len(images),
                "has_schema": bool(soup.find_all('script', {'type': 'application/ld+json'})),
                "sample_content": main_content[:500] + "..." if len(main_content) > 500 else main_content,
                "content_structure": {
                    "headings": headings,
                    "paragraphs": len(soup.find_all('p')),
                    "lists": len(soup.find_all(['ul', 'ol'])),
                    "tables": len(soup.find_all('table')),
                    "images": len(images)
                }
            }
            
            logger.info(f"Completed competing content analysis for: {url}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing competing content: {str(e)}")
            return self._get_mock_content_analysis(url)
    
    def _get_search_results(self, keyword: str, num_results: int = 10) -> List[Dict[str, Any]]:
        """
        Get search results for a keyword.
        
        Args:
            keyword: Keyword to search for
            num_results: Number of results to retrieve
            
        Returns:
            List: Search results
        """
        encoded_query = quote_plus(keyword)
        url = f"https://www.google.com/search?q={encoded_query}&num={num_results}"
        
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1",
        }
        
        # Add a delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        # Make the request
        response = requests.get(url, headers=headers, proxies=self.proxies)
        
        if response.status_code != 200:
            logger.error(f"Failed to get search results: {response.status_code}")
            return []
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract search results (this may need adjustment based on Google's current HTML structure)
        results = []
        for result in soup.select('div.g'):
            try:
                title_element = result.select_one('h3')
                link_element = result.select_one('a')
                snippet_element = result.select_one('div.VwiC3b')
                
                if title_element and link_element and link_element.has_attr('href'):
                    title = title_element.get_text(strip=True)
                    link = link_element['href']
                    snippet = snippet_element.get_text(strip=True) if snippet_element else ""
                    
                    # Filter out non-http links and google links
                    if link.startswith('http') and 'google.com' not in link:
                        results.append({
                            "title": title,
                            "url": link,
                            "snippet": snippet
                        })
            except Exception as e:
                logger.error(f"Error parsing search result: {str(e)}")
        
        return results[:num_results]
    
    def _fetch_url_content(self, url: str) -> Optional[str]:
        """
        Fetch content from a URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            Optional[str]: HTML content or None if failed
        """
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
        }
        
        # Add a delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        try:
            response = requests.get(url, headers=headers, proxies=self.proxies, timeout=10)
            
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"Failed to fetch URL: {url}, status code: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {str(e)}")
            return None
    
    def _extract_common_words(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract common words from search results.
        
        Args:
            search_results: List of search results
            
        Returns:
            List: List of common words with frequencies
        """
        from collections import Counter
        import string
        import re
        
        # Combine all text from titles and snippets
        all_text = ""
        for result in search_results:
            all_text += f" {result.get('title', '')} {result.get('snippet', '')}"
        
        # Clean text
        all_text = all_text.lower()
        all_text = re.sub(r'[^\w\s]', ' ', all_text)
        
        # Split into words and count
        words = all_text.split()
        
        # Filter out common stop words
        stop_words = {'the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your', 'all', 'have', 'new', 'more', 'an', 'was', 'we', 'will', 'home', 'can', 'us', 'about'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count frequency
        word_counts = Counter(filtered_words)
        
        # Convert to list of dicts
        result = [{"word": word, "count": count} for word, count in word_counts.most_common(30)]
        
        return result
    
    def _extract_common_phrases(self, search_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract common phrases from search results.
        
        Args:
            search_results: List of search results
            
        Returns:
            List: List of common phrases with frequencies
        """
        from collections import Counter
        import re
        
        # Combine all text from titles and snippets
        all_text = ""
        for result in search_results:
            all_text += f" {result.get('title', '')} {result.get('snippet', '')}"
        
        # Clean text
        all_text = all_text.lower()
        all_text = re.sub(r'[^\w\s]', ' ', all_text)
        
        # Extract 2 and 3 word phrases
        words = all_text.split()
        phrases = []
        
        # Add 2-word phrases
        for i in range(len(words) - 1):
            phrases.append(f"{words[i]} {words[i+1]}")
        
        # Add 3-word phrases
        for i in range(len(words) - 2):
            phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
        
        # Filter out phrases with stop words at the beginning
        stop_words = {'the', 'and', 'to', 'of', 'a', 'in', 'for', 'is', 'on', 'that', 'by', 'this', 'with', 'i', 'you', 'it', 'not', 'or', 'be', 'are', 'from', 'at', 'as', 'your', 'all', 'have', 'new', 'more', 'an', 'was', 'we', 'will', 'home', 'can', 'us', 'about'}
        filtered_phrases = [phrase for phrase in phrases if phrase.split()[0] not in stop_words]
        
        # Count frequency
        phrase_counts = Counter(filtered_phrases)
        
        # Convert to list of dicts
        result = [{"phrase": phrase, "count": count} for phrase, count in phrase_counts.most_common(20)]
        
        return result
    
    def _analyze_title_patterns(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze title patterns in search results.
        
        Args:
            search_results: List of search results
            
        Returns:
            Dict: Analysis of title patterns
        """
        titles = [result.get('title', '') for result in search_results if result.get('title')]
        if not titles:
            return {}
        
        # Analyze title lengths
        title_lengths = [len(title) for title in titles]
        avg_title_length = sum(title_lengths) / len(title_lengths)
        
        # Check for common patterns
        patterns = {
            "has_number": sum(1 for title in titles if any(char.isdigit() for char in title)),
            "has_question": sum(1 for title in titles if '?' in title),
            "has_year": sum(1 for title in titles if re.search(r'20[12][0-9]', title)),
            "has_brackets": sum(1 for title in titles if '[' in title and ']' in title),
            "has_parentheses": sum(1 for title in titles if '(' in title and ')' in title),
            "starts_with_how": sum(1 for title in titles if title.lower().startswith('how')),
            "starts_with_why": sum(1 for title in titles if title.lower().startswith('why')),
            "starts_with_what": sum(1 for title in titles if title.lower().startswith('what')),
            "starts_with_number": sum(1 for title in titles if re.match(r'^\d+', title)),
            "has_colon": sum(1 for title in titles if ':' in title),
        }
        
        # Calculate percentages
        result = {
            "avg_title_length": avg_title_length,
            "max_title_length": max(title_lengths),
            "min_title_length": min(title_lengths),
            "patterns": {k: {"count": v, "percentage": (v / len(titles)) * 100} for k, v in patterns.items()}
        }
        
        return result
    
    def _analyze_content_structure(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze content structure from search results (simplified version).
        In a real implementation, this would fetch and analyze each page.
        
        Args:
            search_results: List of search results
            
        Returns:
            Dict: Content structure analysis
        """
        # In a real implementation, we would fetch and analyze each URL
        # For now, we'll return a simplified analysis based on snippets
        
        snippets = [result.get('snippet', '') for result in search_results if result.get('snippet')]
        if not snippets:
            return {}
        
        # Analyze snippet length as a proxy for content density
        snippet_lengths = [len(snippet) for snippet in snippets]
        avg_snippet_length = sum(snippet_lengths) / len(snippet_lengths)
        
        # Check for indicators of content type
        indicators = {
            "list_indicator": sum(1 for s in snippets if any(x in s.lower() for x in ['top ', 'best ', '10 ', 'ways to', 'tips', 'steps'])),
            "how_to_indicator": sum(1 for s in snippets if 'how to' in s.lower()),
            "question_indicator": sum(1 for s in snippets if '?' in s),
            "comparison_indicator": sum(1 for s in snippets if any(x in s.lower() for x in [' vs ', 'versus', 'compared to'])),
            "review_indicator": sum(1 for s in snippets if 'review' in s.lower()),
        }
        
        result = {
            "avg_snippet_length": avg_snippet_length,
            "content_type_indicators": {k: {"count": v, "percentage": (v / len(snippets)) * 100} for k, v in indicators.items()}
        }
        
        return result
    
    def _analyze_content_length(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Estimate content length from search results.
        This is a placeholder - in a real implementation, we would fetch and analyze each page.
        
        Args:
            search_results: List of search results
            
        Returns:
            Dict: Content length analysis
        """
        # A very rough estimate based on snippet length
        snippets = [result.get('snippet', '') for result in search_results if result.get('snippet')]
        
        if not snippets:
            return {"estimated_avg_word_count": 0}
        
        # Very rough estimate: average snippet length * 30 as a multiplier
        avg_snippet_length = sum(len(snippet.split()) for snippet in snippets) / len(snippets)
        estimated_word_count = int(avg_snippet_length * 30)
        
        return {
            "estimated_avg_word_count": estimated_word_count,
            "estimation_method": "rough_estimate_from_snippets",
            "note": "This is a very rough estimate. For accurate word counts, each page should be fetched and analyzed."
        }
    
    def _analyze_domains(self, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze domains in search results.
        
        Args:
            search_results: List of search results
            
        Returns:
            Dict: Domain analysis
        """
        from collections import Counter
        
        domains = []
        for result in search_results:
            url = result.get('url', '')
            if url:
                try:
                    domain = urlparse(url).netloc
                    domains.append(domain)
                except:
                    pass
        
        if not domains:
            return {}
        
        # Count domain frequency
        domain_counts = Counter(domains)
        
        # Get domain types
        domain_types = {
            "com": sum(1 for d in domains if d.endswith('.com')),
            "org": sum(1 for d in domains if d.endswith('.org')),
            "net": sum(1 for d in domains if d.endswith('.net')),
            "edu": sum(1 for d in domains if d.endswith('.edu')),
            "gov": sum(1 for d in domains if d.endswith('.gov')),
        }
        
        result = {
            "top_domains": [{"domain": domain, "count": count} for domain, count in domain_counts.most_common(5)],
            "domain_types": {k: {"count": v, "percentage": (v / len(domains)) * 100} for k, v in domain_types.items() if v > 0},
            "unique_domains": len(domain_counts)
        }
        
        return result
    
    def _get_mock_serp_analysis(self, keyword: str, num_results: int = 10) -> Dict[str, Any]:
        """
        Get mock SERP analysis for development and testing.
        
        Args:
            keyword: Keyword to analyze
            num_results: Number of results to include
            
        Returns:
            Dict: Mock SERP analysis
        """
        logger.info(f"Using mock data for SERP analysis of: {keyword}")
        
        # Generate mock search results
        search_results = []
        for i in range(min(num_results, 10)):
            domain = f"example{i}.com"
            search_results.append({
                "title": f"Best {keyword} guide for beginners in 2023" if i == 0 else f"{keyword.title()} tips and tricks {i+1}",
                "url": f"https://{domain}/blog/{keyword.replace(' ', '-')}-{i+1}",
                "snippet": f"Looking for the best {keyword}? Our comprehensive guide covers everything you need to know about {keyword}, including top tips, expert advice, and product recommendations."
            })
        
        # Generate mock common words
        common_words = [
            {"word": keyword.split()[0] if len(keyword.split()) > 0 else keyword, "count": 45},
            {"word": "best", "count": 38},
            {"word": "guide", "count": 32},
            {"word": "tips", "count": 28},
            {"word": "review", "count": 25},
            {"word": "top", "count": 23},
            {"word": "how", "count": 20},
            {"word": "expert", "count": 18},
            {"word": "products", "count": 15},
            {"word": "recommend", "count": 12},
        ]
        
        # Generate mock common phrases
        common_phrases = [
            {"phrase": f"best {keyword}", "count": 15},
            {"phrase": f"{keyword} guide", "count": 12},
            {"phrase": f"how to {keyword}", "count": 10},
            {"phrase": f"{keyword} for beginners", "count": 8},
            {"phrase": f"top {keyword} tips", "count": 7},
            {"phrase": f"{keyword} reviews", "count": 6},
            {"phrase": f"best {keyword} for", "count": 5},
            {"phrase": f"how to choose", "count": 4},
            {"phrase": f"ultimate guide", "count": 3},
            {"phrase": f"complete guide", "count": 2},
        ]
        
        # Mock title patterns
        title_patterns = {
            "avg_title_length": 45.5,
            "max_title_length": 65,
            "min_title_length": 30,
            "patterns": {
                "has_number": {"count": 6, "percentage": 60.0},
                "has_question": {"count": 2, "percentage": 20.0},
                "has_year": {"count": 4, "percentage": 40.0},
                "has_brackets": {"count": 1, "percentage": 10.0},
                "has_parentheses": {"count": 2, "percentage": 20.0},
                "starts_with_how": {"count": 3, "percentage": 30.0},
                "starts_with_why": {"count": 1, "percentage": 10.0},
                "starts_with_what": {"count": 1, "percentage": 10.0},
                "starts_with_number": {"count": 2, "percentage": 20.0},
                "has_colon": {"count": 3, "percentage": 30.0},
            }
        }
        
        # Mock content structure
        content_structure = {
            "avg_snippet_length": 120.5,
            "content_type_indicators": {
                "list_indicator": {"count": 6, "percentage": 60.0},
                "how_to_indicator": {"count": 5, "percentage": 50.0},
                "question_indicator": {"count": 3, "percentage": 30.0},
                "comparison_indicator": {"count": 2, "percentage": 20.0},
                "review_indicator": {"count": 4, "percentage": 40.0},
            }
        }
        
        # Mock content length
        content_length = {
            "estimated_avg_word_count": 1500,
            "estimation_method": "mock_data",
            "note": "This is mock data. For accurate word counts, each page should be fetched and analyzed."
        }
        
        # Mock domain analysis
        domains = {
            "top_domains": [
                {"domain": "example0.com", "count": 1},
                {"domain": "example1.com", "count": 1},
                {"domain": "example2.com", "count": 1},
                {"domain": "example3.com", "count": 1},
                {"domain": "example4.com", "count": 1},
            ],
            "domain_types": {
                "com": {"count": 8, "percentage": 80.0},
                "org": {"count": 1, "percentage": 10.0},
                "net": {"count": 1, "percentage": 10.0},
            },
            "unique_domains": 10
        }
        
        # Combine all mock data
        return {
            "keyword": keyword,
            "num_results": len(search_results),
            "results": search_results,
            "common_words": common_words,
            "common_phrases": common_phrases,
            "title_patterns": title_patterns,
            "content_structure": content_structure,
            "content_length": content_length,
            "domains": domains
        }
    
    def _get_mock_content_analysis(self, url: str) -> Dict[str, Any]:
        """
        Get mock content analysis for development and testing.
        
        Args:
            url: URL of the content to analyze
            
        Returns:
            Dict: Mock content analysis
        """
        logger.info(f"Using mock data for content analysis of: {url}")
        
        # Extract domain from URL
        try:
            domain = urlparse(url).netloc
        except:
            domain = "example.com"
        
        # Extract topic from URL path
        try:
            path = urlparse(url).path
            topic = path.split('/')[-1].replace('-', ' ').title()
        except:
            topic = "Sample Topic"
        
        # Mock headings
        headings = [
            {"level": 1, "text": f"{topic} Guide: Everything You Need to Know"},
            {"level": 2, "text": f"What is {topic}?"},
            {"level": 2, "text": f"Benefits of {topic}"},
            {"level": 2, "text": f"How to Choose the Best {topic}"},
            {"level": 3, "text": "Key Features to Look For"},
            {"level": 3, "text": "Price Considerations"},
            {"level": 2, "text": f"Top 5 {topic} Products"},
            {"level": 3, "text": "Budget Option"},
            {"level": 3, "text": "Premium Choice"},
            {"level": 2, "text": "Frequently Asked Questions"},
            {"level": 2, "text": "Conclusion"},
        ]
        
        # Mock analysis data
        return {
            "url": url,
            "title": f"{topic} Guide: Everything You Need to Know",
            "meta_description": f"Discover everything about {topic} in our comprehensive guide. Learn about benefits, features, and find the best products for your needs.",
            "word_count": 1850,
            "headings": headings,
            "links_count": 24,
            "external_links_count": 8,
            "images_count": 6,
            "has_schema": True,
            "sample_content": f"Welcome to our comprehensive guide on {topic}. In this article, we'll cover everything you need to know about {topic}, from basic definitions to advanced tips and product recommendations. Whether you're a beginner or an experienced user, you'll find valuable information to help you make informed decisions...",
            "content_structure": {
                "headings": headings,
                "paragraphs": 25,
                "lists": 4,
                "tables": 1,
                "images": 6
            }
        }
