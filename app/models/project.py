from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLAEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from app.db.base import Base

class ProjectStatus(str, Enum):
    """Enum for project status"""
    NOT_FOUND = "not_found"
    ERROR = "error"
    UNKNOWN = "unknown"
    INITIALIZING = "initializing"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class Project(Base):
    """Project model for database"""
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True, default=lambda: f"PRJ-{uuid.uuid4().hex[:8].upper()}")
    client_id = Column(String, ForeignKey("clients.id"))
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLAEnum(ProjectStatus), default=ProjectStatus.INITIALIZING)
    niche = Column(String, nullable=True)
    current_stage = Column(String, nullable=True)
    progress = Column(Integer, default=0)
    start_date = Column(DateTime(timezone=True), default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    client = relationship("Client", back_populates="projects")
    websites = relationship("Website", back_populates="project")
    static_sites = relationship("StaticSite", back_populates="project")
    content_items = relationship("ContentItem", back_populates="project")
    
    def __repr__(self):
        return f"<Project {self.id}: {self.name}>"
