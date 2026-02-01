import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database (PostgreSQL RDS)
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/bloodbank')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGIN', 'http://localhost:5173').split(',')
    
    # Blood donation eligibility (days)
    DONATION_INTERVAL_DAYS = 90  # 3 months between donations
    
    # Inventory thresholds
    LOW_STOCK_THRESHOLD = 5
    CRITICAL_STOCK_THRESHOLD = 3


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # Use local PostgreSQL for development
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/bloodbank_dev')


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
