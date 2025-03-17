"""
Crew manager for coordinating CrewAI agents.
"""
from typing import Dict, Any, List, Optional
import logging
from crewai import Crew, Process

from app.crew.agent_factory import AgentFactory
from app.crew.tasks import TaskFactory

logger = logging.getLogger(__name__)

class CrewManager:
    """
    Manager class for coordinating CrewAI agents and their tasks.
    """
    
    def __init__(self):
        """Initialize the crew manager with agent and task factories."""
        self.agent_factory = AgentFactory()
        self.task_factory = TaskFactory()
    
    def create_client_requirements_crew(self, project_id: str, client_data: Dict[str, Any]) -> Crew:
        """
        Create a crew for client requirements gathering.
        
        Args:
            project_id: Unique identifier for the project
            client_data: Initial client information
            
        Returns:
            Crew: A CrewAI crew for client requirements gathering
        """
        logger.info(f"Creating client requirements crew for project {project_id}")
        
        # Create the client requirements agent
        client_requirements_agent = self.agent_factory.create_client_requirements_agent()
        
        # Create the client interview task
        client_interview_task = self.task_factory.create_client_interview_task(
            project_id=project_id,
            client_data=client_data,
            agent=client_requirements_agent
        )
        
        # Create the requirements extraction task
        requirements_extraction_task = self.task_factory.create_requirements_extraction_task(
            project_id=project_id,
            agent=client_requirements_agent,
            context=[client_interview_task]  # This task depends on the interview task
        )
        
        # Create the technical specification task
        technical_spec_task = self.task_factory.create_technical_specification_task(
            project_id=project_id,
            agent=client_requirements_agent,
            context=[requirements_extraction_task]  # This task depends on the requirements task
        )
        
        # Create and return the crew
        return Crew(
            agents=[client_requirements_agent],
            tasks=[client_interview_task, requirements_extraction_task, technical_spec_task],
            verbose=2,
            process=Process.sequential
        )
    
    def create_niche_research_crew(self, project_id: str, requirements_data: Dict[str, Any]) -> Crew:
        """
        Create a crew for niche research.
        
        Args:
            project_id: Unique identifier for the project
            requirements_data: Client requirements data
            
        Returns:
            Crew: A CrewAI crew for niche research
        """
        logger.info(f"Creating niche research crew for project {project_id}")
        
        # Create the niche research agent
        niche_research_agent = self.agent_factory.create_niche_research_agent()
        
        # Create the market analysis task
        market_analysis_task = self.task_factory.create_market_analysis_task(
            project_id=project_id,
            requirements_data=requirements_data,
            agent=niche_research_agent
        )
        
        # Create the competitor analysis task
        competitor_analysis_task = self.task_factory.create_competitor_analysis_task(
            project_id=project_id,
            requirements_data=requirements_data,
            agent=niche_research_agent,
            context=[market_analysis_task]  # This task can use market analysis results
        )
        
        # Create the monetization potential task
        monetization_potential_task = self.task_factory.create_monetization_potential_task(
            project_id=project_id,
            requirements_data=requirements_data,
            agent=niche_research_agent,
            context=[market_analysis_task, competitor_analysis_task]  # Uses both previous tasks
        )
        
        # Create the niche recommendation task
        niche_recommendation_task = self.task_factory.create_niche_recommendation_task(
            project_id=project_id,
            agent=niche_research_agent,
            context=[market_analysis_task, competitor_analysis_task, monetization_potential_task]
        )
        
        # Create and return the crew
        return Crew(
            agents=[niche_research_agent],
            tasks=[
                market_analysis_task, 
                competitor_analysis_task, 
                monetization_potential_task, 
                niche_recommendation_task
            ],
            verbose=2,
            process=Process.sequential
        )
    
    def create_seo_strategy_crew(self, project_id: str, niche_data: Dict[str, Any], requirements_data: Dict[str, Any]) -> Crew:
        """
        Create a crew for SEO strategy development.
        
        Args:
            project_id: Unique identifier for the project
            niche_data: Niche research data
            requirements_data: Client requirements data
            
        Returns:
            Crew: A CrewAI crew for SEO strategy development
        """
        logger.info(f"Creating SEO strategy crew for project {project_id}")
        
        # Create the SEO strategy agent
        seo_strategy_agent = self.agent_factory.create_seo_strategy_agent()
        
        # Create the keyword research task
        keyword_research_task = self.task_factory.create_keyword_research_task(
            project_id=project_id,
            niche_data=niche_data,
            agent=seo_strategy_agent
        )
        
        # Create the content cluster task
        content_cluster_task = self.task_factory.create_content_cluster_task(
            project_id=project_id,
            agent=seo_strategy_agent,
            context=[keyword_research_task]
        )
        
        # Create the site architecture task
        site_architecture_task = self.task_factory.create_site_architecture_task(
            project_id=project_id,
            agent=seo_strategy_agent,
            context=[content_cluster_task]
        )
        
        # Create the technical SEO task
        technical_seo_task = self.task_factory.create_technical_seo_task(
            project_id=project_id,
            requirements_data=requirements_data,
            agent=seo_strategy_agent
        )
        
        # Create the SEO strategy document task
        seo_strategy_document_task = self.task_factory.create_seo_strategy_document_task(
            project_id=project_id,
            agent=seo_strategy_agent,
            context=[
                keyword_research_task, 
                content_cluster_task, 
                site_architecture_task, 
                technical_seo_task
            ]
        )
        
        # Create and return the crew
        return Crew(
            agents=[seo_strategy_agent],
            tasks=[
                keyword_research_task,
                content_cluster_task,
                site_architecture_task,
                technical_seo_task,
                seo_strategy_document_task
            ],
            verbose=2,
            process=Process.sequential
        )
    
    def create_full_blog_creation_crew(self, project_id: str, all_data: Dict[str, Any]) -> Crew:
        """
        Create a full crew for the entire blog creation process.
        
        Args:
            project_id: Unique identifier for the project
            all_data: All project data
            
        Returns:
            Crew: A CrewAI crew for the entire blog creation process
        """
        logger.info(f"Creating full blog creation crew for project {project_id}")
        
        # Create all agents
        client_requirements_agent = self.agent_factory.create_client_requirements_agent()
        niche_research_agent = self.agent_factory.create_niche_research_agent()
        seo_strategy_agent = self.agent_factory.create_seo_strategy_agent()
        content_planning_agent = self.agent_factory.create_content_planning_agent()
        content_generation_agent = self.agent_factory.create_content_generation_agent()
        wordpress_setup_agent = self.agent_factory.create_wordpress_setup_agent()
        design_implementation_agent = self.agent_factory.create_design_implementation_agent()
        monetization_agent = self.agent_factory.create_monetization_agent()
        testing_qa_agent = self.agent_factory.create_testing_qa_agent()
        
        # Create all tasks (these would be defined in TaskFactory)
        # For brevity, not all tasks are shown here
        
        # Client requirements tasks
        client_interview_task = self.task_factory.create_client_interview_task(
            project_id=project_id,
            client_data=all_data.get('client_data', {}),
            agent=client_requirements_agent
        )
        
        # More tasks would be defined here for each stage of the process
        
        # Create and return the crew with all agents and tasks
        return Crew(
            agents=[
                client_requirements_agent,
                niche_research_agent,
                seo_strategy_agent,
                content_planning_agent,
                content_generation_agent,
                wordpress_setup_agent,
                design_implementation_agent,
                monetization_agent,
                testing_qa_agent
            ],
            tasks=[
                client_interview_task,
                # More tasks would be added here
            ],
            verbose=2,
            process=Process.sequential
        )
