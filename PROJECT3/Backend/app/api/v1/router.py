"""
API v1 Router - Combines all endpoint blueprints (Flask Version)
"""
from app.api.v1.endpoints import auth_flask
from app.api.v1.endpoints import disease_flask
from app.api.v1.endpoints import weather_flask
from app.api.v1.endpoints import market_flask
from app.api.v1.endpoints import chat_flask
from app.api.v1.endpoints import user_flask
from app.api.v1.endpoints import insights_flask
from app.api.v1 import irrigation
from app.api.v1 import notifications
from app.api.v1 import disease_analytics
from app.api.v1 import farm_health
from app.api.v1 import reports

def register_blueprints(app, prefix="/api/v1"):
    """Register all Flask blueprints with the app"""
    # Register all blueprints
    app.register_blueprint(auth_flask.blueprint, url_prefix=f"{prefix}/auth")
    app.register_blueprint(disease_flask.blueprint, url_prefix=f"{prefix}/disease")
    app.register_blueprint(weather_flask.blueprint, url_prefix=f"{prefix}/weather")
    app.register_blueprint(market_flask.blueprint, url_prefix=f"{prefix}/market")
    app.register_blueprint(chat_flask.blueprint, url_prefix=f"{prefix}/chat")
    app.register_blueprint(user_flask.blueprint, url_prefix=f"{prefix}/user")
    app.register_blueprint(insights_flask.blueprint, url_prefix=f"{prefix}/insights")
    
    # New features
    app.register_blueprint(irrigation.irrigation_bp)
    app.register_blueprint(notifications.notifications_bp)
    app.register_blueprint(disease_analytics.disease_analytics_bp)
    app.register_blueprint(farm_health.farm_health_bp)
    app.register_blueprint(reports.reports_bp)
