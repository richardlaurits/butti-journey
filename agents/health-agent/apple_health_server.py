#!/usr/bin/env python3
"""
Apple Health API Server
Receives health data from Health Auto Export app
Stores locally and makes available for Health Agent analysis
"""

import json
import os
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration
DATA_DIR = Path('/home/richard-laurits/.openclaw/workspace/agents/health-agent/data/apple-health')
API_KEY = "RICHARD_API_KEY_2026"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

def verify_auth(request):
    """Verify API key from Authorization header"""
    auth_header = request.headers.get('Authorization', '')
    expected = f'Bearer {API_KEY}'
    return auth_header == expected

def save_health_data(data, timestamp):
    """Save incoming health data to file"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"apple-health-{date_str}.json"
    filepath = DATA_DIR / filename
    
    entry = {
        'received_at': datetime.now().isoformat(),
        'timestamp': timestamp,
        'data': data
    }
    
    # Append to daily file
    if filepath.exists():
        with open(filepath, 'r') as f:
            existing = json.load(f)
    else:
        existing = []
    
    existing.append(entry)
    
    with open(filepath, 'w') as f:
        json.dump(existing, f, indent=2)
    
    return filepath

@app.route('/api/health/apple', methods=['POST'])
def receive_apple_health():
    """Endpoint for Apple Health data from Health Auto Export app"""
    
    # Verify authentication
    if not verify_auth(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Parse incoming JSON
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        timestamp = data.get('timestamp', datetime.now().isoformat())
        health_data = data.get('data', data)  # Handle both formats
        
        # Save to file
        filepath = save_health_data(health_data, timestamp)
        
        # Log receipt
        print(f"✅ Received Apple Health data at {datetime.now()}")
        print(f"   Saved to: {filepath}")
        print(f"   Data points: {len(health_data) if isinstance(health_data, list) else 'N/A'}")
        
        return jsonify({
            'status': 'success',
            'message': 'Health data received',
            'saved_to': str(filepath)
        }), 200
        
    except Exception as e:
        print(f"❌ Error processing health data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health/status', methods=['GET'])
def health_status():
    """Check server status"""
    return jsonify({
        'status': 'online',
        'service': 'Apple Health API',
        'timestamp': datetime.now().isoformat(),
        'data_dir': str(DATA_DIR),
        'files_stored': len(list(DATA_DIR.glob('*.json')))
    }), 200

@app.route('/api/health/latest', methods=['GET'])
def get_latest_data():
    """Get latest health data (for Health Agent)"""
    
    if not verify_auth(request):
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Get most recent file
    files = sorted(DATA_DIR.glob('*.json'), reverse=True)
    
    if not files:
        return jsonify({'error': 'No data yet'}), 404
    
    with open(files[0], 'r') as f:
        data = json.load(f)
    
    return jsonify({
        'date': files[0].stem,
        'entries': len(data),
        'latest': data[-1] if data else None
    }), 200

if __name__ == '__main__':
    print("🩺 Apple Health API Server starting...")
    print(f"📁 Data directory: {DATA_DIR}")
    print(f"🔑 API endpoint: /api/health/apple")
    print(f"🌐 Status check: /api/health/status")
    print()
    print("⚠️  Use your server's local IP: http://YOUR_IP:8080")
    print()
    
    # Run on all interfaces, port 8080
    app.run(host='0.0.0.0', port=8080, debug=False)
