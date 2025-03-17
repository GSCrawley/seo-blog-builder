"""
Pydantic schemas for projects.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.project import ProjectStatus

class ProjectBase(BaseModel):
    """Base schema for project data."""
    name: str = Field(..., description="Name of the project", example="Fitness Supplement Blog")
    description: Optional[str] = Field(None, description="Description of the project")
    industry: Optional[str] = Field(None, description="Industry or niche of the project", example="Health & Fitness")
    goals: Optional[str] = Field(None, description="Goals and objectives of the project")

class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    client_id: str = Field(..., description="ID of the client", example="CL-12345")

class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    niche: Optional[str] = None
    current_stage: Optional[str] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    end_date: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

class ProjectResponse(ProjectBase):
    """Schema for project response."""
    id: str = Field(..., description="Unique identifier for the project")
    client_id: str = Field(..., description="ID of the client")
    status: ProjectStatus = Field(..., description="Current status of the project")
    current_stage: Optional[str] = Field(None, description="Current stage of the project workflow")
    progress: Optional[int] = Field(0, description="Progress percentage of the project", ge=0, le=100)
    start_date: Optional[datetime] = Field(None, description="Project start date")
    end_date: Optional[datetime] = Field(None, description="Project end date")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    message: Optional[str] = None
    
    class Config:
        """Pydantic configuration."""
        orm_mode = True

class ProjectDetail(ProjectResponse):
    """Schema for detailed project response."""
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional project metadata")
    stages: Optional[Dict[str, Any]] = Field(None, description="Project stage information")
    timeline: Optional[List[Dict[str, Any]]] = Field(None, description="Project timeline events")
