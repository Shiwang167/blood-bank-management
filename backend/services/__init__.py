from .auth_service import AuthService
from .memory_db_service import InMemoryDBService

# RDSService requires psycopg2 — import lazily in app.py
# DynamoDBService requires boto3 — only available in AWS environments
try:
    from .rds_service import RDSService
except ImportError:
    RDSService = None

try:
    from .dynamodb_service import DynamoDBService
except ImportError:
    DynamoDBService = None

__all__ = ['AuthService', 'InMemoryDBService', 'RDSService', 'DynamoDBService']
