"""
Weather Schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WeatherForecast(BaseModel):
    date: str
    temp_min: float
    temp_max: float
    humidity: int
    description: str
    icon: str
    precipitation: Optional[float] = 0
    wind_speed: float

class WeatherAlert(BaseModel):
    alert_type: str
    severity: str
    message: str
    recommendation: str

class WeatherResponse(BaseModel):
    success: bool
    location: str
    current: dict
    forecast: List[WeatherForecast]
    alerts: List[WeatherAlert]
