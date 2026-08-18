"""
Market Price Schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class MarketPriceData(BaseModel):
    date: date
    price: float
    market: Optional[str] = None

class PricePrediction(BaseModel):
    date: str
    predicted_price: float
    confidence_interval: List[float]

class MarketPriceResponse(BaseModel):
    success: bool
    crop_type: str
    region: Optional[str]
    current_price: float
    unit: str
    historical_prices: List[MarketPriceData]
    predictions: List[PricePrediction]
    trend: str  # "rising", "falling", "stable"
