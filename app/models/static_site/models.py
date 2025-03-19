"""
Database models for static site generation approach.
These models replace the WordPress-specific website models.
"""
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLAEnum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base

class SiteStatus(str, Enum):
    """Enum for static site status"""
    PLANNING = "planning"
    GENERATING_CONTENT = "generating_content"
    BUILDING = "building"
    DEPLOYING = "deploying"
    LIVE = "live"
    UPDATING = "updating"
    ARCHIVED = "archived"
    FAILED = "failed"

class DeploymentProvider(str, Enum):
    """Enum for deployment providers"""
    VERCEL = "vercel"
    NETLIFY = "netlify"
    GITHUB_PAGES = "github_pages"
    CLOUDFLARE_PAGES = "cloudflare_pages"
    CUSTOM = "custom"

class StaticSite(Base):
    """Static site model representing a blog created by the system."""
    __tablename__ = "static_sites"

    id = Column(String, primary_key=True, index=True, default=lambda: f"SITE-{uuid.uuid4().hex[:8].upper()}")
    project_id = Column(String, ForeignKey("projects.id"))
    domain = Column(String, nullable=True)  # Can be null if using default subdomain
    subdomain = Column(String, nullable=False)  # e.g., 'tech-blog' in tech-blog.ourplatform.com
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLAEnum(SiteStatus), default=SiteStatus.PLANNING)
    niche = Column(String, nullable=True)
    primary_keywords = Column(JSON, nullable=True)  # List of primary keywords
    
    # Template information
    template_id = Column(String, nullable=True)
    template_config = Column(JSON, nullable=True)  # Template configuration options
    color_scheme = Column(JSON, nullable=True)  # Color scheme configuration
    font_settings = Column(JSON, nullable=True)  # Font configuration
    
    # Deployment information
    deployment_provider = Column(SQLAEnum(DeploymentProvider), default=DeploymentProvider.VERCEL)
    deployment_id = Column(String, nullable=True)  # ID from the deployment provider
    deployment_url = Column(String, nullable=True)  # URL from the deployment provider
    last_deployed = Column(DateTime(timezone=True), nullable=True)
    
    # Build information
    repository_url = Column(String, nullable=True)  # Git repository URL
    build_settings = Column(JSON, nullable=True)  # Build configuration
    
    # SEO and tracking
    google_analytics_id = Column(String, nullable=True)
    search_console_verified = Column(Boolean, default=False)
    seo_settings = Column(JSON, nullable=True)  # SEO configuration
    ssl_enabled = Column(Boolean, default=True)
    
    # Site metadata
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    project = relationship("Project", back_populates="static_sites")
    content_items = relationship("ContentItem", back_populates="static_site")
    deployments = relationship("Deployment", back_populates="static_site")
    
    def __repr__(self):
        return f"<StaticSite {self.id}: {self.title}>"

class Deployment(Base):
    """Deployment model for tracking site deployments."""
    __tablename__ = "deployments"

    id = Column(String, primary_key=True, index=True, default=lambda: f"DEPLOY-{uuid.uuid4().hex[:8].upper()}")
    static_site_id = Column(String, ForeignKey("static_sites.id"))
    version = Column(String, nullable=False)  # Semantic version or timestamp-based version
    deployed_at = Column(DateTime(timezone=True), default=func.now())
    status = Column(String, nullable=False, default="success")  # success, failed, in_progress
    deployment_url = Column(String, nullable=True)
    deployment_logs = Column(Text, nullable=True)
    is_production = Column(Boolean, default=True)
    built_by = Column(String, nullable=True)  # User or system that triggered the build
    commit_hash = Column(String, nullable=True)  # Git commit hash if applicable
    build_time = Column(Integer, nullable=True)  # Build time in seconds
    metadata = Column(JSON, nullable=True)

    # Relationships
    static_site = relationship("StaticSite", back_populates="deployments")
    
    def __repr__(self):
        return f"<Deployment {self.id}: {self.version}>"

class SiteTemplate(Base):
    """Site template model for blog templates."""
    __tablename__ = "site_templates"

    id = Column(String, primary_key=True, index=True, default=lambda: f"TEMPLATE-{uuid.uuid4().hex[:8].upper()}")
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    preview_image = Column(String, nullable=True)
    repository_url = Column(String, nullable=True)  # Git repository with template code
    version = Column(String, nullable=False, default="1.0.0")
    is_active = Column(Boolean, default=True)
    
    # Template features and characteristics
    features = Column(JSON, nullable=True)  # List of features this template supports
    suitable_niches = Column(JSON, nullable=True)  # List of niches this template is suitable for
    color_schemes = Column(JSON, nullable=True)  # Available color schemes
    supports_dark_mode = Column(Boolean, default=False)
    
    # Performance metrics
    performance_score = Column(Integer, nullable=True)  # 0-100 performance score
    
    # Template configuration options
    config_schema = Column(JSON, nullable=True)  # JSON schema for configuration options
    
    # Metadata
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<SiteTemplate {self.id}: {self.name} v{self.version}>"
