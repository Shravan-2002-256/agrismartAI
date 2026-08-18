"""
Market Price Data Model
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from app.core.database import Base

class MarketPrice(Base):
    __tablename__ = "market_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(String(50), nullable=False, index=True)
    market_name = Column(String(100), nullable=True)
    region = Column(String(50), nullable=True)
    price = Column(Float, nullable=False)  # price per unit
    unit = Column(String(20), default='quintal')  # kg, quintal, ton
    recorded_date = Column(Date, nullable=False, index=True)
    source = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<MarketPrice(crop='{self.crop_type}', price={self.price}, date={self.recorded_date})>"
