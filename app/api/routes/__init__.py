"""
API routes package.
"""
from app.api.routes.projects import router as projects_router
from app.api.routes.blog_generator import router as blog_generator_router
from app.api.routes.seo import router as seo_router
# Import other routers as they are implemented
# from app.api.routes.clients import router as clients_router
# from app.api.routes.analytics import router as analytics_router

# List all routers that should be included in the API
routers = [
    projects_router,
    blog_generator_router,
    seo_router,
    # Add other routers as they are implemented
    # clients_router,
    # analytics_router,
]
