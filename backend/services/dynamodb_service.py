import boto3
from botocore.exceptions import ClientError
from config import Config

class DynamoDBService:
    """Service for DynamoDB operations"""
    
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize DynamoDB client
        if config.DYNAMODB_ENDPOINT:
            # Local development
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name=config.AWS_REGION,
                endpoint_url=config.DYNAMODB_ENDPOINT
            )
        else:
            # Production (uses IAM role)
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name=config.AWS_REGION
            )
        
        # Table references
        self.users_table = self.dynamodb.Table(config.USERS_TABLE)
        self.requests_table = self.dynamodb.Table(config.REQUESTS_TABLE)
        self.inventory_table = self.dynamodb.Table(config.INVENTORY_TABLE)
    
    # User operations
    def create_user(self, user_data):
        """Create a new user"""
        try:
            self.users_table.put_item(Item=user_data)
            return True
        except ClientError as e:
            print(f"Error creating user: {e}")
            return False
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        try:
            response = self.users_table.get_item(Key={'user_id': user_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email):
        """Get user by email using GSI"""
        try:
            response = self.users_table.query(
                IndexName='EmailIndex',
                KeyConditionExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )
            items = response.get('Items', [])
            return items[0] if items else None
        except ClientError as e:
            print(f"Error querying user by email: {e}")
            return None
    
    def update_user(self, user_id, update_data):
        """Update user data"""
        try:
            update_expression = "SET " + ", ".join([f"{k} = :{k}" for k in update_data.keys()])
            expression_values = {f":{k}": v for k, v in update_data.items()}
            
            self.users_table.update_item(
                Key={'user_id': user_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
            return True
        except ClientError as e:
            print(f"Error updating user: {e}")
            return False
    
    # Blood request operations
    def create_request(self, request_data):
        """Create a new blood request"""
        try:
            self.requests_table.put_item(Item=request_data)
            return True
        except ClientError as e:
            print(f"Error creating request: {e}")
            return False
    
    def get_request_by_id(self, request_id):
        """Get request by ID"""
        try:
            response = self.requests_table.get_item(Key={'request_id': request_id})
            return response.get('Item')
        except ClientError as e:
            print(f"Error getting request: {e}")
            return None
    
    def get_requests_by_blood_type(self, blood_type, status=None):
        """Get requests by blood type using GSI"""
        try:
            if status:
                response = self.requests_table.query(
                    IndexName='BloodTypeIndex',
                    KeyConditionExpression='blood_type = :blood_type',
                    FilterExpression='#status = :status',
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={
                        ':blood_type': blood_type,
                        ':status': status
                    }
                )
            else:
                response = self.requests_table.query(
                    IndexName='BloodTypeIndex',
                    KeyConditionExpression='blood_type = :blood_type',
                    ExpressionAttributeValues={':blood_type': blood_type}
                )
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error querying requests: {e}")
            return []
    
    def get_all_requests(self, status=None):
        """Get all requests, optionally filtered by status"""
        try:
            if status:
                response = self.requests_table.scan(
                    FilterExpression='#status = :status',
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={':status': status}
                )
            else:
                response = self.requests_table.scan()
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error scanning requests: {e}")
            return []
    
    def update_request(self, request_id, update_data):
        """Update request data"""
        try:
            update_expression = "SET " + ", ".join([f"{k} = :{k}" for k in update_data.keys()])
            expression_values = {f":{k}": v for k, v in update_data.items()}
            
            self.requests_table.update_item(
                Key={'request_id': request_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
            return True
        except ClientError as e:
            print(f"Error updating request: {e}")
            return False
    
    # Inventory operations
    def get_inventory(self, blood_type=None):
        """Get inventory for specific blood type or all"""
        try:
            if blood_type:
                response = self.inventory_table.get_item(Key={'blood_type': blood_type})
                return response.get('Item')
            else:
                response = self.inventory_table.scan()
                return response.get('Items', [])
        except ClientError as e:
            print(f"Error getting inventory: {e}")
            return None if blood_type else []
    
    def update_inventory(self, blood_type, units_available, updated_by):
        """Update inventory for a blood type"""
        try:
            from datetime import datetime
            self.inventory_table.put_item(Item={
                'blood_type': blood_type,
                'units_available': units_available,
                'last_updated': datetime.utcnow().isoformat(),
                'updated_by': updated_by
            })
            return True
        except ClientError as e:
            print(f"Error updating inventory: {e}")
            return False
    
    def get_low_stock_items(self, threshold=5):
        """Get blood types with low stock"""
        try:
            response = self.inventory_table.scan(
                FilterExpression='units_available < :threshold',
                ExpressionAttributeValues={':threshold': threshold}
            )
            return response.get('Items', [])
        except ClientError as e:
            print(f"Error getting low stock items: {e}")
            return []
