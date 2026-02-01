import jwt
import bcrypt
from datetime import datetime, timedelta
from config import Config

class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, config: Config):
        self.config = config
        self.jwt_secret = config.JWT_SECRET_KEY
        self.token_expiry = config.JWT_ACCESS_TOKEN_EXPIRES
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self, user_id: str, email: str, role: str) -> str:
        """Generate a JWT token"""
        payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'exp': datetime.utcnow() + self.token_expiry,
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm='HS256')
        return token
    
    def verify_token(self, token: str) -> dict:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def validate_role(self, required_roles: list, user_role: str) -> bool:
        """Check if user has required role"""
        return user_role in required_roles
