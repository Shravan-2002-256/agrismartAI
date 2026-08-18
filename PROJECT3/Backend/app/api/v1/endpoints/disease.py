"""
Disease Detection Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.detection import Detection
from app.models.crop import Crop
from app.schemas.disease import (
    DiseaseDetectionResponse,
    DetectionHistoryResponse,
    DiseaseStatsResponse
)
from app.services.disease_detection_production import disease_detection_service as disease_service

router = APIRouter()

@router.post("/detect", response_model=DiseaseDetectionResponse)
async def detect_disease(
    image: UploadFile = File(...),
    crop_type: str = Form(...),
    location: str = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Detect disease from uploaded crop image"""
    
    # Validate file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Validate file size
    contents = await image.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
        )
    
    # Save image
    file_extension = image.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Detect disease using production service
    try:
        # Call production disease detection service
        result = disease_service.predict(
            image_input=contents,
            crop_type=crop_type,
            user_id=str(current_user.id)
        )
        
        if not result.get('success', False):
            raise Exception(result.get('error', 'Detection failed'))
        
        disease_name = result['disease']
        confidence = result['confidence'] / 100.0  # Convert back to 0-1 range for DB
        severity = result['severity']
        recommendations = result['recommendations']
        
        # Save detection to database
        detection = Detection(
            user_id=current_user.id,
            image_path=file_name,
            disease_detected=disease_name,
            confidence=confidence,
            severity=severity,
            recommendations=recommendations
        )
        
        db.add(detection)
        db.commit()
        db.refresh(detection)
        
        # Return full result from production service plus detection_id
        return {
            **result,  # Include all fields from production service
            "detection_id": detection.id
        }
        
    except Exception as e:
        # Clean up file if error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Disease detection failed: {str(e)}"
        )

@router.get("/history", response_model=List[DetectionHistoryResponse])
async def get_detection_history(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's disease detection history"""
    
    detections = db.query(Detection)\
        .filter(Detection.user_id == current_user.id)\
        .order_by(Detection.detected_at.desc())\
        .limit(limit)\
        .all()
    
    result = []
    for detection in detections:
        # Get crop type if available
        crop_type = None
        if detection.crop_id:
            crop = db.query(Crop).filter(Crop.id == detection.crop_id).first()
            if crop:
                crop_type = crop.crop_type
        
        result.append({
            "id": detection.id,
            "crop_type": crop_type,
            "disease_detected": detection.disease_detected,
            "confidence": detection.confidence,
            "severity": detection.severity,
            "detected_at": detection.detected_at,
            "image_url": f"/uploads/{detection.image_path}"
        })
    
    return result

@router.get("/stats", response_model=DiseaseStatsResponse)
async def get_disease_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get disease detection statistics for user"""
    
    # Total detections
    total = db.query(Detection).filter(Detection.user_id == current_user.id).count()
    
    # Most common diseases
    common_diseases = db.query(
        Detection.disease_detected,
        func.count(Detection.id).label('count')
    ).filter(
        Detection.user_id == current_user.id
    ).group_by(
        Detection.disease_detected
    ).order_by(
        func.count(Detection.id).desc()
    ).limit(5).all()
    
    common_diseases_list = [
        {"disease": disease, "count": count}
        for disease, count in common_diseases
    ]
    
    # Severity distribution
    severity_dist = db.query(
        Detection.severity,
        func.count(Detection.id).label('count')
    ).filter(
        Detection.user_id == current_user.id
    ).group_by(
        Detection.severity
    ).all()
    
    severity_distribution = {
        severity or "unknown": count
        for severity, count in severity_dist
    }
    
    return {
        "total_detections": total,
        "common_diseases": common_diseases_list,
        "severity_distribution": severity_distribution
    }
