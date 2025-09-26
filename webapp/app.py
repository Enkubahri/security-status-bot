import os
import hashlib
import hmac
import json
import urllib.parse
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SecurityDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize database
db = SecurityDatabase(os.getenv('DATABASE_PATH', '../security_reports.db'))

# Bot token for authentication
BOT_TOKEN = os.getenv('BOT_TOKEN')

def validate_telegram_data(init_data):
    """
    Validate Telegram Mini App init data
    """
    if not init_data or not BOT_TOKEN:
        return False
    
    try:
        # Parse the init data
        parsed_data = urllib.parse.parse_qsl(init_data)
        data_dict = dict(parsed_data)
        
        # Extract hash
        received_hash = data_dict.get('hash', '')
        if not received_hash:
            return False
        
        # Remove hash from data
        del data_dict['hash']
        
        # Create data check string
        data_check_arr = []
        for key, value in sorted(data_dict.items()):
            data_check_arr.append(f"{key}={value}")
        data_check_string = '\n'.join(data_check_arr)
        
        # Create secret key
        secret_key = hmac.new(
            "WebAppData".encode('utf-8'), 
            BOT_TOKEN.encode('utf-8'), 
            hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            secret_key, 
            data_check_string.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()
        
        return calculated_hash == received_hash
    except Exception as e:
        print(f"Telegram data validation error: {e}")
        return False

def extract_user_from_init_data(init_data):
    """
    Extract user information from Telegram init data
    """
    try:
        parsed_data = urllib.parse.parse_qsl(init_data)
        data_dict = dict(parsed_data)
        
        if 'user' in data_dict:
            user_data = json.loads(data_dict['user'])
            return user_data
        return None
    except Exception as e:
        print(f"Error extracting user data: {e}")
        return None

@app.route('/')
def index():
    """
    Serve the Mini App main page
    """
    return render_template('index.html')

@app.route('/api/user/permissions', methods=['POST'])
def check_user_permissions():
    """
    Check if user is admin or focal person
    """
    try:
        init_data = request.headers.get('X-Telegram-Init-Data', '')
        
        # For development, allow requests without validation
        # In production, uncomment the validation below
        # if not validate_telegram_data(init_data):
        #     return jsonify({'error': 'Invalid request'}), 401
        
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        is_admin = db.is_admin(user_id)
        is_focal_person = db.is_focal_person(user_id)
        
        return jsonify({
            'is_admin': is_admin,
            'is_focal_person': is_focal_person
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """
    Get all security reports
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        location = request.args.get('location')
        
        if location:
            reports_data = db.get_reports_by_location(location, limit)
        else:
            reports_data = db.get_latest_reports(limit)
        
        reports = []
        for report in reports_data:
            reports.append({
                'location': report[0],
                'status': report[1],
                'recommended_action': report[2],
                'reporter_name': report[3],
                'timestamp': report[4]
            })
        
        return jsonify(reports)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports', methods=['POST'])
def create_report():
    """
    Create a new security report
    """
    try:
        init_data = request.headers.get('X-Telegram-Init-Data', '')
        
        # For development, allow requests without validation
        # In production, uncomment the validation below
        # if not validate_telegram_data(init_data):
        #     return jsonify({'error': 'Invalid request'}), 401
        
        data = request.json
        user_id = data.get('user_id')
        user_name = data.get('user_name', f'User{user_id}')
        location = data.get('location', '').strip()
        status = data.get('status', '').strip()
        recommended_action = data.get('recommended_action', '').strip()
        
        # Validate required fields
        if not all([user_id, location, status, recommended_action]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Validate user permissions
        if not (db.is_admin(user_id) or db.is_focal_person(user_id)):
            return jsonify({'error': 'Unauthorized to submit reports'}), 403
        
        # Validate location format (letters and spaces only)
        import re
        if not re.match(r'^[a-zA-Z\s]+$', location):
            return jsonify({'error': 'Location must contain only letters and spaces'}), 400
        
        # Add report to database
        success = db.add_security_report(
            location=location,
            status=status,
            recommended_action=recommended_action,
            reporter_id=user_id,
            reporter_name=user_name
        )
        
        if success:
            return jsonify({'message': 'Report created successfully'}), 201
        else:
            return jsonify({'error': 'Failed to create report'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/focal-people', methods=['GET'])
def get_focal_people():
    """
    Get all focal people (admin only)
    """
    try:
        init_data = request.headers.get('X-Telegram-Init-Data', '')
        
        # For development, allow requests without validation
        # In production, uncomment the validation below
        # if not validate_telegram_data(init_data):
        #     return jsonify({'error': 'Invalid request'}), 401
        
        # Extract user from init data or use a default for development
        user_data = extract_user_from_init_data(init_data)
        user_id = user_data.get('id') if user_data else 994550828  # Your admin ID for development
        
        # Check admin permissions
        if not db.is_admin(user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        focal_people_data = db.get_all_focal_people()
        focal_people = []
        
        for fp in focal_people_data:
            focal_people.append({
                'user_id': fp[0],
                'name': fp[1],
                'added_date': fp[2]
            })
        
        return jsonify(focal_people)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/focal-people', methods=['POST'])
def add_focal_person():
    """
    Add a new focal person (admin only)
    """
    try:
        init_data = request.headers.get('X-Telegram-Init-Data', '')
        
        # For development, allow requests without validation
        # In production, uncomment the validation below
        # if not validate_telegram_data(init_data):
        #     return jsonify({'error': 'Invalid request'}), 401
        
        # Extract user from init data or use a default for development
        user_data = extract_user_from_init_data(init_data)
        admin_user_id = user_data.get('id') if user_data else 994550828  # Your admin ID for development
        
        # Check admin permissions
        if not db.is_admin(admin_user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.json
        focal_user_id = data.get('user_id')
        name = data.get('name', '').strip()
        
        # Validate required fields
        if not all([focal_user_id, name]):
            return jsonify({'error': 'User ID and name are required'}), 400
        
        # Validate name format (letters and spaces only)
        import re
        if not re.match(r'^[a-zA-Z\s]+$', name):
            return jsonify({'error': 'Name must contain only letters and spaces'}), 400
        
        # Add focal person to database
        success = db.add_focal_person(
            telegram_user_id=focal_user_id,
            name=name,
            added_by=admin_user_id
        )
        
        if success:
            return jsonify({'message': 'Focal person added successfully'}), 201
        else:
            return jsonify({'error': 'Failed to add focal person or already exists'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/focal-people/<int:focal_user_id>', methods=['DELETE'])
def remove_focal_person(focal_user_id):
    """
    Remove a focal person (admin only)
    """
    try:
        init_data = request.headers.get('X-Telegram-Init-Data', '')
        
        # For development, allow requests without validation
        # In production, uncomment the validation below
        # if not validate_telegram_data(init_data):
        #     return jsonify({'error': 'Invalid request'}), 401
        
        # Extract user from init data or use a default for development
        user_data = extract_user_from_init_data(init_data)
        admin_user_id = user_data.get('id') if user_data else 994550828  # Your admin ID for development
        
        # Check admin permissions
        if not db.is_admin(admin_user_id):
            return jsonify({'error': 'Admin access required'}), 403
        
        # Remove focal person from database
        success = db.remove_focal_person(focal_user_id)
        
        if success:
            return jsonify({'message': 'Focal person removed successfully'}), 200
        else:
            return jsonify({'error': 'Failed to remove focal person or not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Production configuration
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Initialize database on startup
    db.init_database()
    
    app.run(host=host, port=port, debug=debug)
