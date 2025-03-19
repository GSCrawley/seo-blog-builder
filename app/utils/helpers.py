"""
Helper utilities for the SEO Blog Builder application.
"""
import re
import unicodedata
import os
import json
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

def slugify(text: str) -> str:
    """
    Create a URL-friendly slug from text.
    
    Args:
        text: Text to convert to slug
        
    Returns:
        str: URL-friendly slug
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove accents and normalize
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    
    # Replace any non-word character with a space
    text = re.sub(r'[^\w\s-]', ' ', text)
    
    # Replace spaces with hyphens
    text = re.sub(r'[-\s]+', '-', text).strip('-_')
    
    return text

def safe_json_loads(json_str: str, default_value: Any = None) -> Any:
    """
    Safely load JSON string.
    
    Args:
        json_str: JSON string to load
        default_value: Default value to return if loading fails
        
    Returns:
        Any: Loaded JSON data or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default_value if default_value is not None else {}

def truncate_text(text: str, max_length: int, add_ellipsis: bool = True) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        add_ellipsis: Whether to add ellipsis if truncated
        
    Returns:
        str: Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    # Truncate at the last space before max_length to avoid cutting words
    truncated = text[:max_length].rsplit(' ', 1)[0]
    
    if add_ellipsis:
        truncated += '...'
    
    return truncated

def clean_html(html: str) -> str:
    """
    Remove HTML tags from text.
    
    Args:
        html: HTML text to clean
        
    Returns:
        str: Clean text without HTML tags
    """
    # Simple HTML tag removal (for basic cases)
    clean = re.sub(r'<[^>]*>', '', html)
    
    # Replace multiple spaces with a single space
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    return clean

def create_directory_if_not_exists(path: str) -> bool:
    """
    Create a directory if it doesn't exist.
    
    Args:
        path: Directory path
        
    Returns:
        bool: True if directory exists or was created, False otherwise
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except Exception as e:
        logger.error(f"Error creating directory {path}: {str(e)}")
        return False

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename to make it safe for file systems.
    
    Args:
        filename: Filename to sanitize
        
    Returns:
        str: Sanitized filename
    """
    # Replace invalid characters
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Ensure it's not empty
    if not filename:
        filename = "file"
    
    return filename
