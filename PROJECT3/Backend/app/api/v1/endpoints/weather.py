"""
Weather Forecast Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.weather import WeatherResponse
from app.services.weather_service import weather_service

router = APIRouter()

@router.get("/forecast", response_model=WeatherResponse)
async def get_weather_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    current_user: User = Depends(get_current_active_user)
):
    """Get 7-day weather forecast with crop alerts"""
    
    try:
        forecast = weather_service.get_weather_forecast(lat, lon)
        return forecast
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Weather forecast error: {str(e)}"
        )

@router.get("/alerts")
async def get_weather_alerts(
    lat: float = Query(...),
    lon: float = Query(...),
    current_user: User = Depends(get_current_active_user)
):
    """Get crop-specific weather alerts"""
    
    try:
        forecast = weather_service.get_weather_forecast(lat, lon)
        return {
            "success": True,
            "alerts": forecast.get("alerts", [])
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Weather alerts error: {str(e)}"
        )
