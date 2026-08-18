"""
User Profile and Crop Management Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.crop import Crop
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.crop import CropCreate, CropResponse, CropUpdate

router = APIRouter()

# User Profile Endpoints

@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user's profile"""
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    
    # Update fields if provided
    if user_update.email is not None:
        # Check if email is already taken by another user
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = user_update.email
    
    if user_update.phone is not None:
        current_user.phone = user_update.phone
    
    if user_update.language is not None:
        current_user.language = user_update.language
    
    if user_update.location_lat is not None:
        current_user.location_lat = user_update.location_lat
    
    if user_update.location_lon is not None:
        current_user.location_lon = user_update.location_lon
    
    db.commit()
    db.refresh(current_user)
    
    return current_user

# Crop Management Endpoints

@router.get("/crops", response_model=List[CropResponse])
async def get_user_crops(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all crops for current user"""
    
    crops = db.query(Crop).filter(Crop.user_id == current_user.id).all()
    return crops

@router.post("/crops", response_model=CropResponse, status_code=status.HTTP_201_CREATED)
async def create_crop(
    crop_data: CropCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a new crop"""
    
    new_crop = Crop(
        user_id=current_user.id,
        crop_type=crop_data.crop_type,
        variety=crop_data.variety,
        planted_date=crop_data.planted_date,
        expected_harvest=crop_data.expected_harvest,
        area_size=crop_data.area_size,
        location=crop_data.location
    )
    
    db.add(new_crop)
    db.commit()
    db.refresh(new_crop)
    
    return new_crop

@router.get("/crops/{crop_id}", response_model=CropResponse)
async def get_crop(
    crop_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get specific crop details"""
    
    crop = db.query(Crop).filter(
        Crop.id == crop_id,
        Crop.user_id == current_user.id
    ).first()
    
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )
    
    return crop

@router.put("/crops/{crop_id}", response_model=CropResponse)
async def update_crop(
    crop_id: int,
    crop_update: CropUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update crop information"""
    
    crop = db.query(Crop).filter(
        Crop.id == crop_id,
        Crop.user_id == current_user.id
    ).first()
    
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )
    
    # Update fields if provided
    update_data = crop_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(crop, field, value)
    
    db.commit()
    db.refresh(crop)
    
    return crop

@router.delete("/crops/{crop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crop(
    crop_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a crop"""
    
    crop = db.query(Crop).filter(
        Crop.id == crop_id,
        Crop.user_id == current_user.id
    ).first()
    
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )
    
    db.delete(crop)
    db.commit()
    
    return None
