from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from api import api_bp

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)

app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    import sys
    try:
        # Use '0.0.0.0' to allow connections from any network interface
        # This enables remote access on your local network
        print("\n✓ Backend server is accessible at:")
        print(f"  - Local: http://localhost:5001")
        print(f"  - Network: http://192.168.86.41:5001 (or your machine's IP)")
        print("\nStarting server...\n")
        app.run(debug=True, port=5001, host='0.0.0.0')
    except OSError as e:
        if 'Address already in use' in str(e) or e.errno == 48:
            print(f"\n❌ ERROR: Port 5001 is already in use!")
            print(f"   Please stop the other process using port 5001, or change the port in app.py")
            print(f"   To find what's using the port: lsof -ti:5001")
            sys.exit(1)
        else:
            raise
