"""
SSL/TLS Scanner Module for NexVuln.
Checks certificate validity, TLS versions, and cipher suites.
"""

import ssl
import socket
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


class SSLScanner:
    """SSL/TLS Scanner for certificate and protocol analysis."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.results = {}
    
    def scan(self, target: str) -> Dict:
        """
        Scan target for SSL/TLS configuration.
        
        Args:
            target: Target host or URL
            
        Returns:
            Dictionary with scan results
        """
        self.results = {
            'certificate': {},
            'tls_versions': {},
            'weak_ciphers': [],
            'vulnerabilities': []
        }
        
        # Extract hostname
        if target.startswith(('http://', 'https://')):
            parsed = urlparse(target)
            hostname = parsed.hostname
            port = parsed.port or 443
        else:
            hostname = target.split(':')[0]
            port = int(target.split(':')[1]) if ':' in target else 443
        
        if not hostname:
            console.print("[red]Invalid target hostname[/red]")
            return self.results
        
        try:
            # Check certificate
            self._check_certificate(hostname, port)
            
            # Check TLS versions
            self._check_tls_versions(hostname, port)
            
            # Check cipher suites
            self._check_cipher_suites(hostname, port)
            
        except Exception as e:
            console.print(f"[red]Error scanning SSL/TLS: {str(e)}[/red]")
        
        return self.results
    
    def _check_certificate(self, hostname: str, port: int) -> None:
        """Check SSL certificate validity and expiry."""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse certificate info
                    subject = dict(x[0] for x in cert.get('subject', []))
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    
                    # Check expiry
                    not_after = cert.get('notAfter', '')
                    not_before = cert.get('notBefore', '')
                    
                    if not_after:
                        expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                        days_until_expiry = (expiry_date - datetime.now()).days
                        
                        self.results['certificate'] = {
                            'valid': True,
                            'subject': subject.get('commonName', 'N/A'),
                            'issuer': issuer.get('commonName', 'N/A'),
                            'expires': not_after,
                            'days_until_expiry': days_until_expiry,
                            'expired': days_until_expiry < 0,
                            'expiring_soon': 0 <= days_until_expiry <= 30
                        }
                    else:
                        self.results['certificate'] = {
                            'valid': False,
                            'error': 'Could not parse certificate expiry'
                        }
        
        except ssl.SSLError as e:
            self.results['certificate'] = {
                'valid': False,
                'error': f'SSL Error: {str(e)}'
            }
            self.results['vulnerabilities'].append({
                'type': 'Invalid Certificate',
                'severity': 'high',
                'description': f'Certificate validation failed: {str(e)}'
            })
        except Exception as e:
            self.results['certificate'] = {
                'valid': False,
                'error': f'Connection error: {str(e)}'
            }
    
    def _check_tls_versions(self, hostname: str, port: int) -> None:
        """Check supported TLS versions."""
        tls_versions = {
            'TLSv1.0': ssl.PROTOCOL_TLSv1,
            'TLSv1.1': ssl.PROTOCOL_TLSv1_1,
            'TLSv1.2': ssl.PROTOCOL_TLSv1_2,
            'TLSv1.3': getattr(ssl, 'PROTOCOL_TLS', None)
        }
        
        supported_versions = []
        weak_versions = []
        
        for version_name, protocol in tls_versions.items():
            if protocol is None:
                continue
            
            try:
                context = ssl.SSLContext(protocol)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        supported_versions.append(version_name)
                        if version_name in ['TLSv1.0', 'TLSv1.1']:
                            weak_versions.append(version_name)
            except:
                pass
        
        self.results['tls_versions'] = {
            'supported': supported_versions,
            'weak_versions': weak_versions,
            'has_weak': len(weak_versions) > 0
        }
        
        if weak_versions:
            self.results['vulnerabilities'].append({
                'type': 'Weak TLS Version',
                'severity': 'high',
                'description': f'Server supports deprecated TLS versions: {", ".join(weak_versions)}'
            })
    
    def _check_cipher_suites(self, hostname: str, port: int) -> None:
        """Check for weak cipher suites."""
        # Common weak ciphers
        weak_ciphers = [
            'RC4', 'DES', 'MD5', 'SHA1', 'NULL', 'EXPORT', 'ANON', 'ADH', 'LOW', '3DES'
        ]
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cipher = ssock.cipher()
                    if cipher:
                        cipher_name = cipher[0]
                        
                        # Check if cipher is weak
                        is_weak = any(weak in cipher_name for weak in weak_ciphers)
                        
                        if is_weak:
                            self.results['weak_ciphers'].append({
                                'cipher': cipher_name,
                                'severity': 'medium',
                                'description': 'Weak cipher suite detected'
                            })
                            
                            self.results['vulnerabilities'].append({
                                'type': 'Weak Cipher Suite',
                                'severity': 'medium',
                                'description': f'Weak cipher in use: {cipher_name}'
                            })
        except Exception as e:
            pass
    
    def display_results(self) -> None:
        """Display scan results in formatted tables."""
        # Certificate Info
        cert_table = Table(title="🔐 SSL/TLS Certificate Information", show_header=True, header_style="bold magenta", box=box.ROUNDED)
        cert_table.add_column("Property", style="cyan")
        cert_table.add_column("Value", style="white")
        
        cert = self.results.get('certificate', {})
        if cert.get('valid'):
            status = "✅ Valid" if not cert.get('expired') else "❌ Expired"
            if cert.get('expiring_soon'):
                status = "⚠️  Expiring Soon"
            
            cert_table.add_row("Status", status)
            cert_table.add_row("Subject", cert.get('subject', 'N/A'))
            cert_table.add_row("Issuer", cert.get('issuer', 'N/A'))
            cert_table.add_row("Expires", cert.get('expires', 'N/A'))
            cert_table.add_row("Days Until Expiry", str(cert.get('days_until_expiry', 'N/A')))
        else:
            cert_table.add_row("Status", "❌ Invalid")
            cert_table.add_row("Error", cert.get('error', 'Unknown error'))
        
        console.print(cert_table)
        
        # TLS Versions
        tls_table = Table(title="🔒 TLS Version Support", show_header=True, header_style="bold magenta", box=box.ROUNDED)
        tls_table.add_column("Version", style="cyan")
        tls_table.add_column("Status", style="bold")
        
        tls_info = self.results.get('tls_versions', {})
        supported = tls_info.get('supported', [])
        weak = tls_info.get('weak_versions', [])
        
        all_versions = ['TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']
        for version in all_versions:
            if version in supported:
                if version in weak:
                    tls_table.add_row(version, "[red]⚠️  Supported (WEAK)[/red]")
                else:
                    tls_table.add_row(version, "[green]✅ Supported[/green]")
            else:
                tls_table.add_row(version, "[dim]❌ Not Supported[/dim]")
        
        console.print(tls_table)
        
        # Vulnerabilities
        vulnerabilities = self.results.get('vulnerabilities', [])
        if vulnerabilities:
            vuln_table = Table(title="⚠️  SSL/TLS Vulnerabilities", show_header=True, header_style="bold red", box=box.ROUNDED)
            vuln_table.add_column("Type", style="cyan")
            vuln_table.add_column("Severity", style="yellow")
            vuln_table.add_column("Description", style="white")
            
            for vuln in vulnerabilities:
                severity_color = {
                    'critical': 'red',
                    'high': 'bright_red',
                    'medium': 'yellow',
                    'low': 'blue'
                }.get(vuln.get('severity', 'low'), 'white')
                
                vuln_table.add_row(
                    vuln.get('type', 'N/A'),
                    f"[{severity_color}]{vuln.get('severity', 'N/A').upper()}[/{severity_color}]",
                    vuln.get('description', 'N/A')
                )
            
            console.print(vuln_table)
        else:
            console.print("[green]✅ No SSL/TLS vulnerabilities detected![/green]")
    
    def get_results_dict(self) -> Dict:
        """Get results as dictionary for JSON export."""
        return self.results

