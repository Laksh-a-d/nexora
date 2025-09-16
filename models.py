# File: models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

from cloudinary_config import cloudinary


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship to reports
    reports = relationship("Report", back_populates="owner")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, nullable=False)
    landmark = Column(String, nullable=True)
    size = Column(String, nullable=True)
    content_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_path = Column(String, nullable=True)

    # ✅ Change here: string status with default "pending"
    status = Column(String, default="pending")

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="reports")
    
    
    
    
    