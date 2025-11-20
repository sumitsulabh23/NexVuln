"""
Utility functions for NexVuln scanner.
"""

import socket
import re
from urllib.parse import urlparse
from typing import Tuple, Optional


def validate_target(target: str) -> Tuple[bool, Optional[str], Optional[int]]:
    """
    Validate and parse target URL or IP address.
    
    Args:
        target: Target URL or IP address
        
    Returns:
        Tuple of (is_valid, host, port)
    """
    # Remove protocol if present
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    try:
        parsed = urlparse(target)
        host = parsed.hostname or parsed.path.split('/')[0]
        port = parsed.port
        
        if not host:
            return False, None, None
        
        # Validate host is reachable
        try:
            socket.gethostbyname(host)
        except socket.gaierror:
            return False, None, None
        
        # Default ports
        if not port:
            if parsed.scheme == 'https' or target.startswith('https://'):
                port = 443
            else:
                port = 80
        
        return True, host, port
    except Exception:
        return False, None, None


def get_protocol(target: str) -> str:
    """
    Detect protocol (HTTP/HTTPS) from target.
    
    Args:
        target: Target URL
        
    Returns:
        Protocol string ('http' or 'https')
    """
    target = target.strip().lower()
    if target.startswith('https://'):
        return 'https'
    elif target.startswith('http://'):
        return 'http'
    else:
        # Try HTTPS first, fallback to HTTP
        return 'https'


def normalize_url(target: str) -> str:
    """
    Normalize URL to include protocol.
    
    Args:
        target: Target URL or IP
        
    Returns:
        Normalized URL with protocol
    """
    target = target.strip()
    if not target.startswith(('http://', 'https://')):
        # Try HTTPS first
        return f'https://{target}'
    return target


def is_ip_address(host: str) -> bool:
    """
    Check if host is an IP address.
    
    Args:
        host: Host string
        
    Returns:
        True if IP address, False otherwise
    """
    ip_pattern = re.compile(
        r'^(\d{1,3}\.){3}\d{1,3}$'
    )
    return bool(ip_pattern.match(host))


def format_severity(severity: str) -> str:
    """
    Format severity level for display.
    
    Args:
        severity: Severity level (critical, high, medium, low, info)
        
    Returns:
        Formatted severity string
    """
    severity_map = {
        'critical': '🔴 CRITICAL',
        'high': '🟠 HIGH',
        'medium': '🟡 MEDIUM',
        'low': '🔵 LOW',
        'info': 'ℹ️  INFO'
    }
    return severity_map.get(severity.lower(), severity.upper())

