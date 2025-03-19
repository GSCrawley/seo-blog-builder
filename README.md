# SEO Blog Builder

A SaaS application that creates customized SEO-optimized blog sites for marketing using an agentic architecture.

## Project Overview

This system uses a central orchestrator agent that directs specialized agents, each responsible for specific tasks in the blog creation process. The architecture is designed around the CrewAI framework, allowing for flexible, collaborative AI agents that work together to create high-quality, SEO-optimized blog sites.

## What Has Been Done

### Project Structure
- Created a comprehensive directory structure following best practices for a Python FastAPI application
- Set up Docker and Docker Compose for containerized development environment
- Implemented core configuration and environment variables management

### Agent Architecture
- Designed the multi-agent system with a central orchestrator and specialized agents
- Implemented the CrewAI integration for agent coordination
- Created the agent factory for building specialized agents
- Built the task factory for defining agent tasks
- Developed the crew manager for orchestrating agent interactions

### Core Components
- Implemented state management using Redis for tracking project progress
- Created database models for projects, clients, websites, and content
- Set up LLM service integrations with Claude and OpenAI
- Developed helper utilities for logging, validation, and other common tasks

### API Endpoints
- Created project management API endpoints for creating and managing blog projects
- Implemented state tracking and progress monitoring

### Prompt Engineering
- Created several prompt templates for client requirements gathering
- Developed prompt templates for niche research and market analysis
- Added content generation prompts for article creation

## What Needs To Be Done

The structure we've built leverages the CrewAI framework effectively, allowing each specialized agent to focus on its core competency while the central orchestrator manages the workflow. This modular design should make it easier to extend functionality over time or fine-tune specific aspects of the system as needed.

The Redis-based state management will also provide good scalability as your SaaS grows, allowing the system to maintain project state across multiple servers if needed.

As we move forward with development, we might want to prioritize implementing the Client Requirements Agent and Niche Research Agent first, as these form the foundation for all subsequent work in the pipeline. Getting these right will ensure the rest of the system has quality inputs to work with.

### Agent Implementation
- Complete implementation of individual specialized agents:
  - Client Requirements Agent: Finish implementation of requirements validation and processing
  - Niche Research Agent: Implement full market research capabilities
  - SEO Strategy Agent: Develop keyword research and content planning
  - Content Planning Agent: Build content calendar creation functionality
  - Content Generation Agent: Implement content creation with SEO optimization
  - WordPress Setup Agent: Create automated WordPress site setup
  - Design Implementation Agent: Develop theme customization capabilities
  - Monetization Agent: Implement affiliate link management
  - Testing & QA Agent: Build quality assurance procedures

### API Endpoints
- Finish client management API endpoints
- Add content management endpoints
- Implement website management endpoints
- Create analytics endpoints for tracking performance

### Frontend Development
- Design and implement admin dashboard
- Create client portal for project monitoring
- Build interfaces for interacting with agents
- Develop content management interface

### Integration and Services
- Implement SEO tool integrations (SEMrush, Ahrefs)
- Set up WordPress API integration for site management
- Create hosting provider integrations for automated deployment
- Build analytics integration for performance tracking

### Testing and Deployment
- Write unit tests for all components
- Create integration tests for the agent workflow
- Set up CI/CD pipeline for automated testing and deployment
- Implement security measures and authentication

### Documentation
- Create comprehensive API documentation
- Write user guides for the platform
- Develop technical documentation for developers
- Create legal documents (Terms of Service, Privacy Policy)

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11 or higher
- Redis
- PostgreSQL

### Installation

1. Clone the repository
```bash
git clone https://github.com/gscrawley/seo-blog-builder.git
cd seo-blog-builder
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run with Docker Compose
```bash
docker-compose up -d
```

6. Access the API
```
http://localhost:8000/docs
```

## Architecture

### Agent Architecture

1. **Central Orchestrator Agent**
   - Manages workflow between specialized agents
   - Maintains project state and progress tracking

2. **Specialized Agents**
   - Client Requirements Agent: Extract and process client requirements
   - Niche Research Agent: Analyze market opportunities and competition
   - SEO Strategy Agent: Develop comprehensive SEO strategy
   - Content Planning Agent: Create content calendars and plans
   - Content Generation Agent: Produce SEO-optimized content
   - WordPress Setup Agent: Configure and set up WordPress sites
   - Design Implementation Agent: Implement brand-aligned design
   - Monetization Agent: Implement affiliate marketing strategies
   - Testing & QA Agent: Ensure quality standards and compliance

### Directory Structure

```
seo-blog-builder/
├── app/                    # Main application code
│   ├── agents/             # Agent implementation
│   ├── crew/               # CrewAI implementation
│   ├── api/                # API endpoints
│   ├── core/               # Core business logic
│   ├── services/           # External service integrations
│   ├── models/             # Data models
│   ├── schemas/            # Pydantic schemas
│   ├── db/                 # Database related code
│   └── utils/              # Utility functions
├── templates/              # WordPress templates
├── prompts/                # LLM prompt templates
├── migrations/             # Database migrations
├── scripts/                # Utility scripts
└── tests/                  # Test directory
```

## License

[MIT License](LICENSE)
