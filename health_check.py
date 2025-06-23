from flask import Blueprint, jsonify

health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring and Docker health checks"""
    return jsonify({
        'status': 'healthy',
        'message': 'Hospitell application is running'
    })