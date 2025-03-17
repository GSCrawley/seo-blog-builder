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
    DRAFT = "draft"
    REVIEW = "review"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    UPDATED = "updated"
    ARCHIVED = "archived"

class ContentItem(Base):
    """Content item model representing a piece of content created by the system."""
    __tablename__ = "content_items"

    id = Column(String, primary_key=True, index=True, default=lambda: f"CONTENT-{uuid.uuid4().hex[:8].upper()}")
    project_id = Column(String, ForeignKey("projects.id"))
    website_id = Column(String, ForeignKey("websites.id"))
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    content_type = Column(SQLAEnum(ContentType), default=ContentType.BLOG_POST)
    status = Column(SQLAEnum(ContentStatus), default=ContentStatus.PLANNED)
    summary = Column(Text, nullable=True)
    body = Column(Text, nullable=True)
    word_count = Column(Integer, nullable=True)
    primary_keyword = Column(String, nullable=True)
    secondary_keywords = Column(JSON, nullable=True)  # List of secondary keywords
    meta_title = Column(String, nullable=True)
    meta_description = Column(String, nullable=True)
    categories = Column(JSON, nullable=True)  # List of categories
    tags = Column(JSON, nullable=True)  # List of tags
    featured_image = Column(String, nullable=True)
    author = Column(String, nullable=True)
    affiliate_products = Column(JSON, nullable=True)  # List of affiliate products featured
    internal_links = Column(JSON, nullable=True)  # List of internal links
    external_links = Column(JSON, nullable=True)  # List of external links
    is_pillar = Column(Boolean, default=False)
    pillar_id = Column(String, nullable=True)  # ID of the pillar content if this is a cluster content
    publish_date = Column(DateTime(timezone=True), nullable=True)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    seo_score = Column(Integer, nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="content_items")
    website = relationship("Website", back_populates="content_items")
    
    def __repr__(self):
        return f"<ContentItem {self.id}: {self.title}>"
