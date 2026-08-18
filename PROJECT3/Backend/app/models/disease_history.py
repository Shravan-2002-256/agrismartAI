"""
Disease History Model
Tracks all disease detections for analytics
"""
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class DiseaseHistory(Base):
    __tablename__ = "disease_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    crop_id = Column(Integer, ForeignKey('crops.id'), nullable=True)
    disease_name = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String(20), nullable=True)  # none, low, moderate, high, critical
    crop_type = Column(String(50), nullable=True)
    field_location = Column(String(100), nullable=True)
    image_path = Column(String(300), nullable=True)
    treatment_applied = Column(Text, nullable=True)
    treatment_result = Column(String(50), nullable=True)  # pending, effective, ineffective
    notes = Column(Text, nullable=True)
    weather_conditions = Column(Text, nullable=True)  # Store weather as JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<DiseaseHistory(disease='{self.disease_name}', crop_type='{self.crop_type}', confidence={self.confidence})>"
