"""
Farm Health Score Service
Calculates overall farm health based on multiple factors
"""
import logging
from typing import Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.detection import Detection
from app.models.disease_history import DiseaseHistory

logger = logging.getLogger(__name__)

class FarmHealthService:
    """Calculate farm health score based on various metrics"""
    
    def calculate_health_score(self, db: Session, user_id: int) -> Dict:
        """
        Calculate overall farm health score (0-100)
        
        Factors:
        - Disease detection rate (40%)
        - Recent activity (20%)
        - Crop diversity (20%)
        - Treatment effectiveness (20%)
        """
        try:
            # Get last 30 days data
            cutoff_date = datetime.now() - timedelta(days=30)
            
            # Total detections in last 30 days
            total_detections = db.query(Detection).filter(
                Detection.user_id == user_id,
                Detection.detected_at >= cutoff_date
            ).count()
            
            if total_detections == 0:
                return self._default_score()
            
            # Healthy detections
            healthy_count = db.query(Detection).filter(
                Detection.user_id == user_id,
                Detection.detected_at >= cutoff_date,
                Detection.disease_detected.ilike('%healthy%')
            ).count()
            
            # Calculate health rate (40% weight)
            health_rate = (healthy_count / total_detections * 100) if total_detections > 0 else 0
            health_score = health_rate * 0.4
            
            # Recent activity score (20% weight)
            # More recent scans = better engagement
            recent_7_days = db.query(Detection).filter(
                Detection.user_id == user_id,
                Detection.detected_at >= datetime.now() - timedelta(days=7)
            ).count()
            activity_score = min(recent_7_days / 7 * 100, 100) * 0.2
            
            # Crop diversity score (20% weight)
            unique_crops = db.query(func.count(func.distinct(Detection.crop_type))).filter(
                Detection.user_id == user_id,
                Detection.detected_at >= cutoff_date
            ).scalar()
            diversity_score = min(unique_crops / 3 * 100, 100) * 0.2
            
            # Treatment tracking score (20% weight)
            # Check if user is tracking disease history
            tracked_diseases = db.query(DiseaseHistory).filter(
                DiseaseHistory.user_id == user_id
            ).count()
            tracking_score = min(tracked_diseases / 5 * 100, 100) * 0.2
            
            # Overall score
            overall_score = int(health_score + activity_score + diversity_score + tracking_score)
            
            # Calculate trend (compare with last period)
            previous_period = cutoff_date - timedelta(days=30)
            previous_detections = db.query(Detection).filter(
                Detection.user_id == user_id,
                Detection.detected_at >= previous_period,
                Detection.detected_at < cutoff_date
            ).count()
            
            previous_healthy = db.query(Detection).filter(
                Detection.user_id == user_id,
                Detection.detected_at >= previous_period,
                Detection.detected_at < cutoff_date,
                Detection.disease_detected.ilike('%healthy%')
            ).count()
            
            previous_health_rate = (previous_healthy / previous_detections * 100) if previous_detections > 0 else 0
            trend = int(health_rate - previous_health_rate)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                overall_score, health_rate, recent_7_days, unique_crops
            )
            
            # Count issues (diseased detections)
            issues_detected = total_detections - healthy_count
            
            return {
                "success": True,
                "overall_score": overall_score,
                "health_rate": int(health_rate),
                "healthy_count": healthy_count,
                "total_scans": total_detections,
                "active_crops": unique_crops,
                "issues_detected": issues_detected,
                "trend": trend,
                "breakdown": {
                    "health_contribution": int(health_score),
                    "activity_contribution": int(activity_score),
                    "diversity_contribution": int(diversity_score),
                    "tracking_contribution": int(tracking_score)
                },
                "recommendations": recommendations
            }
            
        except Exception as e:
            logger.error(f"Error calculating health score: {e}")
            return {"success": False, "error": str(e)}
    
    def _default_score(self) -> Dict:
        """Return default score for new users"""
        return {
            "success": True,
            "overall_score": 0,
            "health_rate": 0,
            "healthy_count": 0,
            "total_scans": 0,
            "active_crops": 0,
            "issues_detected": 0,
            "trend": 0,
            "breakdown": {
                "health_contribution": 0,
                "activity_contribution": 0,
                "diversity_contribution": 0,
                "tracking_contribution": 0
            },
            "recommendations": [
                "Start by uploading crop images for disease detection",
                "Regular monitoring helps catch issues early",
                "Track multiple crop types for better insights"
            ]
        }
    
    def _generate_recommendations(
        self, 
        overall_score: int, 
        health_rate: float, 
        recent_activity: int, 
        crop_diversity: int
    ) -> list:
        """Generate personalized recommendations"""
        recommendations = []
        
        if overall_score < 60:
            recommendations.append("Farm health needs attention - increase monitoring frequency")
        
        if health_rate < 70:
            recommendations.append("Disease rate is high - review treatment strategies")
        
        if recent_activity < 3:
            recommendations.append("Increase scan frequency - aim for daily monitoring")
        
        if crop_diversity < 2:
            recommendations.append("Consider crop diversification to reduce disease risk")
        
        if overall_score >= 80:
            recommendations.append("Excellent farm health - maintain current practices")
        
        if len(recommendations) == 0:
            recommendations.append("Farm health is good - continue regular monitoring")
        
        return recommendations

# Global instance
farm_health_service = FarmHealthService()
