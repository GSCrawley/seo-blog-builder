"""
Database session and engine for SQLAlchemy.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from app.db.base import Base

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """
    Get a database session.
    
    Yields:
        Session: SQLAlchemy session
        
    Note:
        This function is used as a dependency in FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
