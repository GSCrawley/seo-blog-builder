"""
WordPress site generation service.
"""
import os
import json
import logging
import requests
from typing import Dict, Any, List, Optional
from requests.auth import HTTPBasicAuth

from app.config import settings

logger = logging.getLogger(__name__)

class WordPressService:
    """
    Service for creating and managing WordPress sites.
    """
    
    def __init__(self, site_key: str = "default"):
        """
        Initialize the WordPress service with site configuration.
        
        Args:
            site_key: Key for the WordPress site in the wp-sites.json configuration
        """
        if site_key not in settings.WP_SITES:
            logger.error(f"WordPress site configuration not found for key: {site_key}")
            raise ValueError(f"WordPress site configuration not found for key: {site_key}")
            
        self.site_config = settings.WP_SITES[site_key]
        self.api_url = self.site_config["URL"].rstrip("/") + "/wp-json/wp/v2"
        self.username = self.site_config["USER"]
        self.password = self.site_config["PASS"]
        self.auth = HTTPBasicAuth(self.username, self.password)
        
    def create_post(self, title: str, content: str, excerpt: str = "", 
                   status: str = "draft", categories: List[int] = None, 
                   tags: List[int] = None, featured_media_id: int = None) -> Dict[str, Any]:
        """
        Create a new WordPress post.
        
        Args:
            title: Post title
            content: Post content (can include HTML)
            excerpt: Optional post excerpt
            status: Post status (draft, publish, pending, future)
            categories: List of category IDs
            tags: List of tag IDs
            featured_media_id: ID of the featured image
            
        Returns:
            Dict: The created post data returned from WordPress
        """
        logger.info(f"Creating WordPress post: {title}")
        
        # Prepare post data
        post_data = {
            "title": title,
            "content": content,
            "status": status
        }
        
        if excerpt:
            post_data["excerpt"] = excerpt
            
        if categories:
            post_data["categories"] = categories
            
        if tags:
            post_data["tags"] = tags
            
        if featured_media_id:
            post_data["featured_media"] = featured_media_id
        
        # Send request to WordPress API
        try:
            response = requests.post(
                f"{self.api_url}/posts",
                json=post_data,
                auth=self.auth
            )
            response.raise_for_status()
            logger.info(f"WordPress post created successfully: {title}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating WordPress post: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"API Response: {e.response.text}")
            raise
    
    def upload_media(self, file_path: str, title: str = None) -> Dict[str, Any]:
        """
        Upload media to WordPress.
        
        Args:
            file_path: Path to the media file
            title: Optional title for the media
            
        Returns:
            Dict: The uploaded media data returned from WordPress
        """
        logger.info(f"Uploading media to WordPress: {file_path}")
        
        # Get filename and MIME type
        filename = os.path.basename(file_path)
        mime_type = self._get_mime_type(filename)
        
        # Prepare form data
        with open(file_path, 'rb') as file:
            files = {'file': (filename, file, mime_type)}
            data = {}
            
            if title:
                data['title'] = title
        
            # Send request to WordPress API
            try:
                response = requests.post(
                    f"{self.api_url}/media",
                    files=files,
                    data=data,
                    auth=self.auth
                )
                response.raise_for_status()
                logger.info(f"Media uploaded successfully: {filename}")
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error uploading media: {str(e)}")
                if hasattr(e, 'response') and e.response:
                    logger.error(f"API Response: {e.response.text}")
                raise
    
    def create_category(self, name: str, description: str = "", parent: int = 0) -> Dict[str, Any]:
        """
        Create a new WordPress category.
        
        Args:
            name: Category name
            description: Optional category description
            parent: Parent category ID (0 for top-level category)
            
        Returns:
            Dict: The created category data returned from WordPress
        """
        logger.info(f"Creating WordPress category: {name}")
        
        # Prepare category data
        category_data = {
            "name": name,
            "description": description,
            "parent": parent
        }
        
        # Send request to WordPress API
        try:
            response = requests.post(
                f"{self.api_url}/categories",
                json=category_data,
                auth=self.auth
            )
            response.raise_for_status()
            logger.info(f"WordPress category created successfully: {name}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating WordPress category: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"API Response: {e.response.text}")
            raise
    
    def create_tag(self, name: str, description: str = "") -> Dict[str, Any]:
        """
        Create a new WordPress tag.
        
        Args:
            name: Tag name
            description: Optional tag description
            
        Returns:
            Dict: The created tag data returned from WordPress
        """
        logger.info(f"Creating WordPress tag: {name}")
        
        # Prepare tag data
        tag_data = {
            "name": name,
            "description": description
        }
        
        # Send request to WordPress API
        try:
            response = requests.post(
                f"{self.api_url}/tags",
                json=tag_data,
                auth=self.auth
            )
            response.raise_for_status()
            logger.info(f"WordPress tag created successfully: {name}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating WordPress tag: {str(e)}")
            if hasattr(e, 'response') and e.response:
                logger.error(f"API Response: {e.response.text}")
            raise
    
    def setup_blog(self, blog_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set up a complete blog with categories, tags, and initial posts.
        
        Args:
            blog_data: Dictionary containing blog setup data
            
        Returns:
            Dict: Status information and created resource IDs
        """
        logger.info("Setting up WordPress blog")
        
        result = {
            "status": "success",
            "categories": {},
            "tags": {},
            "posts": []
        }
        
        try:
            # Create categories
            for category in blog_data.get("categories", []):
                created_category = self.create_category(
                    name=category["name"],
                    description=category.get("description", ""),
                    parent=category.get("parent", 0)
                )
                result["categories"][category["name"]] = created_category["id"]
            
            # Create tags
            for tag in blog_data.get("tags", []):
                created_tag = self.create_tag(
                    name=tag["name"],
                    description=tag.get("description", "")
                )
                result["tags"][tag["name"]] = created_tag["id"]
            
            # Create posts
            for post in blog_data.get("posts", []):
                # Map category and tag names to IDs
                category_ids = [result["categories"][cat] for cat in post.get("categories", []) if cat in result["categories"]]
                tag_ids = [result["tags"][tag] for tag in post.get("tags", []) if tag in result["tags"]]
                
                # Create post
                created_post = self.create_post(
                    title=post["title"],
                    content=post["content"],
                    excerpt=post.get("excerpt", ""),
                    status=post.get("status", "draft"),
                    categories=category_ids,
                    tags=tag_ids
                )
                result["posts"].append({
                    "id": created_post["id"],
                    "title": created_post["title"]["rendered"],
                    "link": created_post["link"]
                })
            
            logger.info("WordPress blog setup completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error setting up WordPress blog: {str(e)}")
            result["status"] = "error"
            result["error"] = str(e)
            return result
    
    def _get_mime_type(self, filename: str) -> str:
        """
        Get the MIME type for a file based on its extension.
        
        Args:
            filename: The filename
            
        Returns:
            str: The MIME type
        """
        ext = os.path.splitext(filename)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.zip': 'application/zip',
            '.mp3': 'audio/mpeg',
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.wmv': 'video/x-ms-wmv',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml'
        }
        return mime_types.get(ext, 'application/octet-stream')
