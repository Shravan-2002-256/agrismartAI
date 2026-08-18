"""
Notification Model
Stores user notifications and alerts
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String(50), nullable=False)  # weather, disease, price, irrigation, harvest
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String(20), default='medium')  # low, medium, high, critical
    is_read = Column(Boolean, default=False)
    action_url = Column(String(200), nullable=True)
    extra_data = Column(Text, nullable=True)  # JSON data for additional info (renamed from metadata)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Notification(user_id={self.user_id}, type='{self.type}', title='{self.title}')>"
