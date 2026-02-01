from flask import Blueprint, request, jsonify, current_app
from middleware import token_required, role_required
from datetime import datetime
import uuid

requests_bp = Blueprint('requests', __name__, url_prefix='/api/requests')

@requests_bp.route('', methods=['POST'])
@token_required
@role_required(['hospital', 'manager'])
def create_request():
    """Create a new blood request"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['blood_type', 'quantity', 'urgency']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate blood type
    valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    if data['blood_type'] not in valid_blood_types:
        return jsonify({'error': 'Invalid blood type'}), 400
    
    # Validate urgency
    if data['urgency'] not in ['normal', 'high']:
        return jsonify({'error': 'Urgency must be normal or high'}), 400
    
    # Create request
    db_service = current_app.db_service
    request_id = str(uuid.uuid4())
    
    request_data = {
        'request_id': request_id,
        'blood_type': data['blood_type'],
        'quantity': int(data['quantity']),
        'urgency': data['urgency'],
        'status': 'open',
        'created_by': request.user['user_id'],
        'timestamp': datetime.utcnow().isoformat(),
        'hospital_name': data.get('hospital_name', ''),
        'location': data.get('location', ''),
        'notes': data.get('notes', '')
    }
    
    success = db_service.create_request(request_data)
    
    if not success:
        return jsonify({'error': 'Failed to create request'}), 500
    
    return jsonify({
        'message': 'Request created successfully',
        'request_id': request_id
    }), 201


@requests_bp.route('', methods=['GET'])
@token_required
def get_requests():
    """Get blood requests with optional filters"""
    db_service = current_app.db_service
    
    # Get query parameters
    status = request.args.get('status')
    blood_type = request.args.get('blood_type')
    
    # Get requests
    if blood_type:
        requests = db_service.get_requests_by_blood_type(blood_type, status)
    else:
        requests = db_service.get_all_requests(status)
    
    # Sort by timestamp (newest first)
    requests.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return jsonify({'requests': requests}), 200


@requests_bp.route('/<request_id>', methods=['GET'])
@token_required
def get_request(request_id):
    """Get a specific blood request"""
    db_service = current_app.db_service
    blood_request = db_service.get_request_by_id(request_id)
    
    if not blood_request:
        return jsonify({'error': 'Request not found'}), 404
    
    return jsonify(blood_request), 200


@requests_bp.route('/<request_id>', methods=['PUT'])
@token_required
@role_required(['hospital', 'manager'])
def update_request(request_id):
    """Update a blood request"""
    data = request.get_json()
    db_service = current_app.db_service
    
    # Check if request exists
    existing_request = db_service.get_request_by_id(request_id)
    if not existing_request:
        return jsonify({'error': 'Request not found'}), 404
    
    # Validate status if provided
    if 'status' in data and data['status'] not in ['open', 'fulfilled', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
    
    # Update request
    update_data = {}
    allowed_fields = ['status', 'notes']
    
    for field in allowed_fields:
        if field in data:
            update_data[field] = data[field]
    
    if not update_data:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    success = db_service.update_request(request_id, update_data)
    
    if not success:
        return jsonify({'error': 'Failed to update request'}), 500
    
    return jsonify({'message': 'Request updated successfully'}), 200


@requests_bp.route('/<request_id>', methods=['DELETE'])
@token_required
@role_required(['hospital', 'manager'])
def delete_request(request_id):
    """Cancel a blood request (soft delete by updating status)"""
    db_service = current_app.db_service
    
    # Check if request exists
    existing_request = db_service.get_request_by_id(request_id)
    if not existing_request:
        return jsonify({'error': 'Request not found'}), 404
    
    # Update status to cancelled
    success = db_service.update_request(request_id, {'status': 'cancelled'})
    
    if not success:
        return jsonify({'error': 'Failed to cancel request'}), 500
    
    return jsonify({'message': 'Request cancelled successfully'}), 200
