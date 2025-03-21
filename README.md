# SEO Blog Builder

A SaaS application that creates customized SEO-optimized blog sites for marketing using an agentic architecture.

## Overview

SEO Blog Builder is a comprehensive solution for generating fully-optimized blog websites with SEO-focused content. It uses a central orchestrator agent that directs specialized agents, each responsible for specific tasks in the blog creation process.

The architecture is designed around the CrewAI framework, allowing for flexible, collaborative AI agents that work together to create high-quality, SEO-optimized blog sites.

## Architecture

The system uses a multi-agent approach with the following specialized agents:

1. **Central Orchestrator Agent** - Manages workflow between specialized agents
2. **Specialized Agents**:
   - **Client Requirements Agent**: Extract and process client requirements
   - **Niche Research Agent**: Analyze market opportunities and competition
   - **SEO Strategy Agent**: Develop comprehensive SEO strategy
   - **Content Planning Agent**: Create content calendars and plans
   - **Content Generation Agent**: Produce SEO-optimized content
   - **WordPress Setup Agent**: Configure and set up WordPress sites
   - **Design Implementation Agent**: Implement brand-aligned design
   - **Monetization Agent**: Implement affiliate marketing strategies
   - **Testing & QA Agent**: Ensure quality standards and compliance

## Project Structure

```
seo-blog-builder/
├── app/                # Main application code
│   ├── agents/         # Agent implementation
│   ├── crew/           # CrewAI implementation
│   ├── api/            # API endpoints
│   ├── core/           # Core business logic
│   ├── services/       # External service integrations
│   ├── models/         # Data models
│   ├── schemas/        # Pydantic schemas
│   ├── db/             # Database related code
│   └── utils/          # Utility functions
├── frontend/           # React frontend
├── templates/          # WordPress templates
├── prompts/            # LLM prompt templates
├── migrations/         # Database migrations
└── scripts/            # Utility scripts
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11 or higher
- Redis
- PostgreSQL
- Node.js (for frontend)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/seo-blog-builder.git
cd seo-blog-builder
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start the services with Docker Compose:
```bash
docker-compose up -d
```

6. Run the API server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. Set up and run the frontend:
```bash
cd frontend
npm install
npm start
```

## API Documentation

Once the server is running, you can access the API documentation at:
```
http://localhost:8000/docs
```

## Development

### Backend

The backend is built with FastAPI and uses SQLAlchemy for database operations. The CrewAI framework is used for agent coordination.

### Frontend

The frontend is built with React and Material-UI. It provides a user-friendly interface for creating and managing blog sites.

Key features:
- Dashboard for monitoring blog generation projects
- Multi-step blog generation wizard
- Real-time status monitoring
- Analytics dashboard for tracking blog performance
- Settings management

See the [frontend README](./frontend/README.md) for more details on the React application.

## License

MIT License

## Contributors

- Your Name <your-email@example.com>
