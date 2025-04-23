from flask import Blueprint, render_template, jsonify, request
from app.services.data_service import get_stored_data, refresh_all_data, get_available_data_types
from app.services.yahoo_api_service import check_auth_status

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Render the dashboard page."""
    auth_status = check_auth_status()
    data_types = get_available_data_types()
    return render_template('dashboard.html', auth_status=auth_status, data_types=data_types)

@main.route('/settings')
def settings():
    """Render the settings page."""
    auth_status = check_auth_status()
    return render_template('settings.html', auth_status=auth_status)

@main.route('/api/data/<data_type>')
def get_data(data_type):
    """API endpoint to get stored data."""
    data = get_stored_data(data_type)
    return jsonify(data)

@main.route('/api/refresh', methods=['POST'])
def refresh_data():
    """API endpoint to trigger data refresh."""
    data_type = request.json.get('data_type', 'all')
    result = refresh_all_data() if data_type == 'all' else refresh_all_data(data_type)
    return jsonify({"success": result})

@main.route('/api/status')
def api_status():
    """API endpoint to check status."""
    auth_status = check_auth_status()
    data_types = get_available_data_types()
    return jsonify({
        "auth_status": auth_status,
        "data_types": data_types
    })