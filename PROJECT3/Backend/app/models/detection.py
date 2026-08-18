"""
Disease Detection History Model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Detection(Base):
    __tablename__ = "detections"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    crop_id = Column(Integer, ForeignKey('crops.id'), nullable=True)
    crop_type = Column(String(50), nullable=True)  # Store crop type directly
    image_path = Column(String(255), nullable=False)
    disease_detected = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String(20), nullable=True)  # low, moderate, high, none
    recommendations = Column(Text, nullable=True)  # Text for SQLite compatibility
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Detection(disease='{self.disease_detected}', confidence={self.confidence})>"
