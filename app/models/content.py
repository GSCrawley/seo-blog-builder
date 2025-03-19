"""
Content model for database.
"""
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLAEnum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base

class ContentType(str, Enum):
    """Enum for content types"""
    BLOG_POST = "blog_post"
    PRODUCT_REVIEW = "product_review"
    COMPARISON = "comparison"
    GUIDE = "guide"
    LISTICLE = "listicle"
    HOW_TO = "how_to"
    NEWS = "news"
    CASE_STUDY = "case_study"
    LANDING_PAGE = "landing_page"
    ABOUT_PAGE = "about_page"
    CATEGORY_PAGE = "category_page"
    PILLAR_PAGE = "pillar_page"
    HOMEPAGE = "homepage"

class ContentStatus(str, Enum):
    """Enum for content status"""
    PLANNED = "planned"
    DRAFTING = "drafting"
    REVIEW = "review"
    READY = "ready"
    PUBLISHED = "published"
    UPDATED = "updated"
    ARCHIVED = "archived"

class ContentItem(Base):
    """Content item model representing a piece of content created by the system."""
    __tablename__ = "content_items"

    id = Column(String, primary_key=True, index=True, default=lambda: f"CONTENT-{uuid.uuid4().hex[:8].upper()}")
    project_id = Column(String, ForeignKey("projects.id"))
    static_site_id = Column(String, ForeignKey("static_sites.id"))
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    content_type = Column(SQLAEnum(ContentType), default=ContentType.BLOG_POST)
    status = Column(SQLAEnum(ContentStatus), default=ContentStatus.PLANNED)
    
    # Summary and content fields
    summary = Column(Text, nullable=True)
    markdown_content = Column(Text, nullable=True)  # Markdown/MDX content
    html_content = Column(Text, nullable=True)  # Generated HTML content
    
    # File structure information
    content_path = Column(String, nullable=True)  # Path in the static site filesystem
    assets_directory = Column(String, nullable=True)  # Directory for content assets
    
    # SEO and metadata fields
    word_count = Column(Integer, nullable=True)
    primary_keyword = Column(String, nullable=True)
    secondary_keywords = Column(JSON, nullable=True)  # List of secondary keywords
    meta_title = Column(String, nullable=True)
    meta_description = Column(String, nullable=True)
    frontmatter = Column(JSON, nullable=True)  # Frontmatter metadata for the content
    
    # Organization fields
    categories = Column(JSON, nullable=True)  # List of categories
    tags = Column(JSON, nullable=True)  # List of tags
    
    # Media fields
    featured_image = Column(String, nullable=True)
    featured_image_alt = Column(String, nullable=True)
    images = Column(JSON, nullable=True)  # List of images used in the content
    
    # Author and attribution
    author = Column(String, nullable=True)
    
    # Affiliate and monetization
    affiliate_products = Column(JSON, nullable=True)  # List of affiliate products featured
    affiliate_disclosure = Column(Text, nullable=True)  # Disclosure text for this content
    
    # Link management
    internal_links = Column(JSON, nullable=True)  # List of internal links
    external_links = Column(JSON, nullable=True)  # List of external links
    
    # Content structure
    table_of_contents = Column(JSON, nullable=True)  # Auto-generated TOC
    content_structure = Column(JSON, nullable=True)  # Headings and sections structure
    
    # Pillar/cluster content
    is_pillar = Column(Boolean, default=False)
    pillar_id = Column(String, nullable=True)  # ID of the pillar content if this is a cluster content
    
    # Timestamps
    publish_date = Column(DateTime(timezone=True), nullable=True)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    
    # Analytics and metrics
    seo_score = Column(Integer, nullable=True)
    readability_score = Column(Integer, nullable=True)
    
    # Metadata
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="content_items")
    static_site = relationship("StaticSite", back_populates="content_items")
    
    def __repr__(self):
        return f"<ContentItem {self.id}: {self.title}>"
