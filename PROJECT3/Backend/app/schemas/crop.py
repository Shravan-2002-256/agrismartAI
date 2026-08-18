"""
Crop Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class CropBase(BaseModel):
    crop_type: str
    variety: Optional[str] = None
    planted_date: Optional[date] = None
    expected_harvest: Optional[date] = None
    area_size: Optional[float] = None
    location: Optional[str] = None

class CropCreate(CropBase):
    pass

class CropUpdate(BaseModel):
    variety: Optional[str] = None
    planted_date: Optional[date] = None
    expected_harvest: Optional[date] = None
    area_size: Optional[float] = None
    location: Optional[str] = None

class CropResponse(CropBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
