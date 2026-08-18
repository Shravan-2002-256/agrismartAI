"""
Disease History Analytics Service
Provides insights and trends from disease detection history
"""
import logging
import json
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.disease_history import DiseaseHistory
from collections import Counter

logger = logging.getLogger(__name__)

class DiseaseAnalyticsService:
    """
    Analytics service for disease history
    Provides trends, patterns, and insights
    """
    
    def __init__(self):
        logger.info("✅ Disease Analytics Service initialized")
    
    def save_detection(
        self,
        db: Session,
        user_id: int,
        disease_name: str,
        confidence: float,
        severity: str,
        crop_type: str = None,
        crop_id: int = None,
        field_location: str = None,
        image_path: str = None,
        weather_conditions: Dict = None
    ) -> DiseaseHistory:
        """Save disease detection to history"""
        try:
            detection = DiseaseHistory(
                user_id=user_id,
                crop_id=crop_id,
                disease_name=disease_name,
                confidence=confidence,
                severity=severity,
                crop_type=crop_type,
                field_location=field_location,
                image_path=image_path,
                weather_conditions=json.dumps(weather_conditions) if weather_conditions else None
            )
            db.add(detection)
            db.commit()
            db.refresh(detection)
            return detection
        except Exception as e:
            logger.error(f"Error saving detection: {e}")
            db.rollback()
            return None
    
    def get_user_history(
        self,
        db: Session,
        user_id: int,
        days: int = 30,
        limit: int = 50
    ) -> List[Dict]:
        """Get user's disease detection history"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            detections = db.query(DiseaseHistory).filter(
                DiseaseHistory.user_id == user_id,
                DiseaseHistory.created_at >= cutoff_date
            ).order_by(DiseaseHistory.created_at.desc()).limit(limit).all()
            
            return [
                {
                    "id": d.id,
                    "disease_name": d.disease_name,
                    "confidence": round(d.confidence, 1),  # Already stored as percentage
                    "severity": d.severity,
                    "crop_type": d.crop_type,
                    "field_location": d.field_location,
                    "treatment_applied": d.treatment_applied,
                    "treatment_result": d.treatment_result,
                    "created_at": d.created_at.isoformat() if d.created_at else None,
                    "days_ago": (datetime.now() - d.created_at).days if d.created_at else 0
                }
                for d in detections
            ]
        except Exception as e:
            logger.error(f"Error fetching history: {e}")
            return []
    
    def get_disease_trends(
        self,
        db: Session,
        user_id: int,
        days: int = 30
    ) -> Dict:
        """Get disease trends and analytics"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get all detections in period
            detections = db.query(DiseaseHistory).filter(
                DiseaseHistory.user_id == user_id,
                DiseaseHistory.created_at >= cutoff_date
            ).all()
            
            if not detections:
                return {
                    "total_detections": 0,
                    "unique_diseases": 0,
                    "most_common_diseases": [],
                    "crop_wise_diseases": {},
                    "severity_distribution": {},
                    "monthly_trend": [],
                    "health_score": 100
                }
            
            # Analysis
            total = len(detections)
            disease_names = [d.disease_name for d in detections]
            disease_counts = Counter(disease_names)
            
            # Most common diseases
            most_common = [
                {"disease": name, "count": count, "percentage": round(count/total*100, 1)}
                for name, count in disease_counts.most_common(5)
            ]
            
            # Crop-wise breakdown
            crop_wise = {}
            for d in detections:
                crop = d.crop_type or "Unknown"
                if crop not in crop_wise:
                    crop_wise[crop] = []
                crop_wise[crop].append(d.disease_name)
            
            crop_disease_summary = {
                crop: {
                    "total": len(diseases),
                    "unique": len(set(diseases)),
                    "most_common": Counter(diseases).most_common(3)
                }
                for crop, diseases in crop_wise.items()
            }
            
            # Severity distribution
            severity_counts = Counter([d.severity for d in detections if d.severity])
            severity_dist = {
                severity: {
                    "count": count,
                    "percentage": round(count/total*100, 1)
                }
                for severity, count in severity_counts.items()
            }
            
            # Monthly trend (last 30 days)
            daily_counts = {}
            for d in detections:
                date_key = d.created_at.date().isoformat() if d.created_at else "unknown"
                daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
            
            # Health score (100 - disease frequency)
            healthy_count = sum(1 for d in detections if 'healthy' in d.disease_name.lower())
            health_score = min(100, int((healthy_count / total) * 100)) if total > 0 else 100
            
            return {
                "total_detections": total,
                "unique_diseases": len(disease_counts),
                "most_common_diseases": most_common,
                "crop_wise_diseases": crop_disease_summary,
                "severity_distribution": severity_dist,
                "monthly_trend": [
                    {"date": date, "count": count}
                    for date, count in sorted(daily_counts.items())
                ],
                "health_score": health_score,
                "healthy_scans": healthy_count,
                "diseased_scans": total - healthy_count
            }
            
        except Exception as e:
            logger.error(f"Error calculating trends: {e}")
            return {"error": str(e)}
    
    def get_treatment_effectiveness(
        self,
        db: Session,
        user_id: int
    ) -> Dict:
        """Analyze treatment effectiveness"""
        try:
            # Get detections with treatment results
            treated = db.query(DiseaseHistory).filter(
                DiseaseHistory.user_id == user_id,
                DiseaseHistory.treatment_applied.isnot(None),
                DiseaseHistory.treatment_result.isnot(None)
            ).all()
            
            if not treated:
                return {
                    "total_treatments": 0,
                    "effective": 0,
                    "ineffective": 0,
                    "pending": 0,
                    "success_rate": 0
                }
            
            result_counts = Counter([t.treatment_result for t in treated])
            
            effective = result_counts.get('effective', 0)
            ineffective = result_counts.get('ineffective', 0)
            pending = result_counts.get('pending', 0)
            
            success_rate = int((effective / (effective + ineffective)) * 100) if (effective + ineffective) > 0 else 0
            
            return {
                "total_treatments": len(treated),
                "effective": effective,
                "ineffective": ineffective,
                "pending": pending,
                "success_rate": success_rate
            }
            
        except Exception as e:
            logger.error(f"Error analyzing treatments: {e}")
            return {"error": str(e)}
    
    def get_field_wise_analysis(
        self,
        db: Session,
        user_id: int
    ) -> Dict:
        """Get field/location-wise disease analysis"""
        try:
            detections = db.query(DiseaseHistory).filter(
                DiseaseHistory.user_id == user_id,
                DiseaseHistory.field_location.isnot(None)
            ).all()
            
            field_diseases = {}
            for d in detections:
                field = d.field_location
                if field not in field_diseases:
                    field_diseases[field] = []
                field_diseases[field].append(d.disease_name)
            
            field_analysis = {
                field: {
                    "total_detections": len(diseases),
                    "unique_diseases": len(set(diseases)),
                    "most_common": Counter(diseases).most_common(3),
                    "risk_level": "high" if len(diseases) > 10 else "medium" if len(diseases) > 5 else "low"
                }
                for field, diseases in field_diseases.items()
            }
            
            return field_analysis
            
        except Exception as e:
            logger.error(f"Error in field analysis: {e}")
            return {}
    
    def update_treatment_result(
        self,
        db: Session,
        detection_id: int,
        user_id: int,
        treatment_applied: str,
        treatment_result: str,
        notes: str = None
    ) -> bool:
        """Update treatment results for a detection"""
        try:
            detection = db.query(DiseaseHistory).filter(
                DiseaseHistory.id == detection_id,
                DiseaseHistory.user_id == user_id
            ).first()
            
            if detection:
                detection.treatment_applied = treatment_applied
                detection.treatment_result = treatment_result
                if notes:
                    detection.notes = notes
                detection.updated_at = datetime.now()
                db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating treatment result: {e}")
            db.rollback()
            return False

# Global instance
disease_analytics = DiseaseAnalyticsService()
