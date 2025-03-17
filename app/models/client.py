"""
Client model for database.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base

class Client(Base):
    """Client model representing a customer in the system."""
    __tablename__ = "clients"

    id = Column(String, primary_key=True, index=True, default=lambda: f"CL-{uuid.uuid4().hex[:8].upper()}")
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="client")
    
    def __repr__(self):
        return f"<Client {self.id}: {self.name}>"
