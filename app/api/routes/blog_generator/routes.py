"""
API routes for the blog generator.
"""
import logging
from typing import Dict, Any, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import uuid

from app.db.session import get_db
from app.orchestration import Orchestrator
from app.core.state import StateManager
from app.models.project import Project, ProjectStatus

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize the orchestrator
orchestrator = Orchestrator()
state_manager = StateManager()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_blog(
    data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new blog for a given topic.
    """
    logger.info(f"Creating new blog for topic: {data.get('topic', 'Not specified')}")
    
    # Validate input
    topic = data.get("topic")
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Topic is required"
        )
    
    # Get user preferences
    preferences = data.get("preferences", {})
    
    # Create project in database
    project_id = f"PRJ-{uuid.uuid4().hex[:8].upper()}"
    db_project = Project(
        id=project_id,
        name=f"Blog - {topic}",
        description=f"Automatically generated blog for topic: {topic}",
        status=ProjectStatus.INITIALIZING,
        client_id=data.get("client_id")  # Optional client ID
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Initialize project with orchestrator
    result = orchestrator.start_project(
        project_id=project_id,
        topic=topic,
        user_preferences=preferences
    )
    
    # Start the workflow in the background
    background_tasks.add_task(process_blog_workflow, project_id)
    
    logger.info(f"Blog creation initiated for project ID: {project_id}")
    
    return {
        "project_id": project_id,
        "topic": topic,
        "status": "initialized",
        "message": "Blog creation process has been started"
    }

@router.get("/{project_id}/status")
async def get_blog_status(project_id: str):
    """
    Get the current status of a blog creation project.
    """
    logger.info(f"Checking status for project ID: {project_id}")
    
    # Get project state
    project_state = state_manager.get_project_state(project_id)
    
    if project_state.get("status") == ProjectStatus.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Get the timeline
    timeline = state_manager.get_project_timeline(project_id)
    
    return {
        "project_id": project_id,
        "status": project_state.get("status"),
        "current_stage": project_state.get("current_stage"),
        "progress": project_state.get("progress", 0),
        "stages": project_state.get("stages", {}),
        "timeline": timeline[-10:] if timeline else []  # Return last 10 events for brevity
    }

@router.post("/{project_id}/cancel")
async def cancel_blog_creation(project_id: str, db: Session = Depends(get_db)):
    """
    Cancel an ongoing blog creation process.
    """
    logger.info(f"Cancelling project ID: {project_id}")
    
    # Get project state
    project_state = state_manager.get_project_state(project_id)
    
    if project_state.get("status") == ProjectStatus.NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    
    # Update database
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if db_project:
        db_project.status = ProjectStatus.PAUSED
        db.commit()
    
    # Update state
    state_manager.update_project_state(
        project_id,
        {
            "status": ProjectStatus.PAUSED,
            "updated_at": datetime.now().isoformat()
        }
    )
    
    # Add event to timeline
    state_manager.add_event_to_project_timeline(
        project_id,
        {
            "event_type": "project_cancelled",
            "description": "Project was cancelled by user request",
            "data": {"previous_status": project_state.get("status")}
        }
    )
    
    return {
        "project_id": project_id,
        "status": "cancelled",
        "message": "Blog creation process has been cancelled"
    }

# Background task function
async def process_blog_workflow(project_id: str):
    """
    Process the blog creation workflow in the background.
    """
    logger.info(f"Starting background workflow for project ID: {project_id}")
    
    try:
        # Execute stages in sequence
        # In a real implementation, you would add error handling and recovery
        
        # 1. Topic Analysis
        topic_result = orchestrator.process_topic_analysis(project_id)
        if not topic_result.get("success", False):
            logger.error(f"Topic analysis failed for project {project_id}")
            return
        
        # 2. Niche Research
        niche_result = orchestrator.process_niche_research(project_id)
        if not niche_result.get("success", False):
            logger.error(f"Niche research failed for project {project_id}")
            return
        
        # 3. Content Planning
        content_plan_result = orchestrator.process_content_planning(project_id)
        if not content_plan_result.get("success", False):
            logger.error(f"Content planning failed for project {project_id}")
            return
        
        # 4. Content Creation
        content_result = orchestrator.process_content_creation(project_id)
        if not content_result.get("success", False):
            logger.error(f"Content creation failed for project {project_id}")
            return
        
        # 5. Site Generation
        site_result = orchestrator.process_site_generation(project_id)
        if not site_result.get("success", False):
            logger.error(f"Site generation failed for project {project_id}")
            return
        
        # 6. Deployment
        deploy_result = orchestrator.process_deployment(project_id)
        if not deploy_result.get("success", False):
            logger.error(f"Deployment failed for project {project_id}")
            return
        
        logger.info(f"Blog creation workflow completed successfully for project {project_id}")
        
    except Exception as e:
        logger.error(f"Error in blog creation workflow for project {project_id}: {str(e)}")
        
        # Update state with error
        state_manager.update_project_state(
            project_id,
            {
                "status": ProjectStatus.FAILED,
                "error": str(e),
                "updated_at": datetime.now().isoformat()
            }
        )
        
        # Add error event to timeline
        state_manager.add_event_to_project_timeline(
            project_id,
            {
                "event_type": "workflow_error",
                "description": f"Blog creation workflow failed with error: {str(e)}",
                "data": {"error": str(e)}
            }
        )
