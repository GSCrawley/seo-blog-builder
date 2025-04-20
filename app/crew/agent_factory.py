"""
Agent factory for creating specialized agents in the CrewAI framework.
"""
from typing import Dict, Any, Optional
from crewai import Agent

from app.config import settings
from app.services.llm.claude import ClaudeService
from app.services.llm.openai import OpenAIService

class AgentFactory:
    """
    Factory class for creating specialized agents in the CrewAI framework.
    """
    
    def __init__(self):
        """Initialize the agent factory with LLM services."""
        self.claude_service = ClaudeService()
        self.openai_service = OpenAIService()
        
    def create_client_requirements_agent(self, **kwargs) -> Agent:
        """
        Create a client requirements agent.
        
        Args:
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent for client requirements tasks
        """
        return Agent(
            role="Client Requirements Specialist",
            goal="Extract comprehensive client requirements and translate them into technical specifications",
            backstory="You are an expert in understanding client needs and translating business requirements into actionable specifications for blog creation.",
            verbose=kwargs.get("verbose", True),
            allow_delegation=kwargs.get("allow_delegation", False),
            llm=self.claude_service.get_llm(),  # Using Claude for natural conversation
            **{k: v for k, v in kwargs.items() if k not in ['verbose', 'allow_delegation']}
        )
        
    def create_niche_research_agent(self, **kwargs) -> Agent:
        """
        Create a niche research agent.
        
        Args:
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent for niche research tasks
        """
        return Agent(
            role="Niche Research Specialist",
            goal="Identify the most profitable and viable niche for the client's blog",
            backstory="You are an expert in market research, competitive analysis, and finding profitable niches for content websites.",
            verbose=kwargs.get("verbose", True),
            allow_delegation=kwargs.get("allow_delegation", False),
            llm=self.openai_service.get_llm(),  # Using OpenAI for market analysis
            **{k: v for k, v in kwargs.items() if k not in ['verbose', 'allow_delegation']}
        )
        
    def create_seo_strategy_agent(self, **kwargs) -> Agent:
        """
        Create an SEO strategy agent.
        
        Args:
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent for SEO strategy tasks
        """
        return Agent(
            role="SEO Strategist",
            goal="Develop a comprehensive SEO strategy that will drive organic traffic and conversions",
            backstory="You are a seasoned SEO professional who specializes in developing content strategies that rank well in search engines and convert visitors.",
            verbose=kwargs.get("verbose", True),
            allow_delegation=kwargs.get("allow_delegation", False),
            llm=self.openai_service.get_llm(),  # Using OpenAI for SEO analysis
            **{k: v for k, v in kwargs.items() if k not in ['verbose', 'allow_delegation']}
        )
    
    def create_content_planning_agent(self, **kwargs) -> Agent:
        """
        Create a content planning agent.
        
        Args:
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent for content planning tasks
        """
        return Agent(
            role="Content Planning Specialist",
            goal="Create detailed content plans including content calendars, templates, and editorial guidelines",
            backstory="You are a content strategist with extensive experience in developing editorial calendars and content structures for high-performing blogs.",
            verbose=kwargs.get("verbose", True),
            allow_delegation=kwargs.get("allow_delegation", False),
            llm=self.claude_service.get_llm(),  # Using Claude for creative planning
            **{k: v for k, v in kwargs.items() if k not in ['verbose', 'allow_delegation']}
        )
    
    def create_content_generation_agent(self, **kwargs) -> Agent:
        """
        Create a content generation agent.
        
        Args:
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent for content generation tasks
        """
        return Agent(
            role="Content Creation Specialist",
            goal="Produce high-quality, SEO-optimized content based on content plans and SEO strategy",
            backstory="You are a skilled content creator specializing in writing engaging, informative content that ranks well and converts visitors.",
            verbose=kwargs.get("verbose", True),
            allow_delegation=kwargs.get("allow_delegation", False),
            llm=self.claude_service.get_llm(),  # Using Claude for content creation
            **{k: v for k, v in kwargs.items() if k not in ['verbose', 'allow_delegation']}
        )
    
    def create_wordpress_setup_agent(self, **kwargs) -> Agent:
        """
        Create a WordPress setup agent.
        
        Args:
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent for WordPress setup tasks
        """
        # Import WordPress tools
        from app.tools.wordpress_tools import (
            CreatePostTool, CreateCategoryTool, CreateTagTool,
            UploadMediaTool, SetupBlogTool
        )
        
        # Create WordPress tools
        wordpress_tools = [
            CreatePostTool(),
            CreateCategoryTool(),
            CreateTagTool(),
            UploadMediaTool(),
            SetupBlogTool()
        ]
        
        return Agent(
            role="WordPress Technical Specialist",
            goal="Configure and set up WordPress sites with appropriate themes, plugins, and technical SEO settings",
            backstory="You are a WordPress expert who specializes in creating optimized, high-performance blog sites with the right technical configuration. You know how to implement SEO best practices in WordPress and how to create a site architecture that supports content strategy.",
            verbose=kwargs.get("verbose", True),
            allow_delegation=kwargs.get("allow_delegation", False),
            tools=kwargs.get("tools", wordpress_tools),
            llm=self.openai_service.get_llm(),  # Using OpenAI for technical tasks
            **{k: v for k, v in kwargs.items() if k not in ['verbose', 'allow_delegation', 'tools']}
        )
    
    def create_design_implementation_agent(self, **kwargs) -> Agent:
        """
        Create a design implementation agent.
        
        Args:
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent for design implementation tasks
        """
        return Agent(
            role="Design Implementation Specialist",
            goal="Create and implement visually appealing, conversion-optimized designs aligned with brand identity",
            backstory="You are a web designer with a strong focus on creating beautiful, functional designs that drive conversions and enhance user experience.",
            verbose=kwargs.get("verbose", True),
            allow_delegation=kwargs.get("allow_delegation", False),
            llm=self.claude_service.get_llm(),  # Using Claude for creative design
            **{k: v for k, v in kwargs.items() if k not in ['verbose', 'allow_delegation']}
        )
    
    def create_monetization_agent(self, **kwargs) -> Agent:
        """
        Create a monetization agent.
        
        Args:
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent for monetization tasks
        """
        return Agent(
            role="Monetization Specialist",
            goal="Implement and optimize revenue generation strategies including affiliate marketing and email capture",
            backstory="You are an expert in blog monetization with a focus on affiliate marketing, email list building, and conversion optimization.",
            verbose=kwargs.get("verbose", True),
            allow_delegation=kwargs.get("allow_delegation", False),
            llm=self.openai_service.get_llm(),  # Using OpenAI for strategic tasks
            **{k: v for k, v in kwargs.items() if k not in ['verbose', 'allow_delegation']}
        )
    
    def create_testing_qa_agent(self, **kwargs) -> Agent:
        """
        Create a testing and QA agent.
        
        Args:
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent for testing and QA tasks
        """
        return Agent(
            role="Testing and QA Specialist",
            goal="Ensure all aspects of the blog site meet quality standards, function correctly, and comply with best practices",
            backstory="You are a meticulous quality assurance specialist who ensures websites are fully functional, properly optimized, and free of issues.",
            verbose=kwargs.get("verbose", True),
            allow_delegation=kwargs.get("allow_delegation", False),
            llm=self.openai_service.get_llm(),  # Using OpenAI for analytical tasks
            **{k: v for k, v in kwargs.items() if k not in ['verbose', 'allow_delegation']}
        )
    
    def create_agent_by_type(self, agent_type: str, **kwargs) -> Agent:
        """
        Create an agent of the specified type.
        
        Args:
            agent_type: Type of agent to create
            **kwargs: Additional parameters for agent customization
            
        Returns:
            Agent: A CrewAI agent of the specified type
        
        Raises:
            ValueError: If an invalid agent type is specified
        """
        agent_creators = {
            "client_requirements": self.create_client_requirements_agent,
            "niche_research": self.create_niche_research_agent,
            "seo_strategy": self.create_seo_strategy_agent,
            "content_planning": self.create_content_planning_agent,
            "content_generation": self.create_content_generation_agent,
            "wordpress_setup": self.create_wordpress_setup_agent,
            "design_implementation": self.create_design_implementation_agent,
            "monetization": self.create_monetization_agent,
            "testing_qa": self.create_testing_qa_agent
        }
        
        if agent_type not in agent_creators:
            raise ValueError(f"Invalid agent type: {agent_type}")
            
        return agent_creators[agent_type](**kwargs)
