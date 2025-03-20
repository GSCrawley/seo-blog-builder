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
        
        try:
            # Get the current project state
            project_state = self.state_manager.get_project_state(project_id)
            topic = project_state.get("topic", "")
            topic_analysis = project_state.get("topic_analysis", {})
            niche_research = project_state.get("niche_research", {})
            
            # Mark stage as in progress
            self._update_stage_status(project_id, "content_planning", "in_progress")
            
            # Use the SEO service to create a content plan
            from app.services.seo import SeoService
            seo_service = SeoService()
            
            # Get the number of articles from user preferences or default to 5
            num_articles = project_state.get("preferences", {}).get("num_articles", 5)
            
            # Create content plan
            content_plan = seo_service.create_content_plan(topic, num_articles)
            
            # Update project state with content plan
            self.state_manager.update_project_state(
                project_id,
                {
                    "content_plan": content_plan,
                    "progress": 45  # Update progress percentage
                }
            )
            
            # Add event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "content_planning_completed",
                    "description": f"Created content plan with {num_articles} articles for: {topic}",
                    "data": {"content_plan_summary": {
                        "pillar_content": content_plan.get("pillar_content", {}).get("title"),
                        "cluster_content": [c.get("title") for c in content_plan.get("cluster_content", [])][:3],
                        "total_articles": content_plan.get("total_articles", 0)
                    }}
                }
            )
            
            # Mark stage as completed
            self._update_stage_status(project_id, "content_planning", "completed")
            
            # Start the next stage
            self._update_stage_status(project_id, "content_creation", "in_progress")
            
            return {
                "success": True,
                "project_id": project_id,
                "topic": topic,
                "content_plan": content_plan,
                "next_stage": "content_creation"
            }
            
        except Exception as e:
            logger.error(f"Error processing content planning: {str(e)}")
            
            # Update stage status to failed
            self._update_stage_status(project_id, "content_planning", "failed")
            
            # Add error event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "content_planning_failed",
                    "description": f"Failed to complete content planning: {str(e)}",
                    "data": {"error": str(e)}
                }
            )
            
            return {
                "success": False,
                "project_id": project_id,
                "error": str(e),
                "message": "Failed to complete content planning"
            }
    
    def process_content_creation(self, project_id: str) -> Dict[str, Any]:
        """
        Create the content for the blog based on the content plan.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Generated content for the blog
        """
        logger.info(f"Processing content creation for project {project_id}")
        
        try:
            # Get the current project state
            project_state = self.state_manager.get_project_state(project_id)
            topic = project_state.get("topic", "")
            content_plan = project_state.get("content_plan", {})
            
            # Mark stage as in progress
            self._update_stage_status(project_id, "content_creation", "in_progress")
            
            # Extract content items from the plan
            pillar_content = content_plan.get("pillar_content", {})
            cluster_content = content_plan.get("cluster_content", [])
            
            # Initialize results
            generated_content = []
            
            # Generate pillar content first
            if pillar_content:
                pillar_article = self._generate_article(
                    topic=topic,
                    article_plan=pillar_content,
                    is_pillar=True
                )
                generated_content.append(pillar_article)
            
            # Generate cluster content
            for article_plan in cluster_content:
                cluster_article = self._generate_article(
                    topic=topic,
                    article_plan=article_plan,
                    is_pillar=False
                )
                generated_content.append(cluster_article)
            
            # Update project state with generated content
            self.state_manager.update_project_state(
                project_id,
                {
                    "generated_content": generated_content,
                    "progress": 65  # Update progress percentage
                }
            )
            
            # Add event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "content_creation_completed",
                    "description": f"Created {len(generated_content)} articles for: {topic}",
                    "data": {
                        "article_count": len(generated_content),
                        "titles": [article.get("title") for article in generated_content[:3]]
                    }
                }
            )
            
            # Mark stage as completed
            self._update_stage_status(project_id, "content_creation", "completed")
            
            # Start the next stage
            self._update_stage_status(project_id, "site_generation", "in_progress")
            
            return {
                "success": True,
                "project_id": project_id,
                "topic": topic,
                "content_count": len(generated_content),
                "next_stage": "site_generation"
            }
            
        except Exception as e:
            logger.error(f"Error processing content creation: {str(e)}")
            
            # Update stage status to failed
            self._update_stage_status(project_id, "content_creation", "failed")
            
            # Add error event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "content_creation_failed",
                    "description": f"Failed to complete content creation: {str(e)}",
                    "data": {"error": str(e)}
                }
            )
            
            return {
                "success": False,
                "project_id": project_id,
                "error": str(e),
                "message": "Failed to complete content creation"
            }
    
    def _generate_article(self, topic: str, article_plan: Dict[str, Any], is_pillar: bool = False) -> Dict[str, Any]:
        """
        Generate an article based on a plan.
        
        Args:
            topic: Main topic
            article_plan: Article plan with title, sections, etc.
            is_pillar: Whether this is a pillar article
            
        Returns:
            Dict: Generated article
        """
        try:
            title = article_plan.get("title", f"Article about {topic}")
            target_keyword = article_plan.get("target_keyword", topic)
            sections = article_plan.get("sections", [])
            
            # Load the article generation prompt
            prompt = self._load_prompt_template("article_generation")
            
            # Replace placeholders in the prompt
            prompt = prompt.replace("{title}", title)
            prompt = prompt.replace("{primary_keyword}", target_keyword)
            prompt = prompt.replace("{content_type}", article_plan.get("type", "article"))
            
            # Format sections for the prompt
            sections_text = "\n".join([f"## {section.get('heading')} ({section.get('word_count', 200)} words)" for section in sections])
            prompt = prompt.replace("{content_brief}", f"This article should cover the following sections:\n{sections_text}")
            
            # Execute the prompt with Claude (better for long-form content)
            response = self.claude_service.get_completion(prompt, temperature=0.7, max_tokens=4000)
            
            # Format the result
            article = {
                "title": title,
                "slug": self._generate_slug(title),
                "content": response,
                "primary_keyword": target_keyword,
                "is_pillar": is_pillar,
                "word_count": len(response.split()),
                "markdown_content": response,  # Save for static site generation
                "created_at": datetime.now().isoformat()
            }
            
            # Generate meta tags
            from app.services.seo import SeoService
            seo_service = SeoService()
            meta_tags = seo_service.generate_meta_tags(title, response, target_keyword)
            
            article["meta_title"] = meta_tags.get("title")
            article["meta_description"] = meta_tags.get("description")
            article["meta_keywords"] = meta_tags.get("keywords")
            
            return article
            
        except Exception as e:
            logger.error(f"Error generating article: {str(e)}")
            return {
                "title": article_plan.get("title", f"Article about {topic}"),
                "content": f"Error generating content: {str(e)}",
                "error": str(e)
            }
    
    def _generate_slug(self, title: str) -> str:
        """
        Generate a URL slug from a title.
        
        Args:
            title: Article title
            
        Returns:
            str: URL slug
        """
        from app.utils.helpers import slugify
        return slugify(title)
    
    def process_site_generation(self, project_id: str) -> Dict[str, Any]:
        """
        Generate the static site using the created content.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Information about the generated site
        """
        logger.info(f"Processing site generation for project {project_id}")
        
        try:
            # Get the current project state
            project_state = self.state_manager.get_project_state(project_id)
            topic = project_state.get("topic", "")
            generated_content = project_state.get("generated_content", [])
            preferences = project_state.get("preferences", {})
            
            # Mark stage as in progress
            self._update_stage_status(project_id, "site_generation", "in_progress")
            
            # Initialize static site generation service
            from app.services.site_generation import StaticSiteGenerationService
            site_service = StaticSiteGenerationService()
            
            # Generate site title and subdomain
            site_title = preferences.get("site_title", f"{topic.title()} - Expert Guide")
            subdomain = preferences.get("subdomain", self._generate_slug(topic))
            
            # Create site configuration
            site_config = {
                "title": site_title,
                "description": preferences.get("site_description", f"Complete guide to {topic} with expert advice and reviews"),
                "subdomain": subdomain,
                "template_id": preferences.get("template", "default"),
                "primary_color": preferences.get("primary_color", "#3498db"),
                "secondary_color": preferences.get("secondary_color", "#2ecc71"),
                "author": preferences.get("author", "Content Team"),
                "google_analytics_id": preferences.get("google_analytics_id", "")
            }
            
            # Create the static site
            site_result = site_service.create_site(project_id, site_config)
            
            if not site_result.get("success", False):
                raise Exception(f"Failed to create static site: {site_result.get('message')}")
            
            site_id = site_result.get("site_id")
            site_path = site_result.get("site_path")
            
            # Add content to the site
            for article in generated_content:
                # Create ContentItem object
                content_item = self._create_content_item_from_article(article, project_id, site_id)
                
                # Add content to the site
                content_result = site_service.add_content(site_id, content_item)
                
                if not content_result.get("success", False):
                    logger.warning(f"Failed to add content {article.get('title')}: {content_result.get('message')}")
            
            # Update project state with site information
            self.state_manager.update_project_state(
                project_id,
                {
                    "site": {
                        "id": site_id,
                        "title": site_title,
                        "subdomain": subdomain,
                        "path": site_path
                    },
                    "progress": 85  # Update progress percentage
                }
            )
            
            # Add event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "site_generation_completed",
                    "description": f"Generated static site for: {topic}",
                    "data": {
                        "site_id": site_id,
                        "site_title": site_title,
                        "subdomain": subdomain
                    }
                }
            )
            
            # Mark stage as completed
            self._update_stage_status(project_id, "site_generation", "completed")
            
            # Start the next stage
            self._update_stage_status(project_id, "deployment", "in_progress")
            
            return {
                "success": True,
                "project_id": project_id,
                "site_id": site_id,
                "site_title": site_title,
                "subdomain": subdomain,
                "next_stage": "deployment"
            }
            
        except Exception as e:
            logger.error(f"Error processing site generation: {str(e)}")
            
            # Update stage status to failed
            self._update_stage_status(project_id, "site_generation", "failed")
            
            # Add error event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "site_generation_failed",
                    "description": f"Failed to generate site: {str(e)}",
                    "data": {"error": str(e)}
                }
            )
            
            return {
                "success": False,
                "project_id": project_id,
                "error": str(e),
                "message": "Failed to generate site"
            }
    
    def _create_content_item_from_article(self, article: Dict[str, Any], project_id: str, site_id: str) -> Any:
        """
        Create a ContentItem object from an article.
        
        Args:
            article: Article data
            project_id: Project ID
            site_id: Site ID
            
        Returns:
            Any: ContentItem object
        """
        # This is a simplified version that returns a dict
        # In a real implementation, you would create a database object
        return {
            "id": f"CONTENT-{uuid.uuid4().hex[:8].upper()}",
            "title": article.get("title", ""),
            "slug": article.get("slug", ""),
            "project_id": project_id,
            "static_site_id": site_id,
            "content_type": "BLOG_POST",
            "status": "PUBLISHED",
            "markdown_content": article.get("markdown_content", ""),
            "meta_title": article.get("meta_title", ""),
            "meta_description": article.get("meta_description", ""),
            "primary_keyword": article.get("primary_keyword", ""),
            "is_pillar": article.get("is_pillar", False),
            "word_count": article.get("word_count", 0),
            "publish_date": datetime.now().isoformat()
        }
    
    def process_deployment(self, project_id: str) -> Dict[str, Any]:
        """
        Deploy the generated site.
        
        Args:
            project_id: Unique identifier for the project
            
        Returns:
            Dict: Deployment information
        """
        logger.info(f"Processing deployment for project {project_id}")
        
        try:
            # Get the current project state
            project_state = self.state_manager.get_project_state(project_id)
            topic = project_state.get("topic", "")
            site_info = project_state.get("site", {})
            preferences = project_state.get("preferences", {})
            
            site_id = site_info.get("id")
            if not site_id:
                raise Exception("Site ID not found in project state")
            
            # Mark stage as in progress
            self._update_stage_status(project_id, "deployment", "in_progress")
            
            # Initialize static site generation service
            from app.services.site_generation import StaticSiteGenerationService
            site_service = StaticSiteGenerationService()
            
            # Build the static site
            build_result = site_service.build_site(site_id)
            
            if not build_result.get("success", False):
                raise Exception(f"Failed to build site: {build_result.get('message')}")
                
            # Get deployment provider from preferences or default to Vercel
            from app.models.static_site import DeploymentProvider
            provider_name = preferences.get("deployment_provider", "vercel")
            
            # Map string to enum
            provider_map = {
                "vercel": DeploymentProvider.VERCEL,
                "netlify": DeploymentProvider.NETLIFY,
                "github_pages": DeploymentProvider.GITHUB_PAGES,
                "cloudflare_pages": DeploymentProvider.CLOUDFLARE_PAGES,
                "custom": DeploymentProvider.CUSTOM
            }
            
            provider = provider_map.get(provider_name.lower(), DeploymentProvider.VERCEL)
            
            # Deploy the site
            deploy_result = site_service.deploy_site(site_id, provider)
            
            if not deploy_result.get("success", False):
                raise Exception(f"Failed to deploy site: {deploy_result.get('message')}")
            
            # Extract deployment information
            deployment_id = deploy_result.get("deployment_id")
            deployment_url = deploy_result.get("deployment_url")
            
            # Update project state with deployment information
            self.state_manager.update_project_state(
                project_id,
                {
                    "deployment": {
                        "id": deployment_id,
                        "url": deployment_url,
                        "provider": provider_name,
                        "status": "deployed",
                        "deployed_at": datetime.now().isoformat()
                    },
                    "status": "COMPLETED",
                    "progress": 100  # Update progress percentage
                }
            )
            
            # Add event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "deployment_completed",
                    "description": f"Deployed site to {provider_name}: {deployment_url}",
                    "data": {
                        "deployment_id": deployment_id,
                        "deployment_url": deployment_url,
                        "provider": provider_name
                    }
                }
            )
            
            # Mark stage as completed
            self._update_stage_status(project_id, "deployment", "completed")
            
            # Mark project as completed
            self.state_manager.update_project_state(
                project_id,
                {"status": "COMPLETED"}
            )
            
            return {
                "success": True,
                "project_id": project_id,
                "deployment_url": deployment_url,
                "status": "completed"
            }
            
        except Exception as e:
            logger.error(f"Error processing deployment: {str(e)}")
            
            # Update stage status to failed
            self._update_stage_status(project_id, "deployment", "failed")
            
            # Add error event to timeline
            self.state_manager.add_event_to_project_timeline(
                project_id,
                {
                    "event_type": "deployment_failed",
                    "description": f"Failed to deploy site: {str(e)}",
                    "data": {"error": str(e)}
                }
            )
            
            return {
                "success": False,
                "project_id": project_id,
                "error": str(e),
                "message": "Failed to deploy site"
            }
    
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
