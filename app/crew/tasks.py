"""
Task factory for creating task definitions for CrewAI agents.
"""
from typing import Dict, Any, List, Optional
from crewai import Task, Agent

class TaskFactory:
    """
    Factory class for creating task definitions for CrewAI agents.
    """
    
    def create_client_interview_task(self, project_id: str, client_data: Dict[str, Any], agent: Agent) -> Task:
        """
        Create a task for conducting a client interview.
        
        Args:
            project_id: Unique identifier for the project
            client_data: Initial client information
            agent: The agent that will perform this task
            
        Returns:
            Task: A CrewAI task for client interview
        """
        return Task(
            description=f"""
            Conduct a comprehensive client interview for project {project_id}.
            
            Client Industry: {client_data.get('industry', 'Not specified')}
            Initial Goals: {client_data.get('goals', 'Not specified')}
            
            Extract the following information:
            1. Target audience demographics and psychographics
            2. Content focus areas and expertise level
            3. Monetization preferences and priorities
            4. Brand voice and positioning
            5. Competitor information and differentiation strategy
            6. Timeline and budget constraints
            7. Technical preferences or requirements
            8. Key performance indicators
            
            Document all responses thoroughly for use in subsequent tasks.
            """,
            agent=agent,
            expected_output="Comprehensive client interview results with detailed responses to all key questions"
        )
    
    def create_requirements_extraction_task(self, project_id: str, agent: Agent, context: List[Task]) -> Task:
        """
        Create a task for extracting business requirements from interview data.
        
        Args:
            project_id: Unique identifier for the project
            agent: The agent that will perform this task
            context: List of tasks that provide context (typically the interview task)
            
        Returns:
            Task: A CrewAI task for requirements extraction
        """
        return Task(
            description=f"""
            Extract formal business requirements from the client interview for project {project_id}.
            
            Analyze the client interview responses and structure them into clear business requirements.
            
            Organize the requirements into the following categories:
            1. Audience Definition
               - Primary audience demographics and psychographics
               - Secondary audience segments if applicable
            
            2. Content Strategy Requirements
               - Primary topics and content focus
               - Content depth and approach
               - Required content elements
            
            3. Monetization Requirements
               - Primary monetization strategies
               - Target affiliate programs if applicable
               - Other revenue generation methods
            
            4. Brand Requirements
               - Voice and tone guidelines
               - Positioning and differentiation
               - Visual style preferences
            
            5. Technical Requirements
               - Platform preferences
               - Design priorities
               - Required features and functionality
            
            6. Timeline and Deliverables
               - Launch timeline
               - Content volume expectations
               - Ongoing maintenance requirements
            
            Ensure all requirements are specific, measurable, achievable, relevant, and time-bound.
            """,
            agent=agent,
            expected_output="Structured business requirements document organized by category",
            context=context
        )
    
    def create_technical_specification_task(self, project_id: str, agent: Agent, context: List[Task]) -> Task:
        """
        Create a task for translating business requirements into technical specifications.
        
        Args:
            project_id: Unique identifier for the project
            agent: The agent that will perform this task
            context: List of tasks that provide context (typically the requirements extraction task)
            
        Returns:
            Task: A CrewAI task for technical specification
        """
        return Task(
            description=f"""
            Translate business requirements into technical specifications for project {project_id}.
            
            Using the structured business requirements, create detailed technical specifications that can be implemented by the technical team.
            
            Include specifications for:
            
            1. WordPress Configuration
               - Theme requirements and recommendations
               - Required plugins with specific features
               - Custom post types and taxonomies needed
               - Page templates required
            
            2. SEO Technical Setup
               - URL structure and permalink settings
               - Schema markup requirements
               - XML sitemap configuration
               - robots.txt configuration
            
            3. Content Structure
               - Content categories and organization
               - Content templates and formats
               - Metadata requirements for different content types
            
            4. Monetization Implementation
               - Affiliate link management approach
               - Ad placement specifications
               - Email capture implementation details
            
            5. Design Requirements
               - Layout specifications for key page types
               - Mobile responsiveness requirements
               - Typography and color palette recommendations
               - Image guidelines and specifications
            
            6. Analytics and Tracking
               - Required tracking implementations
               - Conversion tracking setup
               - Performance monitoring requirements
            
            Ensure specifications are detailed enough for technical implementation while aligning with business requirements.
            """,
            agent=agent,
            expected_output="Comprehensive technical specifications document for implementation",
            context=context
        )
    
    def create_market_analysis_task(self, project_id: str, requirements_data: Dict[str, Any], agent: Agent) -> Task:
        """
        Create a task for market analysis.
        
        Args:
            project_id: Unique identifier for the project
            requirements_data: Client requirements data
            agent: The agent that will perform this task
            
        Returns:
            Task: A CrewAI task for market analysis
        """
        return Task(
            description=f"""
            Perform comprehensive market analysis for potential blog niches related to project {project_id}.
            
            Based on the client requirements:
            Industry: {requirements_data.get('industry', 'Not specified')}
            Target Audience: {requirements_data.get('target_audience', 'Not specified')}
            
            Research and analyze:
            1. Market size and growth trends for 3-5 potential blog niches
            2. Audience demographics and psychographics for each niche
            3. Current trends and hot topics in each niche
            4. Content consumption patterns in each niche (formats, platforms, etc.)
            5. Potential monetization opportunities for each niche
            
            For each potential niche, estimate:
            - Total addressable market
            - Growth rate
            - Audience size and characteristics
            - Content consumption preferences
            - Monetization potential (scale of 1-10)
            
            Provide data-backed insights with sources where possible.
            """,
            agent=agent,
            expected_output="Comprehensive market analysis report for 3-5 potential blog niches with data-backed insights"
        )
    
    def create_competitor_analysis_task(self, project_id: str, requirements_data: Dict[str, Any], agent: Agent, context: List[Task]) -> Task:
        """
        Create a task for competitor analysis.
        
        Args:
            project_id: Unique identifier for the project
            requirements_data: Client requirements data
            agent: The agent that will perform this task
            context: List of tasks that provide context
            
        Returns:
            Task: A CrewAI task for competitor analysis
        """
        return Task(
            description=f"""
            Perform detailed competitor analysis for the potential blog niches identified in the market analysis for project {project_id}.
            
            For each niche identified in the market analysis:
            
            1. Identify the top 5 competitors (blogs, websites) in that niche
            2. Analyze each competitor for:
               - Content strategy (topics, formats, frequency)
               - SEO performance (estimated traffic, keywords ranking for)
               - Monetization methods (affiliate, ads, products, etc.)
               - Audience engagement (comments, social shares)
               - Content quality and depth
               - Unique selling propositions
            
            3. Identify gaps and opportunities by answering:
               - What content topics are underserved?
               - What audience segments are underserved?
               - What content formats are underutilized?
               - What monetization opportunities are being missed?
               - What are common weaknesses across competitors?
            
            Provide specific examples and evidence for each point. Include known competitor names where mentioned by the client:
            {requirements_data.get('competitors', 'None specified')}
            """,
            agent=agent,
            expected_output="Detailed competitor analysis report with identified gaps and opportunities for each potential niche",
            context=context
        )
    
    def create_monetization_potential_task(self, project_id: str, requirements_data: Dict[str, Any], agent: Agent, context: List[Task]) -> Task:
        """
        Create a task for analyzing monetization potential.
        
        Args:
            project_id: Unique identifier for the project
            requirements_data: Client requirements data
            agent: The agent that will perform this task
            context: List of tasks that provide context
            
        Returns:
            Task: A CrewAI task for monetization potential analysis
        """
        return Task(
            description=f"""
            Analyze the monetization potential for each niche identified in the market analysis for project {project_id}.
            
            Client monetization preferences: {requirements_data.get('monetization', 'Not specified')}
            
            For each niche:
            
            1. Identify the top monetization methods:
               - Affiliate marketing opportunities (programs, products, commission rates)
               - Display advertising potential (CPM rates, fill rates)
               - Digital product opportunities (courses, ebooks, templates)
               - Membership/subscription potential
            
            2. For affiliate marketing specifically:
               - List the top 10 affiliate programs relevant to the niche
               - Provide commission rates and cookie duration for each
               - Estimate conversion potential based on audience intent
               - Identify high-ticket vs. low-ticket product opportunities
            
            3. Estimate potential revenue models:
               - Create traffic-based revenue projections for years 1-3
               - Compare revenue potential across different monetization methods
               - Identify the monetization mix with highest potential ROI
            
            4. Analyze monetization-content alignment:
               - Which content types have highest conversion potential
               - How to structure content for optimal monetization
               - Balance between info content and commercial content
            
            Provide a monetization score (1-10) for each niche based on overall revenue potential.
            """,
            agent=agent,
            expected_output="Comprehensive monetization analysis with revenue projections and strategy recommendations for each niche",
            context=context
        )
    
    def create_niche_recommendation_task(self, project_id: str, agent: Agent, context: List[Task]) -> Task:
        """
        Create a task for niche recommendation.
        
        Args:
            project_id: Unique identifier for the project
            agent: The agent that will perform this task
            context: List of tasks that provide context
            
        Returns:
            Task: A CrewAI task for niche recommendation
        """
        return Task(
            description=f"""
            Provide a final niche recommendation for project {project_id} based on all preceding analysis.
            
            Using the insights from:
            - Market analysis
            - Competitor analysis
            - Monetization potential analysis
            
            Create a comprehensive recommendation that includes:
            
            1. Primary Niche Recommendation:
               - Clear definition of the recommended niche
               - Rationale for selection with supporting data
               - Key differentiators and positioning
            
            2. Sub-Niches and Content Categories:
               - 3-5 key sub-niches to focus on
               - Content category structure
               - Priority topics based on opportunity
            
            3. Audience Definition:
               - Detailed primary persona
               - Secondary personas
               - Audience needs and pain points
            
            4. Monetization Strategy:
               - Recommended primary monetization methods
               - Top affiliate programs to partner with
               - Other revenue streams to develop
            
            5. Competitive Advantage:
               - How to differentiate from competitors
               - Unique angle or perspective to adopt
               - Content gaps to exploit
            
            6. Implementation Roadmap:
               - First 90 days content focus
               - Key milestones for niche dominance
               - Growth strategy
            
            Include a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats) for the recommended niche.
            """,
            agent=agent,
            expected_output="Comprehensive niche recommendation with implementation roadmap and SWOT analysis",
            context=context
        )
    
    def create_keyword_research_task(self, project_id: str, niche_data: Dict[str, Any], agent: Agent) -> Task:
        """
        Create a task for keyword research.
        
        Args:
            project_id: Unique identifier for the project
            niche_data: Niche research data
            agent: The agent that will perform this task
            
        Returns:
            Task: A CrewAI task for keyword research
        """
        return Task(
            description=f"""
            Perform comprehensive keyword research for the recommended niche for project {project_id}.
            
            Using the niche recommendation:
            Primary Niche: {niche_data.get('primary_niche', 'Not specified')}
            Sub-Niches: {niche_data.get('sub_niches', 'Not specified')}
            
            Conduct keyword research to:
            
            1. Identify seed keywords:
               - Primary niche keywords
               - Sub-niche keywords
               - Brand-related keywords
               - Competitor keywords
            
            2. Expand seed keywords to discover:
               - Long-tail variations
               - Question-based keywords
               - Commercial intent keywords
               - Informational intent keywords
            
            3. Analyze keyword metrics:
               - Search volume
               - Keyword difficulty
               - CPC (Cost Per Click)
               - SERP features present
               - Commercial intent
            
            4. Categorize keywords by:
               - User intent (informational, navigational, commercial, transactional)
               - Content type suitability (blog post, review, comparison, guide, etc.)
               - Funnel stage (awareness, consideration, decision)
               - Difficulty tier (easy, moderate, competitive)
            
            5. Identify priority keywords based on:
               - Traffic potential
               - Competition level
               - Conversion potential
               - Relevance to niche
            
            Create a comprehensive keyword map with at least 100 target keywords organized by category and priority.
            """,
            agent=agent,
            expected_output="Comprehensive keyword research report with prioritized keyword map"
        )
    
    def create_content_cluster_task(self, project_id: str, agent: Agent, context: List[Task]) -> Task:
        """
        Create a task for content cluster development.
        
        Args:
            project_id: Unique identifier for the project
            agent: The agent that will perform this task
            context: List of tasks that provide context
            
        Returns:
            Task: A CrewAI task for content cluster development
        """
        return Task(
            description=f"""
            Develop a comprehensive content cluster strategy for project {project_id} based on the keyword research.
            
            Using the keyword research results, create:
            
            1. Pillar Content Structure:
               - Identify 5-7 main pillar topics
               - Define the comprehensive topic for each pillar
               - Select primary keywords for each pillar
               - Outline the scope and depth of each pillar
            
            2. Content Cluster Map:
               - Map 8-12 cluster topics for each pillar
               - Assign keywords to each cluster topic
               - Define the relationship between clusters and pillars
               - Ensure comprehensive coverage of the topic space
            
            3. Internal Linking Strategy:
               - Define linking patterns between pillars and clusters
               - Identify cross-linking opportunities between clusters
               - Plan strategic anchor text usage
               - Establish linking hierarchy and depth
            
            4. Content Gap Analysis:
               - Identify topic areas not covered by competitors
               - Find high-opportunity keyword gaps
               - Map competitive advantage areas
               - Prioritize content gaps to fill first
            
            5. Content Type Assignment:
               - Match optimal content types to each topic (guide, list, tutorial, etc.)
               - Recommend content length and depth
               - Assign content priorities (P0, P1, P2)
               - Map conversion potential for each content piece
            
            Create a visual content cluster map showing the relationships between all content pieces.
            """,
            agent=agent,
            expected_output="Comprehensive content cluster strategy with visual map and detailed cluster definitions",
            context=context
        )
    
    def create_site_architecture_task(self, project_id: str, agent: Agent, context: List[Task]) -> Task:
        """
        Create a task for site architecture planning.
        
        Args:
            project_id: Unique identifier for the project
            agent: The agent that will perform this task
            context: List of tasks that provide context
            
        Returns:
            Task: A CrewAI task for site architecture planning
        """
        return Task(
            description=f"""
            Design an optimal site architecture for project {project_id} based on the content cluster strategy.
            
            Using the content cluster strategy, create:
            
            1. URL Structure:
               - Define domain and subdomain strategy
               - Create permalink structure
               - Plan category and tag URLs
               - Ensure SEO-friendly URL patterns
            
            2. Navigation Structure:
               - Design primary navigation menu
               - Plan secondary navigation elements
               - Create mobile navigation approach
               - Design footer navigation structure
            
            3. Page Hierarchy:
               - Define parent-child page relationships
               - Plan content silo structure
               - Design breadcrumb navigation path
               - Map page depth (clicks from homepage)
            
            4. Template Types:
               - Identify required page templates
               - Define template components and modules
               - Plan template variations by content type
               - Design archive page structures
            
            5. Taxonomy Strategy:
               - Define category structure
               - Plan tag implementation
               - Design custom taxonomy needs
               - Create taxonomy relationship map
            
            6. Technical Considerations:
               - Plan XML sitemap structure
               - Design canonical URL strategy
               - Plan pagination handling
               - Map mobile responsiveness requirements
            
            Create a visual site architecture diagram showing the overall structure and relationships.
            """,
            agent=agent,
            expected_output="Comprehensive site architecture plan with visual diagram and detailed specifications",
            context=context
        )
    
    def create_technical_seo_task(self, project_id: str, requirements_data: Dict[str, Any], agent: Agent) -> Task:
        """
        Create a task for technical SEO planning.
        
        Args:
            project_id: Unique identifier for the project
            requirements_data: Client requirements data
            agent: The agent that will perform this task
            
        Returns:
            Task: A CrewAI task for technical SEO planning
        """
        return Task(
            description=f"""
            Develop a comprehensive technical SEO plan for project {project_id}.
            
            Technical preferences: {requirements_data.get('technical_preferences', 'Not specified')}
            
            Create a detailed technical SEO implementation plan including:
            
            1. On-Page SEO:
               - Title tag templates and formats
               - Meta description templates
               - Heading structure guidelines
               - Image optimization requirements
               - Content optimization guidelines
            
            2. Schema Markup:
               - Required schema types by page
               - Article schema implementation
               - Review schema for product content
               - FAQ schema opportunities
               - Organization and website schema
            
            3. Performance Optimization:
               - Page speed requirements
               - Image optimization guidelines
               - CSS and JS handling
               - Critical rendering path optimization
               - Mobile performance considerations
            
            4. Technical Configuration:
               - robots.txt configuration
               - XML sitemap structure
               - Canonical URL implementation
               - hreflang requirements (if multilingual)
               - Pagination handling
            
            5. Indexation Control:
               - Crawl budget optimization
               - Index vs. noindex decisions
               - Follow vs. nofollow strategy
               - Content discovery optimization
               - Archive page handling
            
            6. Tracking Implementation:
               - Google Analytics setup
               - Google Search Console configuration
               - Event tracking requirements
               - Goal configuration
               - E-commerce tracking (if applicable)
            
            Provide step-by-step implementation instructions for WordPress using recommended plugins.
            """,
            agent=agent,
            expected_output="Comprehensive technical SEO plan with implementation instructions for WordPress"
        )
    
    def create_seo_strategy_document_task(self, project_id: str, agent: Agent, context: List[Task]) -> Task:
        """
        Create a task for creating a comprehensive SEO strategy document.
        
        Args:
            project_id: Unique identifier for the project
            agent: The agent that will perform this task
            context: List of tasks that provide context
            
        Returns:
            Task: A CrewAI task for creating an SEO strategy document
        """
        return Task(
            description=f"""
            Create a comprehensive SEO strategy document for project {project_id} that combines all SEO research and planning.
            
            Synthesize the information from:
            - Keyword research
            - Content cluster strategy
            - Site architecture plan
            - Technical SEO plan
            
            Create a complete SEO strategy document including:
            
            1. Executive Summary:
               - Key findings and recommendations
               - Strategic approach overview
               - Expected outcomes and KPIs
               - Implementation timeline
            
            2. Keyword Strategy:
               - Priority keywords by content category
               - Keyword-to-content mapping
               - Competitive keyword opportunities
               - Long-tail keyword strategy
            
            3. Content Strategy:
               - Pillar-cluster content model
               - Content prioritization and roadmap
               - Content types and formats
               - Content updating strategy
            
            4. Technical Implementation:
               - WordPress plugin requirements
               - Technical configuration steps
               - Performance optimization plan
               - Mobile optimization approach
            
            5. On-Page Optimization:
               - Title and meta description templates
               - Content structure guidelines
               - Internal linking strategy
               - Image optimization guidelines
            
            6. Measurement and Reporting:
               - KPI definition and tracking plan
               - Reporting schedule and metrics
               - Success criteria by timeframe
               - Ongoing optimization approach
            
            Include an implementation checklist with sequential steps for executing the strategy.
            """,
            agent=agent,
            expected_output="Comprehensive SEO strategy document with implementation checklist",
            context=context
        )
    
    # Additional task creation methods would follow the same pattern
    # Content planning tasks
    # Content generation tasks
    # WordPress setup tasks
    # Design implementation tasks
    # Monetization tasks
    # Testing and QA tasks
