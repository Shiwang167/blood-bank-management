from .auth import auth_bp
from .requests import requests_bp
from .inventory import inventory_bp
from .donor import donor_bp

__all__ = ['auth_bp', 'requests_bp', 'inventory_bp', 'donor_bp']
