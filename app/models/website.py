"""
Website model for database.
"""
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLAEnum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base

class WebsiteStatus(str, Enum):
    """Enum for website status"""
    PLANNING = "planning"
    DEVELOPMENT = "development"
    STAGING = "staging"
    LIVE = "live"
    MAINTENANCE = "maintenance"
    ARCHIVED = "archived"

class Website(Base):
    """Website model representing a blog site created by the system."""
    __tablename__ = "websites"

    id = Column(String, primary_key=True, index=True, default=lambda: f"SITE-{uuid.uuid4().hex[:8].upper()}")
    project_id = Column(String, ForeignKey("projects.id"))
    domain = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLAEnum(WebsiteStatus), default=WebsiteStatus.PLANNING)
    niche = Column(String, nullable=True)
    primary_keywords = Column(JSON, nullable=True)  # List of primary keywords
    hosting_provider = Column(String, nullable=True)
    wordpress_url = Column(String, nullable=True)
    admin_url = Column(String, nullable=True)
    admin_username = Column(String, nullable=True)
    has_staging = Column(Boolean, default=False)
    staging_url = Column(String, nullable=True)
    theme = Column(String, nullable=True)
    plugins = Column(JSON, nullable=True)  # List of plugins
    google_analytics_id = Column(String, nullable=True)
    search_console_verified = Column(Boolean, default=False)
    ssl_enabled = Column(Boolean, default=True)
    page_speed_score = Column(Integer, nullable=True)
    metadata = Column(JSON, nullable=True)
    launch_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="websites")
    content_items = relationship("ContentItem", back_populates="website")
    
    def __repr__(self):
        return f"<Website {self.id}: {self.domain}>"
