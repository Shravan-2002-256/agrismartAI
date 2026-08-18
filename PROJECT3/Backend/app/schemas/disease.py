"""
Disease Detection Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class DiseaseDetectionRequest(BaseModel):
    crop_type: str = Field(..., description="Type of crop (e.g., tomato, potato)")
    location: Optional[str] = None

class DiseaseDetectionResponse(BaseModel):
    success: bool
    disease: str
    confidence: float
    severity: str
    recommendations: List[Dict[str, str]]
    affected_area: Optional[str] = None
    detection_id: int
    
class DetectionHistoryResponse(BaseModel):
    id: int
    crop_type: Optional[str]
    disease_detected: str
    confidence: float
    severity: Optional[str]
    detected_at: datetime
    image_url: str
    
    class Config:
        from_attributes = True

class DiseaseStatsResponse(BaseModel):
    total_detections: int
    common_diseases: List[Dict[str, any]]
    severity_distribution: Dict[str, int]
