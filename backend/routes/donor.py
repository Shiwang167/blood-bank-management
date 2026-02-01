from flask import Blueprint, request, jsonify, current_app
from middleware import token_required, role_required
from datetime import datetime, timedelta

donor_bp = Blueprint('donor', __name__, url_prefix='/api/donor')

@donor_bp.route('/eligibility', methods=['GET'])
@token_required
@role_required(['donor'])
def check_eligibility():
    """Check donor eligibility based on last donation date"""
    db_service = current_app.db_service
    config = current_app.config
    
    # Get user data
    user = db_service.get_user_by_id(request.user['user_id'])
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    last_donation = user.get('last_donation')
    
    if not last_donation:
        # Never donated before
        return jsonify({
            'eligible': True,
            'last_donation': None,
            'next_eligible_date': None,
            'days_until_eligible': 0,
            'message': 'You are eligible to donate!'
        }), 200
    
    # Parse last donation date
    try:
        last_donation_date = datetime.fromisoformat(last_donation.replace('Z', '+00:00'))
    except:
        last_donation_date = datetime.fromisoformat(last_donation)
    
    # Calculate next eligible date
    interval_days = config['DONATION_INTERVAL_DAYS']
    next_eligible_date = last_donation_date + timedelta(days=interval_days)
    
    # Check if eligible
    now = datetime.utcnow()
    eligible = now >= next_eligible_date
    
    days_until_eligible = (next_eligible_date - now).days if not eligible else 0
    
    return jsonify({
        'eligible': eligible,
        'last_donation': last_donation,
        'next_eligible_date': next_eligible_date.isoformat(),
        'days_until_eligible': max(0, days_until_eligible),
        'message': 'You are eligible to donate!' if eligible else f'You can donate again in {days_until_eligible} days'
    }), 200


@donor_bp.route('/schedule', methods=['POST'])
@token_required
@role_required(['donor'])
def schedule_donation():
    """Schedule a donation for a blood request"""
    data = request.get_json()
    
    # Validate required fields
    if 'request_id' not in data:
        return jsonify({'error': 'Request ID required'}), 400
    
    db_service = current_app.db_service
    
    # Check if request exists
    blood_request = db_service.get_request_by_id(data['request_id'])
    if not blood_request:
        return jsonify({'error': 'Request not found'}), 404
    
    # Check if request is still open
    if blood_request.get('status') != 'open':
        return jsonify({'error': 'Request is no longer open'}), 400
    
    # Get user data
    user = db_service.get_user_by_id(request.user['user_id'])
    
    # Check blood type compatibility
    if user.get('blood_type') != blood_request.get('blood_type'):
        return jsonify({'error': 'Blood type mismatch'}), 400
    
    # In a real system, this would create a donation appointment
    # For now, we'll just return success
    
    return jsonify({
        'message': 'Donation scheduled successfully',
        'request_id': data['request_id'],
        'scheduled_date': data.get('scheduled_date', datetime.utcnow().isoformat())
    }), 200


@donor_bp.route('/matching-requests', methods=['GET'])
@token_required
@role_required(['donor'])
def get_matching_requests():
    """Get blood requests matching donor's blood type"""
    db_service = current_app.db_service
    
    # Get user data
    user = db_service.get_user_by_id(request.user['user_id'])
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    blood_type = user.get('blood_type')
    
    if not blood_type:
        return jsonify({'error': 'Blood type not set'}), 400
    
    # Get matching requests
    requests = db_service.get_requests_by_blood_type(blood_type, status='open')
    
    # Sort by urgency and timestamp
    requests.sort(key=lambda x: (
        0 if x.get('urgency') == 'high' else 1,
        x.get('timestamp', '')
    ), reverse=True)
    
    return jsonify({
        'blood_type': blood_type,
        'matching_requests': requests,
        'count': len(requests)
    }), 200


@donor_bp.route('/update-last-donation', methods=['PUT'])
@token_required
@role_required(['donor', 'manager'])
def update_last_donation():
    """Update last donation date"""
    data = request.get_json()
    
    # Get user ID (can be self or manager updating for donor)
    user_id = data.get('user_id', request.user['user_id'])
    
    # Only managers can update for other users
    if user_id != request.user['user_id'] and request.user['role'] != 'manager':
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    # Validate date
    if 'last_donation' not in data:
        return jsonify({'error': 'Last donation date required'}), 400
    
    db_service = current_app.db_service
    
    # Update user
    success = db_service.update_user(user_id, {
        'last_donation': data['last_donation']
    })
    
    if not success:
        return jsonify({'error': 'Failed to update donation date'}), 500
    
    return jsonify({'message': 'Last donation date updated successfully'}), 200
