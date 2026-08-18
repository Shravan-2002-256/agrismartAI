"""
Initialize Database with Sample Data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.crop import Crop
from app.models.market_price import MarketPrice
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def create_sample_users(db):
    """Create sample users"""
    print("\nCreating sample users...")
    
    users_data = [
        {
            "username": "farmer1",
            "email": "farmer1@agrismart.com",
            "password": "password123",
            "phone": "9876543210",
            "language": "en",
            "location_lat": 28.6139,
            "location_lon": 77.2090
        },
        {
            "username": "farmer2",
            "email": "farmer2@agrismart.com",
            "password": "password123",
            "phone": "9876543211",
            "language": "hi",
            "location_lat": 19.0760,
            "location_lon": 72.8777
        }
    ]
    
    for user_data in users_data:
        # Check if user exists
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if existing_user:
            print(f"User {user_data['username']} already exists, skipping...")
            continue
        
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=get_password_hash(user_data["password"]),
            phone=user_data["phone"],
            language=user_data["language"],
            location_lat=user_data["location_lat"],
            location_lon=user_data["location_lon"]
        )
        
        db.add(user)
        print(f"Created user: {user_data['username']}")
    
    db.commit()

def create_sample_crops(db):
    """Create sample crops"""
    print("\nCreating sample crops...")
    
    users = db.query(User).all()
    
    if not users:
        print("No users found, skipping crop creation")
        return
    
    crops_data = [
        {"crop_type": "tomato", "variety": "Roma", "area_size": 2.5},
        {"crop_type": "potato", "variety": "Russet", "area_size": 3.0},
        {"crop_type": "wheat", "variety": "HD-2967", "area_size": 5.0},
        {"crop_type": "rice", "variety": "Basmati", "area_size": 4.0},
    ]
    
    for user in users:
        for crop_data in crops_data:
            crop = Crop(
                user_id=user.id,
                crop_type=crop_data["crop_type"],
                variety=crop_data["variety"],
                planted_date=datetime.now().date() - timedelta(days=random.randint(30, 90)),
                expected_harvest=datetime.now().date() + timedelta(days=random.randint(30, 120)),
                area_size=crop_data["area_size"],
                location="Farm Area 1"
            )
            db.add(crop)
        
        print(f"Created crops for user: {user.username}")
    
    db.commit()

def create_sample_market_prices(db):
    """Create sample market price data"""
    print("\nCreating sample market prices...")
    
    crops = ["tomato", "potato", "onion", "wheat", "rice", "corn"]
    markets = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]
    
    # Create 90 days of historical data
    for crop in crops:
        base_price = random.uniform(20, 80)
        
        for days_ago in range(90, 0, -1):
            date = datetime.now().date() - timedelta(days=days_ago)
            
            # Add some variation
            price = base_price + random.uniform(-10, 10) + (days_ago * 0.1)
            
            market = random.choice(markets)
            
            market_price = MarketPrice(
                crop_type=crop,
                market_name=market,
                region="India",
                price=round(price, 2),
                unit="quintal",
                recorded_date=date,
                source="AgMarkNet"
            )
            
            db.add(market_price)
        
        print(f"Created market prices for {crop}")
    
    db.commit()

def main():
    """Main initialization function"""
    print("="*50)
    print("AgriSmart AI - Database Initialization")
    print("="*50)
    
    # Initialize database
    init_database()
    
    # Create session
    db = SessionLocal()
    
    try:
        # Create sample data
        create_sample_users(db)
        create_sample_crops(db)
        create_sample_market_prices(db)
        
        print("\n" + "="*50)
        print("Database initialization completed successfully!")
        print("="*50)
        print("\nSample Credentials:")
        print("Username: farmer1 | Password: password123")
        print("Username: farmer2 | Password: password123")
        
    except Exception as e:
        print(f"\nError during initialization: {e}")
        db.rollback()
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
