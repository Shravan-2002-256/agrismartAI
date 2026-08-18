"""
Smart Notifications Service
Generates intelligent alerts based on various factors
"""
import logging
from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.models.user import User
from app.models.crop import Crop
from app.models.disease_history import DiseaseHistory

logger = logging.getLogger(__name__)

class SmartNotificationService:
    """
    Intelligent notification system that generates alerts based on:
    - Weather conditions
    - Disease outbreaks
    - Price changes
    - Irrigation reminders
    - Harvest dates
    """
    
    def __init__(self):
        logger.info("✅ Smart Notification Service initialized")
    
    def create_notification(
        self,
        db: Session,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        priority: str = "medium",
        action_url: str = None,
        extra_data: Dict = None
    ) -> Notification:
        """Create a new notification"""
        try:
            notification = Notification(
                user_id=user_id,
                type=notification_type,
                title=title,
                message=message,
                priority=priority,
                action_url=action_url,
                extra_data=str(extra_data) if extra_data else None
            )
            db.add(notification)
            db.commit()
            db.refresh(notification)
            return notification
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            db.rollback()
            return None
    
    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Dict]:
        """Get notifications for a user"""
        try:
            query = db.query(Notification).filter(Notification.user_id == user_id)
            
            if unread_only:
                query = query.filter(Notification.is_read == False)
            
            notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
            
            return [
                {
                    "id": n.id,
                    "type": n.type,
                    "title": n.title,
                    "message": n.message,
                    "priority": n.priority,
                    "is_read": n.is_read,
                    "action_url": n.action_url,
                    "created_at": n.created_at.isoformat() if n.created_at else None,
                    "time_ago": self._get_time_ago(n.created_at)
                }
                for n in notifications
            ]
        except Exception as e:
            logger.error(f"Error fetching notifications: {e}")
            return []
    
    def mark_as_read(self, db: Session, notification_id: int, user_id: int) -> bool:
        """Mark notification as read"""
        try:
            notification = db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            ).first()
            
            if notification:
                notification.is_read = True
                notification.read_at = datetime.now()
                db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error marking notification as read: {e}")
            db.rollback()
            return False
    
    def mark_all_as_read(self, db: Session, user_id: int) -> bool:
        """Mark all notifications as read"""
        try:
            db.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).update({"is_read": True, "read_at": datetime.now()})
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Error marking all as read: {e}")
            db.rollback()
            return False
    
    def delete_notification(self, db: Session, notification_id: int, user_id: int) -> bool:
        """Delete a notification"""
        try:
            notification = db.query(Notification).filter(
                Notification.id == notification_id,
                Notification.user_id == user_id
            ).first()
            
            if notification:
                db.delete(notification)
                db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting notification: {e}")
            db.rollback()
            return False
    
    def generate_weather_alert(
        self,
        db: Session,
        user_id: int,
        weather_condition: str,
        temperature: float,
        rainfall: float
    ):
        """Generate weather-based alerts"""
        alerts = []
        
        # Heavy rain alert
        if rainfall > 50:
            self.create_notification(
                db, user_id, "weather",
                "🌧️ Heavy Rainfall Alert",
                f"Heavy rainfall expected ({rainfall}mm). Protect crops from waterlogging. Ensure proper drainage.",
                priority="high",
                action_url="/weather"
            )
            alerts.append("heavy_rain")
        
        # Heat wave alert
        if temperature > 40:
            self.create_notification(
                db, user_id, "weather",
                "🌡️ Heat Wave Warning",
                f"Extreme heat expected ({temperature}°C). Increase irrigation frequency. Provide shade for sensitive crops.",
                priority="critical",
                action_url="/irrigation-calculator"
            )
            alerts.append("heat_wave")
        
        # Frost alert
        if temperature < 5:
            self.create_notification(
                db, user_id, "weather",
                "❄️ Frost Alert",
                f"Frost risk detected ({temperature}°C). Cover sensitive crops. Irrigate before sunset to retain heat.",
                priority="critical",
                action_url="/dashboard"
            )
            alerts.append("frost")
        
        return alerts
    
    def generate_disease_alert(
        self,
        db: Session,
        user_id: int,
        disease_name: str,
        severity: str
    ):
        """Generate disease outbreak alert"""
        if severity in ['high', 'critical']:
            self.create_notification(
                db, user_id, "disease",
                f"⚠️ Disease Alert: {disease_name}",
                f"Severity: {severity.upper()}. Take immediate action. Check Disease Detection for treatment recommendations.",
                priority="high" if severity == 'high' else "critical",
                action_url="/disease-detection"
            )
    
    def generate_irrigation_reminder(
        self,
        db: Session,
        user_id: int,
        crop_type: str,
        days_since_last: int
    ):
        """Generate irrigation reminder"""
        if days_since_last >= 3:
            self.create_notification(
                db, user_id, "irrigation",
                f"💧 Irrigation Reminder: {crop_type}",
                f"It's been {days_since_last} days since last irrigation. Check soil moisture and water if needed.",
                priority="medium",
                action_url="/irrigation-calculator"
            )
    
    def generate_harvest_reminder(
        self,
        db: Session,
        user_id: int,
        crop_type: str,
        days_until_harvest: int
    ):
        """Generate harvest date reminder"""
        if days_until_harvest <= 7:
            self.create_notification(
                db, user_id, "harvest",
                f"🌾 Harvest Approaching: {crop_type}",
                f"Expected harvest in {days_until_harvest} days. Prepare harvesting equipment and storage.",
                priority="high",
                action_url="/profile"
            )
    
    def generate_price_alert(
        self,
        db: Session,
        user_id: int,
        crop_type: str,
        current_price: float,
        price_change: float
    ):
        """Generate market price alert"""
        if price_change > 10:
            self.create_notification(
                db, user_id, "price",
                f"📈 Price Surge: {crop_type}",
                f"{crop_type} prices up {price_change:.1f}%! Current: ₹{current_price}/kg. Good time to sell.",
                priority="high",
                action_url="/market-prices"
            )
        elif price_change < -10:
            self.create_notification(
                db, user_id, "price",
                f"📉 Price Drop: {crop_type}",
                f"{crop_type} prices down {abs(price_change):.1f}%. Consider holding or explore alternatives.",
                priority="medium",
                action_url="/market-prices"
            )
    
    def _get_time_ago(self, dt: datetime) -> str:
        """Get human-readable time ago"""
        if not dt:
            return "Unknown"
        
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 30:
            return f"{diff.days // 30} month{'s' if diff.days // 30 > 1 else ''} ago"
        elif diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} hour{'s' if diff.seconds // 3600 > 1 else ''} ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} minute{'s' if diff.seconds // 60 > 1 else ''} ago"
        else:
            return "Just now"
    
    # COMMENTED OUT - Expert Notification System (ready for future deployment)
    # def notify_expert_consultation(self, consultation_data: Dict) -> Dict:
    #     """
    #     Send notification to agricultural expert about consultation request
    #     
    #     SIMULATED IMPLEMENTATION - Production Ready Architecture
    #     
    #     In production deployment:
    #     - Replace logger.info() with twilio_client.messages.create() for SMS
    #     - Replace logger.info() with sendgrid.send() for email
    #     - Add actual KVK expert database lookup
    #     - Implement location-based routing
    #     
    #     Args:
    #         consultation_data: Consultation request data with farmer and disease details
    #         
    #     Returns:
    #         Dict with notification status
    #     """
    #     try:
    #         # Extract consultation details
    #         farmer_name = consultation_data.get('name', 'N/A')
    #         farmer_phone = consultation_data.get('phone', 'N/A')
    #         farmer_email = consultation_data.get('email', 'N/A')
    #         disease = consultation_data.get('disease', 'Unknown')
    #         confidence = consultation_data.get('confidence', 0)
    #         severity = consultation_data.get('severity', 'N/A')
    #         crop_type = consultation_data.get('crop_type', 'N/A')
    #         notes = consultation_data.get('additional_notes', '')
    #         
    #         # Determine expert contact (simulated routing logic)
    #         expert_phone = self._route_to_nearest_expert(crop_type)
    #         expert_email = self._get_expert_email(crop_type)
    #         
    #         # Generate SMS message content
    #         # sms_message = f"""  URGENT: Expert Consultation Request
    #         # Farmer: {farmer_name} ({farmer_phone})
    #         # Disease: {disease}
    #         # Crop: {crop_type.upper()}
    #         # Confidence: {confidence}%
    #         # Severity: {severity}
    #         # {f'Notes: {notes}' if notes else ''}
    #         # Please contact farmer within 24 hours.
    #         # View details: https://agrismart.com/expert/{consultation_data.get('detection_id', 'N/A')}"""
    #         
    #         # SIMULATED SMS NOTIFICATION
    #         # Production: twilio_client.messages.create(to=expert_phone, from_=TWILIO_NUMBER, body=sms_message)
    #         logger.info("=" * 60)
    #         logger.info("📱 ===== EXPERT NOTIFICATION SYSTEM =====")
    #         logger.info("📱 SMS Notification (SIMULATED - Production Ready)")
    #         logger.info(f"   To: {expert_phone} (KVK Agricultural Expert)")
    #         logger.info(f"   Message:\n{sms_message}")
    #         logger.info("")
    #         
    #         # Generate email content
    #         # email_subject = f"[URGENT] Expert Consultation - {disease}"
    #         # email_body = f"""Dear Agricultural Expert,
    #         # A farmer has requested your expert guidance for a crop disease issue.
    #         # FARMER DETAILS:
    #         # Name: {farmer_name}, Phone: {farmer_phone}, Email: {farmer_email}
    #         # DETECTION DETAILS:
    #         # Crop Type: {crop_type.upper()}, Disease: {disease}
    #         # AI Confidence: {confidence}%, Severity Level: {severity}
    #         # RECOMMENDED ACTION: Please contact the farmer within 24 hours."""
    #         
    #         # SIMULATED EMAIL NOTIFICATION
    #         # Production: sendgrid.send(to=expert_email, subject=email_subject, html=email_html)
    #         logger.info("📧 Email Notification (SIMULATED - Production Ready)")
    #         logger.info(f"   To: {expert_email}")
    #         logger.info(f"   Subject: {email_subject}")
    #         logger.info(f"   Body:\n{email_body}")
    #         logger.info("")
    #         
    #         # Log MongoDB record (would be saved in production)
    #         logger.info("✅ Expert notification logged successfully")
    #         logger.info(f"✅ Notification type: SMS + Email")
    #         logger.info(f"✅ Expert: {expert_phone} / {expert_email}")
    #         logger.info(f"✅ Farmer: {farmer_name} ({farmer_phone})")
    #         logger.info(f"✅ Status: notification_sent (simulated)")
    #         logger.info("=" * 60)
    #         
    #         return {
    #             "success": True,
    #             "sms_sent": True,
    #             "email_sent": True,
    #             "expert_phone": expert_phone,
    #             "expert_email": expert_email,
    #             "status": "simulated"
    #         }
    #         
    #     except Exception as e:
    #         logger.error(f"❌ Error sending expert notification: {e}")
    #         return {
    #             "success": False,
    #             "error": str(e)
    #         }
    # 
    # def _route_to_nearest_expert(self, crop_type: str) -> str:
    #     """
    #     Determine nearest KVK expert based on crop type and location
    #     
    #     SIMULATED - In production:
    #     - Query KVK database by location
    #     - Match expert specialization with crop type
    #     - Check expert availability/workload
    #     """
    #     # Simulated expert routing
    #     expert_database = {
    #         'tomato': '+91-9876543210',
    #         'potato': '+91-9876543211',
    #         'corn': '+91-9876543212',
    #         'wheat': '+91-9876543213',
    #         'rice': '+91-9876543214',
    #     }
    #     return expert_database.get(crop_type.lower(), '+91-9876543210')
    # 
    # def _get_expert_email(self, crop_type: str) -> str:
    #     """Get expert email based on crop specialization"""
    #     # Simulated expert email lookup
    #     email_database = {
    #         'tomato': 'kvk.horticulture@agri.gov.in',
    #         'potato': 'kvk.vegetables@agri.gov.in',
    #         'corn': 'kvk.cereals@agri.gov.in',
    #         'wheat': 'kvk.cereals@agri.gov.in',
    #         'rice': 'kvk.cereals@agri.gov.in',
    #     }
    #     return email_database.get(crop_type.lower(), 'kvk.general@agri.gov.in')
    # 
    # def _determine_location(self, phone: str) -> str:
    #     """Determine farmer location from phone number (simulated)"""
    #     # In production: Use phone prefix or user profile location
    #     return "Maharashtra, India"

# Global instance
notification_service = SmartNotificationService()
