# SEO Blog Builder Frontend

This is the frontend React application for the SEO Blog Builder SaaS application. It provides a user interface for creating and managing SEO-optimized blogs generated through our agent-based architecture.

## Features

- Dashboard for monitoring blog generation projects
- Blog generator wizard with multi-step form
- Real-time status monitoring for ongoing blog generation
- Analytics dashboard for performance tracking
- Settings management
- Integration with backend API endpoints

## Prerequisites

- Node.js (v14+)
- npm or yarn
- Backend API running on http://localhost:8000

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will be available at http://localhost:3000.

## Project Structure

```
frontend/
├── public/             # Static files
├── src/
│   ├── components/     # Reusable UI components
│   │   ├── Layout.js            # Main application layout
│   │   ├── LoadingState.js      # Loading indicator component
│   │   ├── ErrorState.js        # Error display component
│   │   ├── EmptyState.js        # Empty state component
│   │   └── StatusCard.js        # Blog status card component
│   ├── pages/         # Page components
│   │   ├── Dashboard.js         # Main dashboard page
│   │   ├── BlogGenerator.js     # Blog creation wizard
│   │   ├── BlogStatus.js        # Status monitoring page
│   │   ├── Analytics.js         # Analytics dashboard
│   │   └── Settings.js          # Settings page
│   ├── services/      # API service functions
│   │   └── blogService.js       # Blog API service
│   ├── utils/         # Utility functions
│   │   └── apiUtils.js          # API error handling utilities
│   ├── App.js          # Main application component
│   └── index.js        # Application entry point
└── package.json        # Project dependencies
```

## Key Components

### Layout.js
Main layout with navigation sidebar that provides consistent UI structure across all pages.

### BlogGenerator.js
Multi-step form for creating new blogs with the following steps:
1. Topic - Select a blog topic and industry
2. Audience - Define target audience and characteristics
3. Content - Set content preferences and structure
4. Monetization - Configure monetization strategies

### BlogStatus.js
Status monitoring for blog generation with real-time updates, progress tracking, and activity timeline.

### Dashboard.js
Overview of all blog projects with status cards and quick access to project details.

### Analytics.js
Dashboard for tracking performance metrics of generated blogs including traffic, content performance, SEO metrics, and conversions.

### Settings.js
Configuration page for API keys, email notifications, branding, and storage settings.

## Services

### blogService.js
Provides API functions for interacting with the backend:
- `createBlog(blogData)` - Create a new blog generation project
- `getBlogStatus(projectId)` - Get current status of a blog project
- `cancelBlogGeneration(projectId)` - Cancel an ongoing blog generation process
- `getAllBlogs()` - Retrieve all blog projects

## Utilities

### apiUtils.js
Utilities for handling API errors and formatting error messages consistently:
- `formatApiError(error)` - Format error messages from API responses
- `handleApiError(error, setError, setLoading)` - Handle API errors consistently

## Development

The frontend proxies API requests to the backend server running on port 8000. Make sure the backend server is running before starting the frontend development server.

### Adding New Pages
1. Create a new page component in the `src/pages` directory
2. Add the route to `App.js`
3. Add the page to the navigation in `Layout.js`

### Adding New Components
1. Create a new component in the `src/components` directory
2. Import and use the component in your pages

### Adding New API Services
1. Create a new service file in the `src/services` directory
2. Use axios for API requests and follow the pattern in existing services

## Building for Production

To create a production build:

```bash
npm run build
```

The build artifacts will be stored in the `build/` directory, ready to be deployed to a web server.
