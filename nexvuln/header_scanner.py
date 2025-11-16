"""
HTTP Security Header Scanner Module for NexVuln.
Checks for missing security headers.
"""

import requests
import urllib3
import warnings
from typing import Dict, List, Optional
from urllib.parse import urlparse
from rich.console import Console
from rich.table import Table
from rich import box

# Suppress SSL warnings (intentional for security testing)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Suppress urllib3 OpenSSL compatibility warnings
warnings.filterwarnings('ignore', category=UserWarning, module='urllib3')

console = Console()


class HeaderScanner:
    """HTTP Security Header Scanner."""
    
    # Security headers to check
    SECURITY_HEADERS = {
        'Content-Security-Policy': {
            'severity': 'high',
            'description': 'Prevents XSS attacks by controlling resource loading'
        },
        'X-Frame-Options': {
            'severity': 'medium',
            'description': 'Prevents clickjacking attacks'
        },
        'X-XSS-Protection': {
            'severity': 'low',
            'description': 'Enables XSS filter in browsers (deprecated but still used)'
        },
        'Strict-Transport-Security': {
            'severity': 'high',
            'description': 'Forces HTTPS connections (HSTS)'
        },
        'X-Content-Type-Options': {
            'severity': 'medium',
            'description': 'Prevents MIME type sniffing'
        },
        'Referrer-Policy': {
            'severity': 'low',
            'description': 'Controls referrer information sent with requests'
        }
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.results = []
    
    def scan(self, url: str) -> List[Dict]:
        """
        Scan target URL for security headers.
        
        Args:
            url: Target URL
            
        Returns:
            List of header scan results
        """
        self.results = []
        
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            # Try HTTPS first, fallback to HTTP
            try:
                response = requests.get(url, timeout=self.timeout, allow_redirects=True, verify=False)
            except requests.exceptions.SSLError:
                url = url.replace('https://', 'http://')
                response = requests.get(url, timeout=self.timeout, allow_redirects=True, verify=False)
            
            headers = response.headers
            
            # Check each security header
            for header_name, header_info in self.SECURITY_HEADERS.items():
                header_value = headers.get(header_name, None)
                
                result = {
                    'header': header_name,
                    'present': header_value is not None,
                    'value': header_value or 'MISSING',
                    'severity': header_info['severity'],
                    'description': header_info['description'],
                    'status': '✅ Present' if header_value else '❌ Missing'
                }
                
                self.results.append(result)
            
            # Additional checks
            self._check_additional_security(response)
            
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error connecting to {url}: {str(e)}[/red]")
            # Still add results with error status
            for header_name, header_info in self.SECURITY_HEADERS.items():
                self.results.append({
                    'header': header_name,
                    'present': False,
                    'value': 'ERROR',
                    'severity': header_info['severity'],
                    'description': header_info['description'],
                    'status': '❌ Error'
                })
        
        return self.results
    
    def _check_additional_security(self, response: requests.Response) -> None:
        """Check for additional security issues."""
        # Check for server header disclosure
        server_header = response.headers.get('Server', None)
        if server_header:
            self.results.append({
                'header': 'Server',
                'present': True,
                'value': server_header,
                'severity': 'info',
                'description': 'Server information disclosure',
                'status': '⚠️  Present'
            })
        
        # Check for powered-by header
        powered_by = response.headers.get('X-Powered-By', None)
        if powered_by:
            self.results.append({
                'header': 'X-Powered-By',
                'present': True,
                'value': powered_by,
                'severity': 'low',
                'description': 'Technology stack disclosure',
                'status': '⚠️  Present'
            })
    
    def display_results(self) -> None:
        """Display scan results in a formatted table."""
        if not self.results:
            console.print("[yellow]No header scan results.[/yellow]")
            return
        
        table = Table(title="🔒 HTTP Security Headers Scan", show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Header", style="cyan", no_wrap=True)
        table.add_column("Status", style="bold")
        table.add_column("Severity", style="yellow")
        table.add_column("Value", style="white", overflow="fold")
        table.add_column("Description", style="dim")
        
        for result in self.results:
            # Color code severity
            severity_color = {
                'critical': 'red',
                'high': 'bright_red',
                'medium': 'yellow',
                'low': 'blue',
                'info': 'dim'
            }.get(result['severity'], 'white')
            
            severity_text = result['severity'].upper()
            
            table.add_row(
                result['header'],
                result['status'],
                f"[{severity_color}]{severity_text}[/{severity_color}]",
                result['value'][:50] + '...' if len(result['value']) > 50 else result['value'],
                result['description']
            )
        
        console.print(table)
        
        # Summary
        missing_headers = [r for r in self.results if not r['present'] and r['severity'] in ['high', 'medium']]
        if missing_headers:
            console.print(f"\n[red]⚠️  Found {len(missing_headers)} missing security headers![/red]")
    
    def get_results_dict(self) -> List[Dict]:
        """Get results as dictionary for JSON export."""
        return self.results

