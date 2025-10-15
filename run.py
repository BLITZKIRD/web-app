#!/usr/bin/env python3
"""
Startup script for the Flask Password Generator application.
This script provides a simple way to run the application with proper configuration.
"""

import os
from app import app

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print("🔐 Flask Password Generator")
    print("=" * 40)
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print("=" * 40)
    print(f"Open your browser and go to: http://{host}:{port}")
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Run the Flask application
    app.run(host=host, port=port, debug=debug)