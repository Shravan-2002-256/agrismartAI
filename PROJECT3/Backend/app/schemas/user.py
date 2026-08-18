"""
User Pydantic Schemas for Request/Response
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    phone: Optional[str] = None
    language: str = Field(default='en', pattern='^(en|hi|te|ta)$')
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    language: Optional[str] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
