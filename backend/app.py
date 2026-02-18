from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import config
from services import AuthService, InMemoryDBService
from routes import auth_bp, requests_bp, inventory_bp, donor_bp
import os
import logging

# Load .env file before anything else
load_dotenv()

logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    config_obj = config[config_name]()
    app.config.from_object(config_obj)
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize services
    # Use RDSService (PostgreSQL) if DATABASE_URL is explicitly set,
    # otherwise fall back to InMemoryDBService for local development
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        try:
            from services import RDSService
            app.db_service = RDSService(config_obj)
            logger.info("Using PostgreSQL (RDS) database service")
        except Exception as e:
            logger.warning(f"Failed to connect to PostgreSQL: {e}")
            logger.info("Falling back to in-memory database service")
            app.db_service = InMemoryDBService(config_obj)
    else:
        logger.info("No DATABASE_URL set — using in-memory database service (local dev mode)")
        app.db_service = InMemoryDBService(config_obj)
    
    app.auth_service = AuthService(config_obj)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(requests_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(donor_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health():
        db_status = 'connected' if app.db_service.health_check() else 'disconnected'
        return {
            'status': 'healthy' if db_status == 'connected' else 'unhealthy',
            'service': 'BloodBridge API',
            'database': db_status
        }, 200 if db_status == 'connected' else 503
    
    @app.route('/')
    def index():
        return {
            'message': 'BloodBridge API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'requests': '/api/requests',
                'inventory': '/api/inventory',
                'donor': '/api/donor'
            }
        }, 200
    
    return app


if __name__ == '__main__':
    # Get environment
    env = os.getenv('FLASK_ENV', 'development')
    
    # Create app
    app = create_app(env)
    
    # Run app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(env == 'development'))
