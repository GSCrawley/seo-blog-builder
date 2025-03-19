"""
Custom orchestration system for managing the blog generation workflow.
"""
import logging
import os
from typing import Dict, Any, List, Optional
import json
from datetime import datetime

from app.config import settings
from app.core.state import StateManager
from app.models.project import ProjectStatus
from app.services.llm.claude import ClaudeService
from app.services.llm.openai import OpenAIService
from app.services.site_generation import StaticSiteGenerationService

logger = logging.getLogger(__name__)

class Orchestrator:
    """
    Orchestrates the entire blog creation process using specialized agents.
    This replaces the CrewAI dependency with a custom orchestration layer.
    """
    
    def __init__(self):
        """Initialize the orchestrator."""
        self.state_manager = StateManager()
        self.claude_service = ClaudeService()
        self.openai_service = OpenAIService()
        self.site_service = StaticSiteGenerationService()
        
    def start_project(self, project_id: str, topic: str, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start a new blog creation project for a given topic.
        
        Args:
            project_id: Unique identifier for the project
            topic: The main topic or niche for the blog
            user_preferences: User preferences for the blog
            
        Returns:
            Dict: Project information and initial state
        """
        logger.info(f"Starting new project for topic: {topic}")
        
        # Initialize project state
        initial_state = {
            "project_id": project_id,
            "topic": topic,
            "preferences": user_preferences,
            "status": ProjectStatus.INITIALIZING,
            "current_stage": "topic_analysis",
            "progress": 0,
            "stages": {
                "topic_analysis": {"status": "pending", "started_at": None, "completed_at": None},
                "niche_research": {"status": "pending", "started_at": None, "completed_at": None},
                "content_planning": {"status": "pending", "started_at": None, "completed_at": None},
                "content_creation": {"status": "pending", "started_at": None, "completed_at": None},
                "site_generation": {"status": "pending", "started_at": None, "completed_at": None},
                "deployment": {"status": "pending", "started_at": None, "completed_at": None}
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.state_manager.create_project_state(project_id, initial_state)
        
        # Add initial event to timeline
        self.state_manager.add_event_to_project_timeline(
            project_id,
            {
                "event_type": "project_started",
                "description": f"Started new project for topic: {topic}",
                "data": {"topic": topic, "preferences": user_preferences}
            }
        )
        
        # Start the first stage asynchronously
        # In a real implementation, this would be a background task
        # For now, we'll just update the state
        self._update_stage_status(project_id, "topic_analysis", "in_progress")
        
        return {
            "project_id": project_id,
            "topic": topic,
            "status": ProjectStatus.INITIALIZING,
            "message": "Project initialized successfully, starting topic analysis"
        }
    
    def process_topic_analysis(self, project_id: str) -> Dict[str, Any]:
        """
        Analyze the topic to understand its scope, audience, and potential.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Results of the topic analysis
        """
        logger.info(f"Processing topic analysis for project {project_id}")
        
        try:
            # Get the current project state
            project_state = self.state_manager.get_project_state(project_id)
            topic = project_state.get("topic", "")
            
            # Mark stage as in progress
            self._update_stage_status(project_id, "topic_analysis", "in_progress")
            
            # Load prompt template
            prompt = self._load_prompt_template("topic_analysis")
            
            # Replace placeholders in the prompt
            prompt = prompt.replace("{topic}", topic)
            
            # Execute the prompt with Claude
            response = self.claude_service.get_completion(prompt, temperature=0.3, max_tokens=2000)
            
            # Parse the response (assuming it's JSON or has a structured format)
            # In a real implementation, you would ensure the response is properly structured
            analysis_data = {
                "topic": topic,
                "analysis": response,
                "timestamp": datetime.now().isoformat()
            }
            
            # Update project state with analysis results
            self.state_manager.update_project_state(
                project_id,
                {
                    "topic_analysis": analysis_data,
                    "progress": 15  # Update progress percentage
                }
            )
            
            # Add event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "topic_analysis_completed",
                    "description": f"Completed topic analysis for: {topic}",
                    "data": {"analysis_summary": analysis_data}
                }
            )
            
            # Mark stage as completed
            self._update_stage_status(project_id, "topic_analysis", "completed")
            
            # Start the next stage
            self._update_stage_status(project_id, "niche_research", "in_progress")
            
            return {
                "success": True,
                "project_id": project_id,
                "topic": topic,
                "analysis": analysis_data,
                "next_stage": "niche_research"
            }
            
        except Exception as e:
            logger.error(f"Error processing topic analysis: {str(e)}")
            
            # Update stage status to failed
            self._update_stage_status(project_id, "topic_analysis", "failed")
            
            # Add error event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "topic_analysis_failed",
                    "description": f"Failed to complete topic analysis: {str(e)}",
                    "data": {"error": str(e)}
                }
            )
            
            return {
                "success": False,
                "project_id": project_id,
                "error": str(e),
                "message": "Failed to complete topic analysis"
            }
    
    def process_niche_research(self, project_id: str) -> Dict[str, Any]:
        """
        Research the niche to identify keywords, competitors, and audience.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Results of the niche research
        """
        logger.info(f"Processing niche research for project {project_id}")
        
        try:
            # Get the current project state
            project_state = self.state_manager.get_project_state(project_id)
            topic = project_state.get("topic", "")
            topic_analysis = project_state.get("topic_analysis", {})
            
            # Mark stage as in progress
            self._update_stage_status(project_id, "niche_research", "in_progress")
            
            # Load prompt template
            prompt = self._load_prompt_template("niche_research")
            
            # Replace placeholders in the prompt
            prompt = prompt.replace("{topic}", topic)
            prompt = prompt.replace("{topic_analysis}", json.dumps(topic_analysis))
            
            # Execute the prompt with OpenAI (better for research tasks)
            response = self.openai_service.get_completion(prompt, model="gpt-4-turbo", temperature=0.2, max_tokens=3000)
            
            # Parse the response
            research_data = {
                "topic": topic,
                "research": response,
                "timestamp": datetime.now().isoformat()
            }
            
            # Update project state with research results
            self.state_manager.update_project_state(
                project_id,
                {
                    "niche_research": research_data,
                    "progress": 30  # Update progress percentage
                }
            )
            
            # Add event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "niche_research_completed",
                    "description": f"Completed niche research for: {topic}",
                    "data": {"research_summary": research_data}
                }
            )
            
            # Mark stage as completed
            self._update_stage_status(project_id, "niche_research", "completed")
            
            # Start the next stage
            self._update_stage_status(project_id, "content_planning", "in_progress")
            
            return {
                "success": True,
                "project_id": project_id,
                "topic": topic,
                "research": research_data,
                "next_stage": "content_planning"
            }
            
        except Exception as e:
            logger.error(f"Error processing niche research: {str(e)}")
            
            # Update stage status to failed
            self._update_stage_status(project_id, "niche_research", "failed")
            
            # Add error event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "niche_research_failed",
                    "description": f"Failed to complete niche research: {str(e)}",
                    "data": {"error": str(e)}
                }
            )
            
            return {
                "success": False,
                "project_id": project_id,
                "error": str(e),
                "message": "Failed to complete niche research"
            }
    
    def process_content_planning(self, project_id: str) -> Dict[str, Any]:
        """
        Plan the content structure for the blog.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Content plan for the blog
        """
        logger.info(f"Processing content planning for project {project_id}")
        
        # Similar implementation to the previous methods
        # This would create a content plan with article topics, structures, etc.
        pass
    
    def process_content_creation(self, project_id: str) -> Dict[str, Any]:
        """
        Create the content for the blog based on the content plan.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Generated content for the blog
        """
        logger.info(f"Processing content creation for project {project_id}")
        
        # Similar implementation to the previous methods
        # This would generate the actual blog content
        pass
    
    def process_site_generation(self, project_id: str) -> Dict[str, Any]:
        """
        Generate the static site using the created content.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Information about the generated site
        """
        logger.info(f"Processing site generation for project {project_id}")
        
        # Similar implementation to the previous methods
        # This would use the StaticSiteGenerationService to build the site
        pass
    
    def process_deployment(self, project_id: str) -> Dict[str, Any]:
        """
        Deploy the generated site.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Deployment information
        """
        logger.info(f"Processing deployment for project {project_id}")
        
        # Similar implementation to the previous methods
        # This would use the StaticSiteGenerationService to deploy the site
        pass
    
    def _update_stage_status(self, project_id: str, stage: str, status: str) -> None:
        """
        Update the status of a project stage.
        
        Args:
            project_id: Unique identifier for the project
            stage: Name of the stage to update
            status: New status for the stage
        """
        # Get current state
        state = self.state_manager.get_project_state(project_id)
        
        # Update the stage status
        if "stages" in state and stage in state["stages"]:
            timestamp = datetime.now().isoformat()
            
            # Update specific timestamp based on status
            if status == "in_progress":
                state["stages"][stage]["started_at"] = timestamp
            elif status in ["completed", "failed"]:
                state["stages"][stage]["completed_at"] = timestamp
            
            state["stages"][stage]["status"] = status
            
            # Update current stage in main state if starting a new stage
            if status == "in_progress":
                state["current_stage"] = stage
            
            # Update global status if needed
            if status == "failed":
                state["status"] = ProjectStatus.FAILED
            elif all(s["status"] == "completed" for s in state["stages"].values()):
                state["status"] = ProjectStatus.COMPLETED
            else:
                state["status"] = ProjectStatus.IN_PROGRESS
            
            # Update timestamp
            state["updated_at"] = timestamp
            
            # Save the updated state
            self.state_manager.update_project_state(project_id, state)
    
    def _load_prompt_template(self, template_name: str) -> str:
        """
        Load a prompt template by name.
        
        Args:
            template_name: Name of the template to load
            
        Returns:
            str: Prompt template content
        """
        # Determine the template path based on the template name
        template_paths = {
            "topic_analysis": os.path.join(settings.PROMPT_TEMPLATES_DIR, "topic_analysis.txt"),
            "niche_research": os.path.join(settings.PROMPT_TEMPLATES_DIR, "niche_research", "market_analysis.txt"),
            "content_planning": os.path.join(settings.PROMPT_TEMPLATES_DIR, "content_planning", "content_plan.txt"),
            "article_generation": os.path.join(settings.PROMPT_TEMPLATES_DIR, "content_generation", "article_generation.txt"),
        }
        
        if template_name not in template_paths:
            logger.error(f"Template not found: {template_name}")
            return f"ERROR: Template {template_name} not found"
        
        template_path = template_paths[template_name]
        
        try:
            with open(template_path, 'r') as f:
                template = f.read()
            return template
        except Exception as e:
            logger.error(f"Error loading template {template_name}: {str(e)}")
            return f"ERROR: Failed to load template {template_name}: {str(e)}"
