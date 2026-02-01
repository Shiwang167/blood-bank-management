from flask import Blueprint, request, jsonify, current_app
from middleware import token_required, role_required

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')

@inventory_bp.route('', methods=['GET'])
@token_required
def get_inventory():
    """Get blood inventory"""
    db_service = current_app.db_service
    config = current_app.config
    
    # Get all inventory
    inventory = db_service.get_inventory()
    
    # Add low stock indicators
    for item in inventory:
        units = item.get('units_available', 0)
        if units < config['CRITICAL_STOCK_THRESHOLD']:
            item['stock_status'] = 'critical'
        elif units < config['LOW_STOCK_THRESHOLD']:
            item['stock_status'] = 'low'
        else:
            item['stock_status'] = 'good'
        
        item['is_low_stock'] = units < config['LOW_STOCK_THRESHOLD']
    
    # Sort by blood type
    blood_type_order = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    inventory.sort(key=lambda x: blood_type_order.index(x['blood_type']) if x['blood_type'] in blood_type_order else 999)
    
    return jsonify({'inventory': inventory}), 200


@inventory_bp.route('/<blood_type>', methods=['GET'])
@token_required
def get_inventory_by_type(blood_type):
    """Get inventory for specific blood type"""
    db_service = current_app.db_service
    config = current_app.config
    
    item = db_service.get_inventory(blood_type)
    
    if not item:
        return jsonify({'error': 'Blood type not found'}), 404
    
    # Add stock status
    units = item.get('units_available', 0)
    if units < config['CRITICAL_STOCK_THRESHOLD']:
        item['stock_status'] = 'critical'
    elif units < config['LOW_STOCK_THRESHOLD']:
        item['stock_status'] = 'low'
    else:
        item['stock_status'] = 'good'
    
    item['is_low_stock'] = units < config['LOW_STOCK_THRESHOLD']
    
    return jsonify(item), 200


@inventory_bp.route('', methods=['PUT'])
@token_required
@role_required(['manager'])
def update_inventory():
    """Update blood inventory (manager only)"""
    data = request.get_json()
    
    # Validate required fields
    if not all(field in data for field in ['blood_type', 'units_available']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Validate blood type
    valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    if data['blood_type'] not in valid_blood_types:
        return jsonify({'error': 'Invalid blood type'}), 400
    
    # Validate units
    try:
        units = int(data['units_available'])
        if units < 0:
            return jsonify({'error': 'Units cannot be negative'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid units value'}), 400
    
    # Update inventory
    db_service = current_app.db_service
    success = db_service.update_inventory(
        data['blood_type'],
        units,
        request.user['user_id']
    )
    
    if not success:
        return jsonify({'error': 'Failed to update inventory'}), 500
    
    return jsonify({'message': 'Inventory updated successfully'}), 200


@inventory_bp.route('/low-stock', methods=['GET'])
@token_required
@role_required(['manager'])
def get_low_stock():
    """Get low stock alerts (manager only)"""
    db_service = current_app.db_service
    config = current_app.config
    
    threshold = request.args.get('threshold', config['LOW_STOCK_THRESHOLD'], type=int)
    low_stock_items = db_service.get_low_stock_items(threshold)
    
    # Add severity
    for item in low_stock_items:
        units = item.get('units_available', 0)
        if units < config['CRITICAL_STOCK_THRESHOLD']:
            item['severity'] = 'critical'
        else:
            item['severity'] = 'low'
    
    return jsonify({'low_stock_items': low_stock_items}), 200
