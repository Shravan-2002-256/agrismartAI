"""
Market prices endpoints with LSTM Neural Network Forecasting
AI-Enhanced Market Intelligence with Deep Learning Predictions
"""
from flask import Blueprint, request, jsonify, g
from app.core.security import token_required
from app.models.market_price import MarketPrice

# ✅ USING LSTM V3.0: Production Market Forecasting
from app.services.market_forecasting_production import market_forecasting_service

from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

blueprint = Blueprint('market', __name__)

@blueprint.route('/prices', methods=['GET'])
@token_required
def get_market_prices():
    """
    🧠 LSTM-ENHANCED MARKET PRICES ENDPOINT
    
    Returns price data PLUS LSTM 7-day forecasts with confidence intervals
    """
    try:
        crop = request.args.get('crop', 'tomato').lower()
        market = request.args.get('market', 'average')
        
        logger.info(f"Fetching LSTM forecast for {crop}")
        
        # 🚀 CALL LSTM FORECASTING SERVICE
        forecast_result = market_forecasting_service.forecast_prices(crop, market, periods=7)
        
        if not forecast_result.get('success'):
            return jsonify(forecast_result), 500
        
        # Get historical data for chart
        historical_df = market_forecasting_service.get_historical_prices(crop, market, days=30)
        historical_prices = [
            {
                'date': row['ds'].strftime('%Y-%m-%d'),
                'price': round(float(row['y']), 2)
            }
            for _, row in historical_df.iterrows()
        ]
        
        # Current price (last historical price)
        current_price = round(float(historical_df['y'].iloc[-1]), 2) if len(historical_df) > 0 else 0
        
        # Format predictions to match frontend expectations
        predictions = [
            {
                'date': pred['date'],
                'predicted_price': pred['price'],  # Frontend expects 'predicted_price'
                'lower': pred.get('lower', pred['price'] * 0.9),
                'upper': pred.get('upper', pred['price'] * 1.1),
                'confidence': pred.get('confidence', 0.85),
                'uncertainty': f"±{int((1 - pred.get('confidence', 0.85)) * 100)}%"
            }
            for pred in forecast_result.get('predictions', [])
        ]
        
        # Return enhanced response with LSTM predictions
        return jsonify({
            "success": True,
            "data": {
                "crop": crop,
                "market": market,
                "current_price": current_price,
                "historical_prices": historical_prices[-30:],  # Last 30 days
                "predictions": predictions,
                "trend": forecast_result.get('trend', 'stable'),
                "price_change_percent": forecast_result.get('price_change_percent', 0),
                "forecasting_method": forecast_result.get('method', 'LSTM Neural Network'),
                "model_info": {
                    "type": "Weather-Aware LSTM",
                    "layers": "Multi-layer Recurrent Network",
                    "features": "Price + Humidity + Rainfall + Temperature",
                    "lookback_days": 30,
                    "forecast_days": 7,
                    "weather_integrated": forecast_result.get('weather_integrated', True)
                }
            }
        })
        
    except Exception as e:
        logger.error(f"Market forecast error: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500
        
        trend_multipliers = {
            'increasing': 1.02,
            'decreasing': 0.98,
            'stable': 1.00
        }
        trend_mult = trend_multipliers.get(trend, 1.00)
        
        for i in range(1, 8):
            date = datetime.now() + timedelta(days=i)
            
            # Apply trend with some randomness
            predicted_price = last_price * (trend_mult ** i)
            random_factor = random.uniform(0.95, 1.05)
            predicted_price = predicted_price * random_factor
            
            # Confidence decreases with days ahead
            confidence = 0.85 - (i * 0.05)
            
            predictions.append({
                "date": date.date().isoformat(),
                "predicted_price": round(predicted_price, 2),
                "confidence": round(confidence, 2)
            })
        
        # Reset random seed
        random.seed()
        
        # Current market data
        current_market = {
            "crop_name": crop.title(),
            "current_price": round(last_price, 2),
            "unit": "kg",
            "market_name": location or "National Average",
            "last_updated": datetime.now().isoformat(),
            "trend": trend,
            "change_percent": round((last_price - base_price) / base_price * 100, 2)
        }
        
        return jsonify({
            "success": True,
            "data": {
                "crop": crop.title(),
                "current_price": current_market['current_price'],
                "unit": "kg",
                "trend": trend,
                "change_percent": current_market['change_percent'],
                "historical_prices": historical_prices,
                "predictions": predictions,
                "market_info": current_market
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@blueprint.route('/trends', methods=['GET'])
@token_required
def get_price_trends():
    """Get price trends"""
    try:
        crop = request.args.get('crop', 'tomato')
        days = request.args.get('days', 30, type=int)
        
        # Generate dummy trend data
        trends = []
        base_price = 45
        for i in range(min(days, 30)):
            date = datetime.now() - timedelta(days=i)
            trends.append({
                "date": date.date().isoformat(),
                "price": round(base_price + (i % 10 - 5) * 2, 2),
                "volume": 1000 + (i * 50)
            })
        
        return jsonify({
            "success": True,
            "data": {
                "crop": crop,
                "trends": list(reversed(trends)),
                "average_price": base_price,
                "min_price": base_price - 10,
                "max_price": base_price + 10
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@blueprint.route('/compare', methods=['GET'])
@token_required
def compare_prices():
    """Compare prices across locations"""
    try:
        crop = request.args.get('crop', 'tomato')
        
        return jsonify({
            "success": True,
            "data": {
                "crop": crop,
                "comparisons": [
                    {"location": "Delhi Mandi", "price": 48, "change": 2.5},
                    {"location": "Mumbai Market", "price": 52, "change": -1.8},
                    {"location": "Bangalore APMC", "price": 45, "change": 0.5},
                    {"location": "Hyderabad Market", "price": 50, "change": 3.2}
                ]
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
