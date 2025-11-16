#!/usr/bin/env python3
"""
NexVuln Web Application
Flask backend for the vulnerability scanner web interface.
"""

import warnings
warnings.filterwarnings('ignore', message='.*urllib3.*OpenSSL.*', category=UserWarning)
warnings.filterwarnings('ignore', message='.*NotOpenSSLWarning.*')

# Flask imports - installed via pip install flask flask-cors
try:
    from flask import Flask, render_template, jsonify, request, send_file
    from flask_cors import CORS
except ImportError as e:
    raise ImportError(
        "Flask dependencies not installed. Run: pip3 install flask flask-cors"
    ) from e
import json
import os
import threading
from datetime import datetime
from typing import Dict, Any

from nexvuln.port_scanner import PortScanner
from nexvuln.header_scanner import HeaderScanner
from nexvuln.ssl_scanner import SSLScanner
from nexvuln.directory_scanner import DirectoryScanner
from nexvuln.utils import validate_target, normalize_url, get_protocol

import os

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')

app = Flask(__name__, 
            static_folder=os.path.join(WEB_DIR, 'static'),
            template_folder=os.path.join(WEB_DIR, 'templates'))
CORS(app)

# Store scan results in memory (in production, use Redis or database)
scan_results = {}
scan_status = {}


@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/api/scan/headers', methods=['POST'])
def scan_headers():
    """Scan HTTP security headers."""
    try:
        data = request.json
        target = data.get('target', '').strip()
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Validate target
        is_valid, host, port = validate_target(target)
        if not is_valid:
            return jsonify({'error': f'Invalid or unreachable target: {target}'}), 400
        
        # Run scan
        scanner = HeaderScanner()
        results = scanner.scan(normalize_url(target))
        
        return jsonify({
            'success': True,
            'target': target,
            'results': scanner.get_results_dict(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan/ssl', methods=['POST'])
def scan_ssl():
    """Scan SSL/TLS configuration."""
    try:
        data = request.json
        target = data.get('target', '').strip()
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Validate target
        is_valid, host, port = validate_target(target)
        if not is_valid:
            return jsonify({'error': f'Invalid or unreachable target: {target}'}), 400
        
        # Run scan
        scanner = SSLScanner()
        results = scanner.scan(normalize_url(target))
        
        return jsonify({
            'success': True,
            'target': target,
            'results': scanner.get_results_dict(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan/ports', methods=['POST'])
def scan_ports():
    """Scan open ports."""
    try:
        data = request.json
        target = data.get('target', '').strip()
        scan_type = data.get('scan_type', 'fast')  # 'fast' or 'full'
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Validate target
        is_valid, host, port = validate_target(target)
        if not is_valid:
            return jsonify({'error': f'Invalid or unreachable target: {target}'}), 400
        
        # Run scan
        scanner = PortScanner()
        results = scanner.scan(host, scan_type=scan_type)
        
        return jsonify({
            'success': True,
            'target': target,
            'results': scanner.get_results_dict(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan/directories', methods=['POST'])
def scan_directories():
    """Scan for directories and files."""
    try:
        data = request.json
        target = data.get('target', '').strip()
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Validate target
        is_valid, host, port = validate_target(target)
        if not is_valid:
            return jsonify({'error': f'Invalid or unreachable target: {target}'}), 400
        
        # Run scan
        scanner = DirectoryScanner()
        results = scanner.scan(normalize_url(target))
        
        return jsonify({
            'success': True,
            'target': target,
            'results': scanner.get_results_dict(),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/scan/full', methods=['POST'])
def scan_full():
    """Run full comprehensive scan."""
    try:
        data = request.json
        target = data.get('target', '').strip()
        scan_type = data.get('scan_type', 'fast')
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Validate target
        is_valid, host, port = validate_target(target)
        if not is_valid:
            return jsonify({'error': f'Invalid or unreachable target: {target}'}), 400
        
        results = {
            'target': target,
            'scan_date': datetime.now().isoformat(),
            'port_scan': [],
            'header_scan': [],
            'ssl_scan': {},
            'directory_scan': []
        }
        
        # Run all scans
        try:
            # Port scan
            port_scanner = PortScanner()
            port_results = port_scanner.scan(host, scan_type=scan_type)
            results['port_scan'] = port_scanner.get_results_dict()
        except Exception as e:
            results['port_scan'] = {'error': str(e)}
        
        try:
            # Header scan
            header_scanner = HeaderScanner()
            header_scanner.scan(normalize_url(target))
            results['header_scan'] = header_scanner.get_results_dict()
        except Exception as e:
            results['header_scan'] = {'error': str(e)}
        
        try:
            # SSL scan (only for HTTPS)
            if get_protocol(target) == 'https' or port == 443:
                ssl_scanner = SSLScanner()
                ssl_scanner.scan(normalize_url(target))
                results['ssl_scan'] = ssl_scanner.get_results_dict()
        except Exception as e:
            results['ssl_scan'] = {'error': str(e)}
        
        try:
            # Directory scan
            dir_scanner = DirectoryScanner()
            dir_scanner.scan(normalize_url(target))
            results['directory_scan'] = dir_scanner.get_results_dict()
        except Exception as e:
            results['directory_scan'] = {'error': str(e)}
        
        return jsonify({
            'success': True,
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/validate', methods=['POST'])
def validate_target_endpoint():
    """Validate if target is reachable."""
    try:
        data = request.json
        target = data.get('target', '').strip()
        
        if not target:
            return jsonify({'valid': False, 'error': 'Target is required'}), 400
        
        is_valid, host, port = validate_target(target)
        
        return jsonify({
            'valid': is_valid,
            'host': host,
            'port': port,
            'error': None if is_valid else f'Invalid or unreachable target: {target}'
        })
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500


@app.route('/api/download', methods=['POST'])
def download_report():
    """Download scan results as JSON."""
    try:
        data = request.json
        results = data.get('results', {})
        
        # Create temporary file
        filename = f"nexvuln_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join('/tmp', filename)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import sys
    import socket
    
    def find_free_port(start_port=5001, max_attempts=10):
        """Find a free port starting from start_port."""
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        raise RuntimeError(f"Could not find a free port in range {start_port}-{start_port + max_attempts}")
    
    # Use port 5001 by default (5000 is often used by macOS AirPlay)
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            port = find_free_port()
    else:
        port = find_free_port()
    
    print("=" * 60)
    print("🔒 NexVuln Web Application")
    print("=" * 60)
    print("🌐 Starting web server...")
    print(f"📡 Access the interface at: http://localhost:{port}")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=port)

