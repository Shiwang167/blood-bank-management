import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
DYNAMODB_ENDPOINT = os.getenv('DYNAMODB_ENDPOINT', None)

def create_dynamodb_tables():
    """Create DynamoDB tables for BloodBridge"""
    
    # Initialize DynamoDB client
    if DYNAMODB_ENDPOINT:
        dynamodb = boto3.client(
            'dynamodb',
            region_name=AWS_REGION,
            endpoint_url=DYNAMODB_ENDPOINT
        )
    else:
        dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
    
    tables = []
    
    # Table 1: Users
    users_table = {
        'TableName': 'BloodBridge_Users',
        'KeySchema': [
            {'AttributeName': 'user_id', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'email', 'AttributeType': 'S'}
        ],
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'EmailIndex',
                'KeySchema': [
                    {'AttributeName': 'email', 'KeyType': 'HASH'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    }
    tables.append(users_table)
    
    # Table 2: BloodRequests
    requests_table = {
        'TableName': 'BloodBridge_BloodRequests',
        'KeySchema': [
            {'AttributeName': 'request_id', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'request_id', 'AttributeType': 'S'},
            {'AttributeName': 'blood_type', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'S'}
        ],
        'GlobalSecondaryIndexes': [
            {
                'IndexName': 'BloodTypeIndex',
                'KeySchema': [
                    {'AttributeName': 'blood_type', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    }
    tables.append(requests_table)
    
    # Table 3: Inventory
    inventory_table = {
        'TableName': 'BloodBridge_Inventory',
        'KeySchema': [
            {'AttributeName': 'blood_type', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'blood_type', 'AttributeType': 'S'}
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    }
    tables.append(inventory_table)
    
    # Create tables
    for table_config in tables:
        try:
            print(f"Creating table: {table_config['TableName']}...")
            dynamodb.create_table(**table_config)
            print(f"✓ Table {table_config['TableName']} created successfully")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print(f"⚠ Table {table_config['TableName']} already exists")
            else:
                print(f"✗ Error creating table {table_config['TableName']}: {e}")
    
    print("\n✓ All tables processed")
    
    # Initialize inventory with default values
    print("\nInitializing inventory...")
    initialize_inventory(dynamodb)


def initialize_inventory(dynamodb):
    """Initialize inventory with default blood types"""
    blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    
    for blood_type in blood_types:
        try:
            if DYNAMODB_ENDPOINT:
                resource = boto3.resource(
                    'dynamodb',
                    region_name=AWS_REGION,
                    endpoint_url=DYNAMODB_ENDPOINT
                )
            else:
                resource = boto3.resource('dynamodb', region_name=AWS_REGION)
            
            table = resource.Table('BloodBridge_Inventory')
            
            from datetime import datetime
            table.put_item(Item={
                'blood_type': blood_type,
                'units_available': 10,  # Default 10 units
                'last_updated': datetime.utcnow().isoformat(),
                'updated_by': 'system'
            })
            print(f"✓ Initialized inventory for {blood_type}")
        except ClientError as e:
            print(f"✗ Error initializing {blood_type}: {e}")


if __name__ == '__main__':
    print("BloodBridge - DynamoDB Table Creation Script")
    print("=" * 50)
    create_dynamodb_tables()
    print("\n✓ Setup complete!")
