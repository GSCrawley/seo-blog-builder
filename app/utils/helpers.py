"""
Helper functions for the SEO Blog Builder application.
"""
import os
import json
import string
import random
import re
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)

def load_prompt_template(template_name: str) -> str:
    """
    Load a prompt template from the prompts directory.
    
    Args:
        template_name: Name of the template file
        
    Returns:
        str: Content of the template file
    """
    template_path = os.path.join(settings.PROMPT_TEMPLATES_DIR, template_name)
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Template file not found: {template_path}")
        return ""
    except Exception as e:
        logger.error(f"Error loading template {template_name}: {str(e)}")
        return ""

def generate_project_id() -> str:
    """
    Generate a unique project ID.
    
    Returns:
        str: Unique project ID
    """
    timestamp = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"PRJ-{timestamp}-{random_str}"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to be safe for filesystem operations.
    
    Args:
        filename: The filename to sanitize
        
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in filename if c in valid_chars)
    
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    
    return sanitized

def extract_keywords_from_text(text: str, min_length: int = 3) -> List[str]:
    """
    Extract potential keywords from text.
    
    Args:
        text: The text to extract keywords from
        min_length: Minimum length of words to consider
        
    Returns:
        List[str]: List of potential keywords
    """
    # Basic implementation - would be enhanced with NLP in a real system
    words = re.findall(r'\b[a-zA-Z]{%d,}\b' % min_length, text.lower())
    # Remove duplicates while preserving order
    return list(dict.fromkeys(words))

def merge_dictionaries(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary
        
    Returns:
        Dict[str, Any]: Merged dictionary
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dictionaries(result[key], value)
        else:
            result[key] = value
            
    return result

def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory
    """
    os.makedirs(directory_path, exist_ok=True)

def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Format a number as currency.
    
    Args:
        amount: The amount to format
        currency: Currency code
        
    Returns:
        str: Formatted currency string
    """
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"
