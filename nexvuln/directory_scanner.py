"""
Directory Brute Force Scanner Module for NexVuln.
Scans for common directories and files.
"""

import requests
import urllib3
import warnings
from typing import List, Dict, Optional
from urllib.parse import urljoin
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich import box

# Suppress SSL warnings (intentional for security testing)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Suppress urllib3 OpenSSL compatibility warnings
warnings.filterwarnings('ignore', category=UserWarning, module='urllib3')

console = Console()


class DirectoryScanner:
    """Directory and file brute force scanner."""
    
    # Default wordlist of common directories
    DEFAULT_WORDLIST = [
        'admin', 'administrator', 'login', 'wp-admin', 'wp-login', 'dashboard',
        'backup', 'backups', 'config', 'configuration', 'conf', 'settings',
        'api', 'v1', 'v2', 'test', 'testing', 'dev', 'development', 'staging',
        'phpmyadmin', 'mysql', 'database', 'db', 'sql', 'phpinfo', 'info',
        'logs', 'log', 'error', 'errors', 'debug', 'tmp', 'temp', 'cache',
        'assets', 'static', 'public', 'private', 'secure', 'secure_files',
        'uploads', 'upload', 'files', 'file', 'images', 'img', 'media',
        'download', 'downloads', 'documents', 'docs', 'documentation',
        'old', 'old_files', 'archive', 'archives', 'www', 'wwwroot',
        'includes', 'include', 'includes_files', 'lib', 'libs', 'library',
        'scripts', 'script', 'js', 'css', 'styles', 'style',
        'robots.txt', 'sitemap.xml', '.git', '.svn', '.env', '.htaccess',
        'web.config', 'crossdomain.xml', 'clientaccesspolicy.xml',
        'readme', 'readme.txt', 'license', 'changelog', 'changelog.txt',
        'install', 'install.php', 'setup', 'setup.php', 'upgrade',
        'search', 'search.php', 'index.php.bak', 'index.html.bak',
        'admin.php', 'admin.html', 'admin/index', 'admin/login',
        'manager', 'management', 'control', 'controlpanel', 'panel'
    ]
    
    # Status codes that indicate found resources
    FOUND_STATUS_CODES = [200, 201, 202, 204, 301, 302, 307, 401, 403]
    
    def __init__(self, timeout: int = 5, wordlist: Optional[List[str]] = None):
        self.timeout = timeout
        self.wordlist = wordlist or self.DEFAULT_WORDLIST
        self.results = []
    
    def scan(self, url: str, threads: int = 10) -> List[Dict]:
        """
        Scan target URL for directories and files.
        
        Args:
            url: Target URL
            threads: Number of concurrent threads (not used in this implementation)
            
        Returns:
            List of found directories/files
        """
        self.results = []
        
        # Normalize URL
        if not url.endswith('/'):
            url = url + '/'
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Try HTTPS first, fallback to HTTP
        try:
            test_response = requests.get(url, timeout=self.timeout, verify=False, allow_redirects=True)
        except requests.exceptions.SSLError:
            url = url.replace('https://', 'http://')
            test_response = requests.get(url, timeout=self.timeout, allow_redirects=True)
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error connecting to {url}: {str(e)}[/red]")
            return self.results
        
        # Scan directories
        with Progress(
            BarColumn(),
            TextColumn("[progress.description]{task.description}"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Scanning directories...", total=len(self.wordlist))
            
            for directory in self.wordlist:
                test_url = urljoin(url, directory)
                
                try:
                    response = requests.get(
                        test_url,
                        timeout=self.timeout,
                        allow_redirects=True,
                        verify=False
                    )
                    
                    status_code = response.status_code
                    
                    if status_code in self.FOUND_STATUS_CODES:
                        result = {
                            'url': test_url,
                            'path': directory,
                            'status_code': status_code,
                            'status': 'Found',
                            'content_length': len(response.content),
                            'response_time': response.elapsed.total_seconds()
                        }
                        self.results.append(result)
                
                except requests.exceptions.RequestException:
                    pass
                
                progress.update(task, advance=1)
        
        return self.results
    
    def load_wordlist(self, filepath: str) -> bool:
        """
        Load wordlist from file.
        
        Args:
            filepath: Path to wordlist file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.wordlist = [line.strip() for line in f if line.strip()]
            return True
        except Exception as e:
            console.print(f"[red]Error loading wordlist: {str(e)}[/red]")
            return False
    
    def display_results(self) -> None:
        """Display scan results in a formatted table."""
        if not self.results:
            console.print("[yellow]No directories/files found.[/yellow]")
            return
        
        table = Table(title="📁 Directory/File Discovery Results", show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Path", style="cyan", no_wrap=False)
        table.add_column("Status Code", style="bold yellow", justify="center")
        table.add_column("Status", style="bold")
        table.add_column("Size", style="dim")
        table.add_column("Response Time", style="dim")
        
        for result in self.results:
            # Color code status
            status_code = result['status_code']
            if status_code == 200:
                status_color = "[green]✅ Found[/green]"
            elif status_code in [301, 302, 307]:
                status_color = "[yellow]↪️  Redirect[/yellow]"
            elif status_code == 403:
                status_color = "[red]🚫 Forbidden[/red]"
            elif status_code == 401:
                status_color = "[blue]🔒 Unauthorized[/blue]"
            else:
                status_color = f"[white]✅ Found ({status_code})[/white]"
            
            size = f"{result['content_length']} bytes"
            response_time = f"{result['response_time']:.2f}s"
            
            table.add_row(
                result['path'],
                str(status_code),
                status_color,
                size,
                response_time
            )
        
        console.print(table)
        console.print(f"\n[green]✅ Found {len(self.results)} accessible paths![/green]")
    
    def get_results_dict(self) -> List[Dict]:
        """Get results as dictionary for JSON export."""
        return self.results

