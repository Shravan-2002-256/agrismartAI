"""
User Database Model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    phone = Column(String(15), nullable=True)
    language = Column(String(10), default='en')
    location_lat = Column(Float, nullable=True)
    location_lon = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    
    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
