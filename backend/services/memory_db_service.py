"""
In-Memory Database Service
A simple replacement for DynamoDB for local testing without Docker
"""
from datetime import datetime
import uuid

class InMemoryDBService:
    """Service for in-memory database operations (replaces DynamoDB for testing)"""
    
    def __init__(self, config):
        self.config = config
        
        # In-memory storage
        self.users = {}  # user_id -> user_data
        self.users_by_email = {}  # email -> user_id
        self.requests = {}  # request_id -> request_data
        self.inventory = {}  # blood_type -> inventory_data
        
        # Initialize inventory with all blood types
        self._initialize_inventory()
    
    def _initialize_inventory(self):
        """Initialize inventory with all blood types"""
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        for blood_type in blood_types:
            self.inventory[blood_type] = {
                'blood_type': blood_type,
                'units_available': 10,  # Start with 10 units each
                'last_updated': datetime.utcnow().isoformat(),
                'updated_by': 'system'
            }
    
    # User operations
    def create_user(self, user_data):
        """Create a new user"""
        try:
            user_id = user_data.get('user_id')
            email = user_data.get('email')
            
            # Check if email already exists
            if email in self.users_by_email:
                return False
            
            self.users[user_id] = user_data
            self.users_by_email[email] = user_id
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email):
        """Get user by email"""
        user_id = self.users_by_email.get(email)
        if user_id:
            return self.users.get(user_id)
        return None
    
    def update_user(self, user_id, update_data):
        """Update user data"""
        try:
            if user_id not in self.users:
                return False
            
            # Update user data
            for key, value in update_data.items():
                self.users[user_id][key] = value
            
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    # Blood request operations
    def create_request(self, request_data):
        """Create a new blood request"""
        try:
            request_id = request_data.get('request_id')
            self.requests[request_id] = request_data
            return True
        except Exception as e:
            print(f"Error creating request: {e}")
            return False
    
    def get_request_by_id(self, request_id):
        """Get request by ID"""
        return self.requests.get(request_id)
    
    def get_requests_by_blood_type(self, blood_type, status=None):
        """Get requests by blood type"""
        results = []
        for request in self.requests.values():
            if request.get('blood_type') == blood_type:
                if status is None or request.get('status') == status:
                    results.append(request)
        return results
    
    def get_all_requests(self, status=None):
        """Get all requests, optionally filtered by status"""
        if status is None:
            return list(self.requests.values())
        
        results = []
        for request in self.requests.values():
            if request.get('status') == status:
                results.append(request)
        return results
    
    def update_request(self, request_id, update_data):
        """Update request data"""
        try:
            if request_id not in self.requests:
                return False
            
            # Update request data
            for key, value in update_data.items():
                self.requests[request_id][key] = value
            
            return True
        except Exception as e:
            print(f"Error updating request: {e}")
            return False
    
    # Inventory operations
    def get_inventory(self, blood_type=None):
        """Get inventory for specific blood type or all"""
        if blood_type:
            return self.inventory.get(blood_type)
        else:
            return list(self.inventory.values())
    
    def update_inventory(self, blood_type, units_available, updated_by):
        """Update inventory for a blood type"""
        try:
            self.inventory[blood_type] = {
                'blood_type': blood_type,
                'units_available': units_available,
                'last_updated': datetime.utcnow().isoformat(),
                'updated_by': updated_by
            }
            return True
        except Exception as e:
            print(f"Error updating inventory: {e}")
            return False
    
    def get_low_stock_items(self, threshold=5):
        """Get blood types with low stock"""
        results = []
        for item in self.inventory.values():
            if item.get('units_available', 0) < threshold:
                results.append(item)
        return results
