#!/usr/bin/env python3
"""
NexVuln - Mini Nessus Clone
Main scanner entry point with CLI interface.
"""

import warnings
# Suppress urllib3 OpenSSL warnings early (compatibility issue, not critical)
warnings.filterwarnings('ignore', message='.*urllib3.*OpenSSL.*', category=UserWarning)
warnings.filterwarnings('ignore', message='.*NotOpenSSLWarning.*')

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

from nexvuln.port_scanner import PortScanner
from nexvuln.header_scanner import HeaderScanner
from nexvuln.ssl_scanner import SSLScanner
from nexvuln.directory_scanner import DirectoryScanner
from nexvuln.utils import validate_target, normalize_url, get_protocol

console = Console()


class NexVulnScanner:
    """Main scanner orchestrator."""
    
    def __init__(self):
        self.target = None
        self.results = {
            'target': None,
            'scan_date': None,
            'port_scan': [],
            'header_scan': [],
            'ssl_scan': {},
            'directory_scan': []
        }
    
    def run_full_scan(self, target: str, port_scan_type: str = "fast") -> Dict:
        """
        Run all scan modules.
        
        Args:
            target: Target URL or IP
            port_scan_type: "fast" or "full" for port scanning
            
        Returns:
            Complete scan results dictionary
        """
        self.target = target
        self.results['target'] = target
        self.results['scan_date'] = datetime.now().isoformat()
        
        # Validate target
        is_valid, host, port = validate_target(target)
        if not is_valid:
            console.print(f"[red]❌ Invalid or unreachable target: {target}[/red]")
            return self.results
        
        console.print(Panel.fit(
            f"[bold cyan]NexVuln - Mini Nessus Clone[/bold cyan]\n"
            f"[white]Target: {target}[/white]\n"
            f"[white]Host: {host}:{port}[/white]",
            border_style="cyan",
            box=box.DOUBLE
        ))
        console.print()
        
        # 1. Port Scan
        console.print("[bold yellow]━━━ Port Scanning ━━━[/bold yellow]")
        try:
            port_scanner = PortScanner()
            port_results = port_scanner.scan(host, scan_type=port_scan_type)
            port_scanner.display_results()
            self.results['port_scan'] = port_scanner.get_results_dict()
        except Exception as e:
            console.print(f"[red]Port scan error: {str(e)}[/red]")
        console.print()
        
        # 2. HTTP Security Headers Scan
        console.print("[bold yellow]━━━ HTTP Security Headers Scan ━━━[/bold yellow]")
        try:
            header_scanner = HeaderScanner()
            header_results = header_scanner.scan(normalize_url(target))
            header_scanner.display_results()
            self.results['header_scan'] = header_scanner.get_results_dict()
        except Exception as e:
            console.print(f"[red]Header scan error: {str(e)}[/red]")
        console.print()
        
        # 3. SSL/TLS Scan (only for HTTPS)
        if get_protocol(target) == 'https' or port == 443:
            console.print("[bold yellow]━━━ SSL/TLS Scan ━━━[/bold yellow]")
            try:
                ssl_scanner = SSLScanner()
                ssl_results = ssl_scanner.scan(normalize_url(target))
                ssl_scanner.display_results()
                self.results['ssl_scan'] = ssl_scanner.get_results_dict()
            except Exception as e:
                console.print(f"[red]SSL scan error: {str(e)}[/red]")
            console.print()
        
        # 4. Directory Brute Force
        console.print("[bold yellow]━━━ Directory/File Discovery ━━━[/bold yellow]")
        try:
            dir_scanner = DirectoryScanner()
            dir_results = dir_scanner.scan(normalize_url(target))
            dir_scanner.display_results()
            self.results['directory_scan'] = dir_scanner.get_results_dict()
        except Exception as e:
            console.print(f"[red]Directory scan error: {str(e)}[/red]")
        console.print()
        
        return self.results
    
    def run_port_scan(self, target: str, scan_type: str = "fast") -> List[Dict]:
        """Run only port scan."""
        is_valid, host, port = validate_target(target)
        if not is_valid:
            console.print(f"[red]❌ Invalid target: {target}[/red]")
            return []
        
        port_scanner = PortScanner()
        results = port_scanner.scan(host, scan_type=scan_type)
        port_scanner.display_results()
        return results
    
    def run_header_scan(self, target: str) -> List[Dict]:
        """Run only header scan."""
        header_scanner = HeaderScanner()
        results = header_scanner.scan(normalize_url(target))
        header_scanner.display_results()
        return results
    
    def run_ssl_scan(self, target: str) -> Dict:
        """Run only SSL scan."""
        ssl_scanner = SSLScanner()
        results = ssl_scanner.scan(normalize_url(target))
        ssl_scanner.display_results()
        return results
    
    def run_directory_scan(self, target: str, wordlist_path: Optional[str] = None) -> List[Dict]:
        """Run only directory scan."""
        dir_scanner = DirectoryScanner()
        if wordlist_path:
            dir_scanner.load_wordlist(wordlist_path)
        results = dir_scanner.scan(normalize_url(target))
        dir_scanner.display_results()
        return results
    
    def export_results(self, output_file: str = "report.json") -> None:
        """
        Export scan results to JSON file.
        
        Args:
            output_file: Output file path
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            console.print(f"\n[green]✅ Results exported to: {output_file}[/green]")
        except Exception as e:
            console.print(f"[red]Error exporting results: {str(e)}[/red]")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='NexVuln - Mini Nessus Clone | Comprehensive Vulnerability Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nexvuln --target example.com --full-scan
  nexvuln --target 192.168.1.1 --ports full
  nexvuln --target https://example.com --headers
  nexvuln --target example.com --ssl
  nexvuln --target example.com --dirs --wordlist wordlist.txt
        """
    )
    
    parser.add_argument(
        '--target', '-t',
        required=True,
        help='Target URL or IP address'
    )
    
    parser.add_argument(
        '--full-scan', '-f',
        action='store_true',
        help='Run all scan modules (port, headers, SSL, directories)'
    )
    
    parser.add_argument(
        '--ports',
        choices=['fast', 'full'],
        help='Scan ports (fast: common ports, full: 1-65535)'
    )
    
    parser.add_argument(
        '--headers',
        action='store_true',
        help='Scan HTTP security headers'
    )
    
    parser.add_argument(
        '--ssl',
        action='store_true',
        help='Scan SSL/TLS configuration'
    )
    
    parser.add_argument(
        '--dirs',
        action='store_true',
        help='Brute force directories and files'
    )
    
    parser.add_argument(
        '--wordlist', '-w',
        help='Custom wordlist file for directory scanning'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='report.json',
        help='Output JSON file (default: report.json)'
    )
    
    args = parser.parse_args()
    
    scanner = NexVulnScanner()
    
    # Determine scan mode
    if args.full_scan:
        # Full scan
        port_scan_type = args.ports or "fast"
        scanner.run_full_scan(args.target, port_scan_type=port_scan_type)
        scanner.export_results(args.output)
    
    elif args.ports or args.headers or args.ssl or args.dirs:
        # Individual scans
        if args.ports:
            scanner.run_port_scan(args.target, scan_type=args.ports)
        
        if args.headers:
            scanner.run_header_scan(args.target)
        
        if args.ssl:
            scanner.run_ssl_scan(args.target)
        
        if args.dirs:
            scanner.run_directory_scan(args.target, wordlist_path=args.wordlist)
        
        # Export if any scan was run
        scanner.export_results(args.output)
    
    else:
        # Default: full scan
        console.print("[yellow]No specific scan selected. Running full scan...[/yellow]\n")
        scanner.run_full_scan(args.target)
        scanner.export_results(args.output)


if __name__ == '__main__':
    main()

