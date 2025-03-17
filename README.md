# SEO Blog Builder

A SaaS application that creates customized SEO-optimized blog sites for marketing using an agentic architecture.

## Overview

This system uses a central orchestrator agent that directs specialized agents, each responsible for specific tasks in the blog creation process. The architecture is designed around the CrewAI framework, allowing for flexible, collaborative AI agents that work together to create high-quality, SEO-optimized blog sites.

## Agent Architecture

1. **Central Orchestrator Agent** - Manages workflow between specialized agents
2. **Client Requirements Agent** - Extracts and processes client requirements
3. **Niche Research Agent** - Analyzes market opportunities and competition
4. **SEO Strategy Agent** - Develops comprehensive SEO strategy
5. **Content Planning Agent** - Creates detailed content plans
6. **Content Generation Agent** - Produces high-quality, SEO-optimized content
7. **WordPress Setup Agent** - Configures and sets up WordPress sites
8. **Design Implementation Agent** - Implements visually appealing, conversion-optimized designs
9. **Monetization Agent** - Implements revenue generation strategies
10. **Testing & QA Agent** - Ensures quality standards and compliance

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/seo-blog-builder.git
cd seo-blog-builder

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the application
python -m app.main
```

## Development

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
# seo-blog-builder
