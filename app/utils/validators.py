"""
Validation utilities for the SEO Blog Builder application.
"""
import re
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

def validate_client_requirements(requirements: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate client requirements for completeness and consistency.
    
    Args:
        requirements: Client requirements dictionary
        
    Returns:
        Tuple[bool, List[str]]: Validation result and list of issues
    """
    issues = []
    
    # Check for required fields
    required_fields = [
        "audience", 
        "content", 
        "monetization", 
        "branding", 
        "technical"
    ]
    
    for field in required_fields:
        if field not in requirements:
            issues.append(f"Missing required field: {field}")
    
    # Check audience definition
    if "audience" in requirements:
        audience = requirements["audience"]
        if "primary" not in audience:
            issues.append("Missing primary audience definition")
        elif "demographics" not in audience["primary"]:
            issues.append("Missing primary audience demographics")
    
    # Check content requirements
    if "content" in requirements:
        content = requirements["content"]
        if "primary_topics" not in content or not content["primary_topics"]:
            issues.append("Missing primary content topics")
    
    # Check monetization strategy
    if "monetization" in requirements:
        monetization = requirements["monetization"]
        if "primary_strategy" not in monetization:
            issues.append("Missing primary monetization strategy")
    
    # Check technical requirements
    if "technical" in requirements:
        technical = requirements["technical"]
        if "platform" not in technical:
            issues.append("Missing technical platform preference")
    
    # Check for logical consistency
    if "monetization" in requirements and "content" in requirements:
        monetization = requirements["monetization"]
        content = requirements["content"]
        
        # If affiliate marketing is the primary strategy, ensure content types are suitable
        if monetization.get("primary_strategy") == "affiliate_marketing":
            suitable_content_types = ["product_reviews", "comparisons", "buying_guides"]
            found_suitable = False
            
            for content_type in suitable_content_types:
                if content_type in str(content):
                    found_suitable = True
                    break
            
            if not found_suitable:
                issues.append("Affiliate marketing strategy requires appropriate content types (reviews, comparisons, guides)")
    
    is_valid = len(issues) == 0
    return is_valid, issues

def validate_email(email: str) -> bool:
    """
    Validate an email address.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if the email is valid, False otherwise
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def validate_domain(domain: str) -> bool:
    """
    Validate a domain name.
    
    Args:
        domain: Domain name to validate
        
    Returns:
        bool: True if the domain is valid, False otherwise
    """
    domain_pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return bool(re.match(domain_pattern, domain))

def validate_keyword_list(keywords: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate a list of keywords for SEO.
    
    Args:
        keywords: List of keywords to validate
        
    Returns:
        Tuple[bool, List[str]]: Validation result and list of issues
    """
    issues = []
    
    if not keywords:
        issues.append("Keyword list is empty")
        return False, issues
    
    for i, keyword in enumerate(keywords):
        # Check for minimum length
        if len(keyword) < 3:
            issues.append(f"Keyword {i+1} '{keyword}' is too short (minimum 3 characters)")
        
        # Check for maximum length (typical long-tail keyword shouldn't be extremely long)
        if len(keyword) > 100:
            issues.append(f"Keyword {i+1} is too long (maximum 100 characters)")
        
        # Check for special characters that aren't typically used in search
        if re.search(r'[^a-zA-Z0-9\s\-\'\"\&\+\,\.]', keyword):
            issues.append(f"Keyword {i+1} '{keyword}' contains unusual special characters")
    
    # Check for duplicate keywords
    if len(keywords) != len(set(keywords)):
        issues.append("Keyword list contains duplicates")
    
    is_valid = len(issues) == 0
    return is_valid, issues

def validate_content_brief(brief: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a content brief.
    
    Args:
        brief: Content brief dictionary
        
    Returns:
        Tuple[bool, List[str]]: Validation result and list of issues
    """
    issues = []
    
    # Check for required fields
    required_fields = ["title", "primary_keyword", "content_type", "target_audience", "word_count"]
    
    for field in required_fields:
        if field not in brief:
            issues.append(f"Missing required field: {field}")
    
    # Validate title
    if "title" in brief:
        title = brief["title"]
        if len(title) < 10:
            issues.append("Title is too short (minimum 10 characters)")
        elif len(title) > 100:
            issues.append("Title is too long (maximum 100 characters)")
    
    # Validate word count
    if "word_count" in brief:
        word_count = brief["word_count"]
        try:
            word_count = int(word_count)
            if word_count < 300:
                issues.append("Word count is too low (minimum 300 words)")
            elif word_count > 10000:
                issues.append("Word count is too high (maximum 10,000 words)")
        except (ValueError, TypeError):
            issues.append("Word count must be a number")
    
    # Validate keywords
    if "secondary_keywords" in brief and brief["secondary_keywords"]:
        if isinstance(brief["secondary_keywords"], list):
            valid, keyword_issues = validate_keyword_list(brief["secondary_keywords"])
            if not valid:
                issues.extend(keyword_issues)
        else:
            issues.append("Secondary keywords must be a list")
    
    is_valid = len(issues) == 0
    return is_valid, issues
