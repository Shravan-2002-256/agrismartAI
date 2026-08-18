"""
Market Price Prediction Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.market import MarketPriceResponse
from app.services.market_prediction import market_service

router = APIRouter()

@router.get("/prices", response_model=MarketPriceResponse)
async def get_market_prices(
    crop: str = Query(..., description="Crop type (e.g., tomato, potato)"),
    region: str = Query(None, description="Region/state"),
    current_user: User = Depends(get_current_active_user)
):
    """Get current market prices and predictions"""
    
    try:
        prices = market_service.get_price_forecast(crop, region)
        return prices
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Market price error: {str(e)}"
        )

@router.get("/predict")
async def predict_prices(
    crop: str = Query(...),
    region: str = Query(None),
    days: int = Query(7, ge=1, le=30),
    current_user: User = Depends(get_current_active_user)
):
    """Get price predictions for specified days"""
    
    try:
        predictions = market_service.get_price_forecast(crop, region, days)
        return {
            "success": True,
            "predictions": predictions.get("predictions", [])
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Price prediction error: {str(e)}"
        )
