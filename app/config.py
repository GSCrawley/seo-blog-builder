import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    API_KEY: str = os.getenv("API_KEY", "your-api-key-here")
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./seo_blog_builder.db")
    
    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", None)
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    
    # LLM Services
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # SEO Tools
    SEMRUSH_API_KEY: str = os.getenv("SEMRUSH_API_KEY", "")
    AHREFS_API_KEY: str = os.getenv("AHREFS_API_KEY", "")
    
    # Using mock data for SEO (disable when real APIs are available)
    USE_MOCK_DATA: bool = os.getenv("USE_MOCK_DATA", "True").lower() == "true"
    
    # Google Ads API credentials for Keyword Planner
    GOOGLE_ADS_CREDENTIALS: Optional[Dict[str, Any]] = None
    GOOGLE_ADS_CUSTOMER_ID: Optional[str] = os.getenv("GOOGLE_ADS_CUSTOMER_ID", None)
    
    # Web scraping settings
    SCRAPING_PROXIES: Optional[Dict[str, str]] = None
    
    # WordPress
    WP_DEFAULT_USERNAME: str = os.getenv("WP_DEFAULT_USERNAME", "admin")
    WP_DEFAULT_PASSWORD: str = os.getenv("WP_DEFAULT_PASSWORD", "password")
    
    # Hosting (for automated setup)
    HOSTING_API_KEY: str = os.getenv("HOSTING_API_KEY", "")
    HOSTING_API_SECRET: str = os.getenv("HOSTING_API_SECRET", "")
    
    # Agent settings
    DEFAULT_AGENT_TEMPERATURE: float = 0.2
    MAX_AGENT_RETRIES: int = 3
    
    # File paths
    PROMPT_TEMPLATES_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "prompts"
    )
    TEMPLATES_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
        "templates"
    )
    
    # Static site generation settings
    SITES_DIR: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "sites"
    )
    DEFAULT_DOMAIN: str = os.getenv("DEFAULT_DOMAIN", "seoblog.ai")
    
    # Deployment settings
    VERCEL_TOKEN: str = os.getenv("VERCEL_TOKEN", "")
    NETLIFY_TOKEN: str = os.getenv("NETLIFY_TOKEN", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    # Default admin email for sites
    DEFAULT_ADMIN_EMAIL: str = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@seoblog.ai")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create a settings instance
settings = Settings()
