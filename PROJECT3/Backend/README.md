# AgriSmart AI - Backend

Intelligent Agricultural Advisory System backend built with FastAPI, TensorFlow, and PostgreSQL.

## Features

- 🌿 **Disease Detection**: Deep learning-based crop disease identification (EfficientNetB0)
- 🌤️ **Weather Forecasting**: Location-based weather alerts for farmers
- 💰 **Market Price Prediction**: LSTM-based price forecasting
- 💬 **Multi-lingual Chatbot**: Support for English, Hindi, Telugu, Tamil
- 🔐 **Authentication**: JWT-based secure authentication
- 📊 **Analytics**: Track detection history and user insights

## Tech Stack

- **Framework**: FastAPI 0.104+
- **ML/AI**: TensorFlow 2.15, Prophet, spaCy
- **Databases**: PostgreSQL, MongoDB, Redis
- **Authentication**: JWT (python-jose)

## Quick Start

### 1. Prerequisites

- Python 3.9+
- PostgreSQL 14+
- MongoDB 6+
- Redis 7+

### 2. Installation

```bash
# Clone and navigate
cd Backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Copy environment file
cp .env.example .env
# Edit .env with your configuration
```

### 3. Database Setup

```bash
# Run migrations
alembic upgrade head

# Or use the init script
python scripts/init_db.py
```

### 4. Download & Prepare ML Models

```bash
# Download PlantVillage dataset
python scripts/download_dataset.py

# Train disease detection model (optional - pre-trained included)
python ml_models/train_disease_model.py

# Train market price prediction model
python ml_models/train_market_model.py
```

### 5. Run the Server

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

API Documentation will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
Backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── disease.py
│   │       │   ├── weather.py
│   │       │   ├── market.py
│   │       │   ├── chat.py
│   │       │   └── user.py
│   │       └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/
│   │   ├── user.py
│   │   ├── crop.py
│   │   └── detection.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── disease.py
│   │   └── market.py
│   ├── services/
│   │   ├── disease_detection.py
│   │   ├── weather_service.py
│   │   ├── market_prediction.py
│   │   └── chatbot_service.py
│   ├── utils/
│   │   ├── image_processing.py
│   │   └── helpers.py
│   └── main.py
├── ml_models/
│   ├── train_disease_model.py
│   ├── train_market_model.py
│   └── inference.py
├── scripts/
│   ├── download_dataset.py
│   ├── init_db.py
│   └── create_sample_data.py
├── tests/
├── models/  # Trained ML models
├── data/    # Datasets
├── uploads/ # User uploaded images
├── logs/    # Application logs
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh token

### Disease Detection
- `POST /api/v1/disease/detect` - Detect disease from image
- `GET /api/v1/disease/history` - Get detection history
- `GET /api/v1/disease/stats` - Get disease statistics

### Weather
- `GET /api/v1/weather/forecast` - Get weather forecast
- `GET /api/v1/weather/alerts` - Get crop-specific alerts

### Market Prices
- `GET /api/v1/market/prices` - Get current prices
- `GET /api/v1/market/predict` - Get price predictions

### Chatbot
- `POST /api/v1/chat/query` - Send chat message
- `GET /api/v1/chat/history` - Get chat history

### User Profile
- `GET /api/v1/user/profile` - Get user profile
- `PUT /api/v1/user/profile` - Update profile
- `GET /api/v1/user/crops` - Get saved crops
- `POST /api/v1/user/crops` - Add new crop

## Environment Variables

See `.env.example` for all required environment variables.

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_disease_detection.py
```

## Deployment

### Using Docker (Recommended)

```bash
docker-compose up -d
```

### Manual Deployment

1. Set up production database
2. Configure environment variables
3. Run migrations
4. Start with gunicorn/uvicorn workers

## Performance

- Disease detection: < 2 seconds
- Model size: ~50MB (EfficientNetB0)
- Accuracy: 90%+ on PlantVillage dataset
- API response time: < 100ms (cached)

## License

MIT License - See LICENSE file

## Support

For issues and questions, contact the development team.
