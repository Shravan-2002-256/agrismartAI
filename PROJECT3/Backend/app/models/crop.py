"""
Crop Database Model
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Crop(Base):
    __tablename__ = "crops"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    crop_type = Column(String(50), nullable=False)
    variety = Column(String(50), nullable=True)
    planted_date = Column(Date, nullable=True)
    expected_harvest = Column(Date, nullable=True)
    area_size = Column(Float, nullable=True)  # in acres or hectares
    location = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Crop(crop_type='{self.crop_type}', user_id={self.user_id})>"
