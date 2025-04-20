"""
WordPress tools for CrewAI agents.
"""
from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

from app.config import settings
from app.services.site_generation.wordpress_service import WordPressService

class CreatePostInput(BaseModel):
    """Input for WordPress Create Post Tool."""
    site_key: str = Field(description="Key for the WordPress site in configuration")
    title: str = Field(description="Post title")
    content: str = Field(description="Post content (can include HTML)")
    excerpt: str = Field(default="", description="Optional post excerpt")
    status: str = Field(default="draft", description="Post status (draft, publish, pending, future)")
    categories: List[int] = Field(default=[], description="List of category IDs")
    tags: List[int] = Field(default=[], description="List of tag IDs")
    featured_media_id: Optional[int] = Field(default=None, description="ID of the featured image")

class CreatePostTool(BaseTool):
    """Tool for creating posts in WordPress."""
    name: str = "WordPress Create Post Tool"
    description: str = "Creates a new post in WordPress with specified title, content, and metadata."
    args_schema: Type[BaseModel] = CreatePostInput
    
    def _run(self, site_key: str, title: str, content: str, excerpt: str = "", 
             status: str = "draft", categories: List[int] = None, 
             tags: List[int] = None, featured_media_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Create a post in WordPress.
        
        Args:
            site_key: Key for the WordPress site in configuration
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
        wp_service = WordPressService(site_key=site_key)
        
        # Use empty lists if None is provided
        if categories is None:
            categories = []
        if tags is None:
            tags = []
        
        # Create post
        post = wp_service.create_post(
            title=title,
            content=content,
            excerpt=excerpt,
            status=status,
            categories=categories,
            tags=tags,
            featured_media_id=featured_media_id
        )
        
        return post

class CreateCategoryInput(BaseModel):
    """Input for WordPress Create Category Tool."""
    site_key: str = Field(description="Key for the WordPress site in configuration")
    name: str = Field(description="Category name")
    description: str = Field(default="", description="Category description")
    parent: int = Field(default=0, description="Parent category ID (0 for top-level category)")

class CreateCategoryTool(BaseTool):
    """Tool for creating categories in WordPress."""
    name: str = "WordPress Create Category Tool"
    description: str = "Creates a new category in WordPress."
    args_schema: Type[BaseModel] = CreateCategoryInput
    
    def _run(self, site_key: str, name: str, description: str = "", parent: int = 0) -> Dict[str, Any]:
        """
        Create a category in WordPress.
        
        Args:
            site_key: Key for the WordPress site in configuration
            name: Category name
            description: Category description
            parent: Parent category ID (0 for top-level category)
            
        Returns:
            Dict: The created category data returned from WordPress
        """
        wp_service = WordPressService(site_key=site_key)
        
        # Create category
        category = wp_service.create_category(
            name=name,
            description=description,
            parent=parent
        )
        
        return category

class CreateTagInput(BaseModel):
    """Input for WordPress Create Tag Tool."""
    site_key: str = Field(description="Key for the WordPress site in configuration")
    name: str = Field(description="Tag name")
    description: str = Field(default="", description="Tag description")

class CreateTagTool(BaseTool):
    """Tool for creating tags in WordPress."""
    name: str = "WordPress Create Tag Tool"
    description: str = "Creates a new tag in WordPress."
    args_schema: Type[BaseModel] = CreateTagInput
    
    def _run(self, site_key: str, name: str, description: str = "") -> Dict[str, Any]:
        """
        Create a tag in WordPress.
        
        Args:
            site_key: Key for the WordPress site in configuration
            name: Tag name
            description: Tag description
            
        Returns:
            Dict: The created tag data returned from WordPress
        """
        wp_service = WordPressService(site_key=site_key)
        
        # Create tag
        tag = wp_service.create_tag(
            name=name,
            description=description
        )
        
        return tag

class UploadMediaInput(BaseModel):
    """Input for WordPress Upload Media Tool."""
    site_key: str = Field(description="Key for the WordPress site in configuration")
    file_path: str = Field(description="Path to the media file")
    title: Optional[str] = Field(default=None, description="Optional title for the media")

class UploadMediaTool(BaseTool):
    """Tool for uploading media to WordPress."""
    name: str = "WordPress Upload Media Tool"
    description: str = "Uploads media to WordPress."
    args_schema: Type[BaseModel] = UploadMediaInput
    
    def _run(self, site_key: str, file_path: str, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload media to WordPress.
        
        Args:
            site_key: Key for the WordPress site in configuration
            file_path: Path to the media file
            title: Optional title for the media
            
        Returns:
            Dict: The uploaded media data returned from WordPress
        """
        wp_service = WordPressService(site_key=site_key)
        
        # Upload media
        media = wp_service.upload_media(
            file_path=file_path,
            title=title
        )
        
        return media

class SetupBlogInput(BaseModel):
    """Input for WordPress Setup Blog Tool."""
    site_key: str = Field(description="Key for the WordPress site in configuration")
    blog_data: Dict[str, Any] = Field(description="Blog setup data including categories, tags, and posts")

class SetupBlogTool(BaseTool):
    """Tool for setting up a complete blog in WordPress."""
    name: str = "WordPress Setup Blog Tool"
    description: str = "Sets up a complete blog in WordPress with categories, tags, and initial posts."
    args_schema: Type[BaseModel] = SetupBlogInput
    
    def _run(self, site_key: str, blog_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set up a complete blog in WordPress.
        
        Args:
            site_key: Key for the WordPress site in configuration
            blog_data: Blog setup data including categories, tags, and posts
            
        Returns:
            Dict: Status information and created resource IDs
        """
        wp_service = WordPressService(site_key=site_key)
        
        # Set up blog
        result = wp_service.setup_blog(blog_data=blog_data)
        
        return result
