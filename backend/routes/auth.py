from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import uuid

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'password', 'role']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate role
    valid_roles = ['donor', 'hospital', 'manager']
    if data['role'] not in valid_roles:
        return jsonify({'error': 'Invalid role'}), 400
    
    # Validate blood type for donors
    if data['role'] == 'donor' and 'blood_type' not in data:
        return jsonify({'error': 'Blood type required for donors'}), 400
    
    # Check if user already exists
    db_service = current_app.db_service
    existing_user = db_service.get_user_by_email(data['email'])
    
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 409
    
    # Hash password
    auth_service = current_app.auth_service
    password_hash = auth_service.hash_password(data['password'])
    
    # Create user
    user_id = str(uuid.uuid4())
    user_data = {
        'user_id': user_id,
        'name': data['name'],
        'email': data['email'],
        'password_hash': password_hash,
        'role': data['role'],
        'phone': data.get('phone', ''),
        'created_at': datetime.utcnow().isoformat()
    }
    
    # Add donor-specific fields
    if data['role'] == 'donor':
        user_data['blood_type'] = data['blood_type']
        user_data['last_donation'] = data.get('last_donation', None)
    
    # Add hospital-specific fields
    if data['role'] == 'hospital':
        user_data['hospital_name'] = data.get('hospital_name', '')
        user_data['location'] = data.get('location', '')
    
    success = db_service.create_user(user_data)
    
    if not success:
        return jsonify({'error': 'Failed to create user'}), 500
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user_id
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    # Validate required fields
    if not all(field in data for field in ['email', 'password']):
        return jsonify({'error': 'Email and password required'}), 400
    
    # Get user
    db_service = current_app.db_service
    user = db_service.get_user_by_email(data['email'])
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Verify password
    auth_service = current_app.auth_service
    if not auth_service.verify_password(data['password'], user['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate token
    token = auth_service.generate_token(
        user['user_id'],
        user['email'],
        user['role']
    )
    
    # Prepare user data (exclude password hash)
    user_data = {
        'user_id': user['user_id'],
        'name': user['name'],
        'email': user['email'],
        'role': user['role']
    }
    
    if user['role'] == 'donor':
        user_data['blood_type'] = user.get('blood_type')
        user_data['last_donation'] = user.get('last_donation')
    
    if user['role'] == 'hospital':
        user_data['hospital_name'] = user.get('hospital_name')
        user_data['location'] = user.get('location')
    
    return jsonify({
        'token': token,
        'user': user_data
    }), 200
