"""
API routes for project management.
"""
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project, ProjectStatus
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.agents.orchestrator import OrchestratorAgent
from app.core.state import StateManager

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize the orchestrator agent
orchestrator = OrchestratorAgent()
state_manager = StateManager()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project.
    """
    logger.info(f"Creating new project: {project.name}")
    
    # Create project in database
    db_project = Project(
        name=project.name,
        description=project.description,
        client_id=project.client_id,
        status=ProjectStatus.INITIALIZING
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Initialize project with orchestrator
    result = orchestrator.initialize_project(
        project_id=db_project.id,
        client_data={
            "name": project.name,
            "description": project.description,
            "industry": project.industry,
            "goals": project.goals,
            "client_id": project.client_id
        }
    )
    
    logger.info(f"Project created with ID: {db_project.id}")
    
    return {
        "id": db_project.id,
        "name": db_project.name,
        "description": db_project.description,
        "status": db_project.status,
        "client_id": db_project.client_id,
        "message": result
    }

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    status: Optional[ProjectStatus] = None,
    client_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List projects with optional filtering.
    """
    logger.info(f"Listing projects with filters - status: {status}, client_id: {client_id}")
    
    query = db.query(Project)
    
    if status:
        query = query.filter(Project.status == status)
    
    if client_id:
        query = query.filter(Project.client_id == client_id)
    
    projects = query.offset(skip).limit(limit).all()
    
    return projects

@router.get("/{project_id}", response_model=Dict[str, Any])
async def get_project(project_id: str):
    """
    Get project details and state.
    """
    logger.info(f"Getting project details for ID: {project_id}")
    
    # Get project state from state manager
    project_state = state_manager.get_project_state(project_id)
    
    if project_state.get("status") == ProjectStatus.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    return project_state

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """
    Update project details.
    """
    logger.info(f"Updating project with ID: {project_id}")
    
    db_project = db.query(Project).filter(Project.id == project_id).first()
    
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Update project in database
    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    
    # Also update state if needed
    if project_update.status:
        state_manager.update_project_state(
            project_id=project_id,
            updates={"status": project_update.status}
        )
    
    logger.info(f"Project {project_id} updated successfully")
    
    return db_project

@router.post("/{project_id}/run/{stage}", response_model=Dict[str, Any])
async def run_project_stage(project_id: str, stage: str):
    """
    Run a specific stage of the project workflow.
    """
    logger.info(f"Running stage {stage} for project {project_id}")
    
    # Validate that project exists
    project_state = state_manager.get_project_state(project_id)
    
    if project_state.get("status") == ProjectStatus.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Map stage name to orchestrator method
    stage_methods = {
        "client_requirements": orchestrator.start_client_requirements_stage,
        "niche_research": orchestrator.start_niche_research_stage,
        "seo_strategy": orchestrator.start_seo_strategy_stage,
        "content_planning": orchestrator.start_content_planning_stage,
        "content_generation": orchestrator.start_content_generation_stage,
        "wordpress_setup": orchestrator.start_wordpress_setup_stage,
        "design_implementation": orchestrator.start_design_implementation_stage,
        "monetization": orchestrator.start_monetization_stage,
        "testing_qa": orchestrator.start_testing_qa_stage,
    }
    
    if stage not in stage_methods:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stage: {stage}"
        )
    
    # Run the specified stage
    method = stage_methods[stage]
    result = method(project_id)
    
    return {
        "project_id": project_id,
        "stage": stage,
        "status": "initiated",
        "message": result
    }

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str, db: Session = Depends(get_db)):
    """
    Delete a project.
    """
    logger.info(f"Deleting project with ID: {project_id}")
    
    db_project = db.query(Project).filter(Project.id == project_id).first()
    
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Delete project from database
    db.delete(db_project)
    db.commit()
    
    # Delete project state
    state_manager.delete_project_state(project_id)
    
    logger.info(f"Project {project_id} deleted successfully")
    
    return None
