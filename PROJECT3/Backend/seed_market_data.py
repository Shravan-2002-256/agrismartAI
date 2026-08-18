"""
Seed MongoDB with realistic market price data
Run once to populate market_prices collection
"""
import sys
import os

# Add Backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
import numpy as np
from datetime import datetime, timedelta
from app.core.mongodb import connect_mongodb, get_market_prices_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_market_prices():
    """Seed market_prices collection with 90 days of historical data"""
    
    # Connect to MongoDB
    logger.info("Connecting to MongoDB...")
    db = connect_mongodb()
    
    if db is None:
        logger.error("Failed to connect to MongoDB")
        return
    
    collection = get_market_prices_collection()
    
    # Clear existing market prices (optional - comment out to keep existing data)
    # collection.delete_many({'forecasted': False})
    # logger.info("Cleared existing market price data")
    
    # Base prices per kg (realistic Indian market rates)
    crops = {
        'tomato': 35,      # ₹35/kg (range: ₹20-60)
        'potato': 25,      # ₹25/kg (range: ₹15-40)
        'onion': 40,       # ₹40/kg (range: ₹20-80)
        'wheat': 30,       # ₹30/kg (range: ₹25-35)
        'rice': 45,        # ₹45/kg (range: ₹35-60)
        'corn': 28,        # ₹28/kg (range: ₹20-35)
        'apple': 120,      # ₹120/kg (range: ₹80-180)
        'grape': 80,       # ₹80/kg (range: ₹50-120)
        'pepper': 600,     # ₹600/kg (range: ₹400-800)
        'strawberry': 250, # ₹250/kg (range: ₹150-350)
        'peach': 100,      # ₹100/kg (range: ₹60-150)
        'orange': 60,      # ₹60/kg (range: ₹40-90)
        'soybean': 55,     # ₹55/kg (range: ₹40-70)
        'cherry': 500      # ₹500/kg (range: ₹300-700)
    }
    
    days = 90
    total_inserted = 0
    
    logger.info(f"Seeding {len(crops)} crops with {days} days of historical data...")
    
    for crop, base_price in crops.items():
        
        np.random.seed(hash(crop) % 10000)  # Consistent seed per crop
        
        # Generate realistic price variations
        trend = np.linspace(0, 0.2, days)  # 20% upward trend over 90 days
        seasonality = 0.1 * np.sin(np.linspace(0, 4*np.pi, days))  # ±10% seasonal variation
        noise = np.random.normal(0, 0.05, days)  # ±5% daily volatility
        
        prices = base_price * (1 + trend + seasonality + noise)
        
        # Insert data for each day
        for i in range(days):
            date = datetime.utcnow() - timedelta(days=days-i)
            price = round(float(prices[i]), 2)
            
            document = {
                'commodity': crop,
                'market': 'average',
                'date': date,
                'price': price,
                'forecasted': False,
                'created_at': datetime.utcnow()
            }
            
            # Upsert (insert if not exists, update if exists)
            collection.update_one(
                {
                    'commodity': crop,
                    'market': 'average',
                    'date': date,
                    'forecasted': False
                },
                {'$set': document},
                upsert=True
            )
            
            total_inserted += 1
        
        logger.info(f"✓ Seeded {crop}: {days} days, price range ₹{prices.min():.2f}-₹{prices.max():.2f}/kg")
    
    logger.info(f"\n✅ SUCCESS! Seeded {total_inserted} market price records for {len(crops)} crops")
    logger.info(f"📊 Date range: {(datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')} to {datetime.utcnow().strftime('%Y-%m-%d')}")
    
    # Verify data
    count = collection.count_documents({'forecasted': False})
    logger.info(f"📈 Total market price records in MongoDB: {count}")


if __name__ == "__main__":
    try:
        seed_market_prices()
    except Exception as e:
        logger.error(f"❌ Seeding failed: {e}", exc_info=True)
        sys.exit(1)
