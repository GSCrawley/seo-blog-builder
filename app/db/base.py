"""
Base model and database session for SQLAlchemy.
"""
from sqlalchemy.ext.declarative import declarative_base

# Create base class for SQLAlchemy models
Base = declarative_base()
