"""
Port Scanner Module for NexVuln.
Scans for open ports and detects services/versions.
"""

import nmap
from typing import List, Dict, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class PortScanner:
    """Port scanner using python-nmap."""
    
    def __init__(self):
        self.scanner = nmap.PortScanner()
        self.results = []
    
    def scan(self, target: str, ports: str = "1-1000", scan_type: str = "fast") -> List[Dict]:
        """
        Scan target for open ports.
        
        Args:
            target: Target host or IP
            ports: Port range (e.g., "1-1000", "80,443,8080")
            scan_type: "fast" for common ports, "full" for full range
            
        Returns:
            List of open port information
        """
        self.results = []
        
        # Adjust ports based on scan type
        if scan_type == "fast":
            ports = "21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5432,5900,8080,8443"
        elif scan_type == "full":
            ports = "1-65535"
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task(f"[cyan]Scanning ports on {target}...", total=None)
                
                # Perform scan
                self.scanner.scan(target, ports, arguments='-sV -sC --version-intensity 5')
                
                progress.update(task, completed=True)
            
            # Parse results
            if target in self.scanner.all_hosts():
                for proto in self.scanner[target].all_protocols():
                    ports_list = self.scanner[target][proto].keys()
                    
                    for port in ports_list:
                        port_info = self.scanner[target][proto][port]
                        result = {
                            'port': port,
                            'protocol': proto,
                            'state': port_info['state'],
                            'service': port_info.get('name', 'unknown'),
                            'version': port_info.get('version', ''),
                            'product': port_info.get('product', ''),
                            'extrainfo': port_info.get('extrainfo', '')
                        }
                        
                        if result['state'] == 'open':
                            self.results.append(result)
        
        except nmap.PortScannerError as e:
            console.print(f"[red]Nmap error: {str(e)}[/red]")
        except Exception as e:
            console.print(f"[red]Error scanning ports: {str(e)}[/red]")
        
        return self.results
    
    def display_results(self) -> None:
        """Display scan results in a formatted table."""
        if not self.results:
            console.print("[yellow]No open ports found.[/yellow]")
            return
        
        table = Table(title="🔍 Open Ports Scan Results", show_header=True, header_style="bold magenta")
        table.add_column("Port", style="cyan", no_wrap=True)
        table.add_column("Protocol", style="green")
        table.add_column("State", style="yellow")
        table.add_column("Service", style="blue")
        table.add_column("Version", style="magenta")
        table.add_column("Product", style="white")
        
        for result in self.results:
            version_info = result['version'] or 'N/A'
            if result['extrainfo']:
                version_info += f" ({result['extrainfo']})"
            
            table.add_row(
                str(result['port']),
                result['protocol'].upper(),
                result['state'].upper(),
                result['service'],
                version_info,
                result['product'] or 'N/A'
            )
        
        console.print(table)
    
    def get_results_dict(self) -> List[Dict]:
        """Get results as dictionary for JSON export."""
        return self.results

