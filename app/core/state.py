"""
State manager for the SEO Blog Builder application.
"""
from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime
import redis

from app.models.project import ProjectStatus
from app.config import settings

logger = logging.getLogger(__name__)

class StateManager:
    """
    Manages state for all projects in the system.
    Uses Redis for distributed state management to enable scalability.
    """
    
    def __init__(self):
        """Initialize the state manager with Redis connection."""
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        
    def _get_project_key(self, project_id: str) -> str:
        """Generate Redis key for a project."""
        return f"project:{project_id}:state"
    
    def create_project_state(self, project_id: str, initial_state: Dict[str, Any]) -> bool:
        """
        Create a new project state in Redis.
        
        Args:
            project_id: Unique identifier for the project
            initial_state: Initial state data for the project
            
        Returns:
            bool: Success status
        """
        key = self._get_project_key(project_id)
        
        # Check if project already exists
        if self.redis_client.exists(key):
            logger.warning(f"Project {project_id} already exists, not overwriting")
            return False
            
        # Add created timestamp if not present
        if "created_at" not in initial_state:
            initial_state["created_at"] = datetime.now().isoformat()
            
        # Store the state in Redis
        try:
            self.redis_client.set(key, json.dumps(initial_state))
            logger.info(f"Created state for project {project_id}")
            return True
        except Exception as e:
            logger.error(f"Error creating state for project {project_id}: {str(e)}")
            return False
    
    def get_project_state(self, project_id: str) -> Dict[str, Any]:
        """
        Get the current state of a project.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Project state data
        """
        key = self._get_project_key(project_id)
        
        try:
            state_json = self.redis_client.get(key)
            if not state_json:
                logger.warning(f"No state found for project {project_id}")
                return {
                    "status": ProjectStatus.NOT_FOUND,
                    "error": "Project not found"
                }
                
            return json.loads(state_json)
        except Exception as e:
            logger.error(f"Error getting state for project {project_id}: {str(e)}")
            return {
                "status": ProjectStatus.ERROR,
                "error": f"Error retrieving project state: {str(e)}"
            }
    
    def update_project_state(self, project_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update specific fields in the project state.
        
        Args:
            project_id: Unique identifier for the project
            updates: Dictionary of fields to update
            
        Returns:
            bool: Success status
        """
        key = self._get_project_key(project_id)
        
        try:
            # Get current state
            current_state_json = self.redis_client.get(key)
            if not current_state_json:
                logger.warning(f"Cannot update non-existent project {project_id}")
                return False
                
            current_state = json.loads(current_state_json)
            
            # Update state with new values
            for key, value in updates.items():
                current_state[key] = value
                
            # Add updated timestamp
            current_state["updated_at"] = datetime.now().isoformat()
            
            # Store updated state
            self.redis_client.set(key, json.dumps(current_state))
            logger.info(f"Updated state for project {project_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating state for project {project_id}: {str(e)}")
            return False
    
    def delete_project_state(self, project_id: str) -> bool:
        """
        Delete a project's state.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            bool: Success status
        """
        key = self._get_project_key(project_id)
        
        try:
            result = self.redis_client.delete(key)
            if result:
                logger.info(f"Deleted state for project {project_id}")
                return True
            else:
                logger.warning(f"No state found to delete for project {project_id}")
                return False
        except Exception as e:
            logger.error(f"Error deleting state for project {project_id}: {str(e)}")
            return False
    
    def list_active_projects(self) -> Dict[str, Dict[str, Any]]:
        """
        List all active projects with basic status information.
        
        Returns:
            Dict: Dictionary of project IDs mapping to basic status info
        """
        try:
            # Get all project keys
            keys = self.redis_client.keys("project:*:state")
            
            results = {}
            for key in keys:
                try:
                    # Extract project ID from key
                    project_id = key.split(":")[1]
                    
                    # Get state
                    state_json = self.redis_client.get(key)
                    if state_json:
                        state = json.loads(state_json)
                        
                        # Include only basic information
                        results[project_id] = {
                            "status": state.get("status", ProjectStatus.UNKNOWN),
                            "stage": state.get("stage", "unknown"),
                            "progress": state.get("progress", 0),
                            "created_at": state.get("created_at", ""),
                            "updated_at": state.get("updated_at", "")
                        }
                except Exception as e:
                    logger.error(f"Error processing project key {key}: {str(e)}")
                    continue
                    
            return results
        except Exception as e:
            logger.error(f"Error listing active projects: {str(e)}")
            return {}
            
    def add_event_to_project_timeline(self, project_id: str, event: Dict[str, Any]) -> bool:
        """
        Add an event to the project's timeline for audit and tracking.
        
        Args:
            project_id: Unique identifier for the project
            event: Event data to add to timeline
            
        Returns:
            bool: Success status
        """
        timeline_key = f"project:{project_id}:timeline"
        
        try:
            # Ensure event has timestamp
            if "timestamp" not in event:
                event["timestamp"] = datetime.now().isoformat()
                
            # Add to timeline (implemented as a Redis list)
            self.redis_client.rpush(timeline_key, json.dumps(event))
            logger.info(f"Added event to timeline for project {project_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding event to timeline for project {project_id}: {str(e)}")
            return False
    
    def get_project_timeline(self, project_id: str) -> list:
        """
        Get the timeline of events for a project.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            list: List of timeline events
        """
        timeline_key = f"project:{project_id}:timeline"
        
        try:
            # Get all timeline events
            event_jsons = self.redis_client.lrange(timeline_key, 0, -1)
            
            # Parse JSON strings to dictionaries
            events = [json.loads(event_json) for event_json in event_jsons]
            
            return events
        except Exception as e:
            logger.error(f"Error getting timeline for project {project_id}: {str(e)}")
            return []
