# 🔒 NexVuln - Mini Nessus Clone

A comprehensive, production-ready vulnerability scanner for web applications and network services. NexVuln combines multiple scanning techniques to provide a complete security assessment of your targets.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### 🔍 **Open Port Scanner**
- Fast scan of common ports or full port range (1-65535)
- Service and version detection using Nmap
- Clean, formatted table output
- Identifies running services and potential attack vectors

### 🛡️ **HTTP Security Header Scanner**
- Checks for critical security headers:
  - `Content-Security-Policy` (XSS protection)
  - `X-Frame-Options` (Clickjacking protection)
  - `X-XSS-Protection` (Browser XSS filter)
  - `Strict-Transport-Security` (HSTS)
  - `X-Content-Type-Options` (MIME sniffing protection)
  - `Referrer-Policy` (Referrer information control)
- Severity-based reporting
- Detects information disclosure headers

### 🔐 **SSL/TLS Scanner**
- Certificate validity and expiry checking
- TLS version detection (1.0, 1.1, 1.2, 1.3)
- Weak cipher suite detection
- Vulnerability identification
- Days until certificate expiry calculation

### 📁 **Directory Brute Force Scanner**
- Discovers hidden directories and files
- Customizable wordlist support
- Status code analysis (200, 301, 302, 403, etc.)
- Response time and size tracking
- Default wordlist with 100+ common paths

## 📋 Requirements

- **Python 3.7+**
- **Nmap** (must be installed on system)
- Python packages (see `requirements.txt`)

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd /path/to/nexvuln
```

### 2. Install System Dependencies

#### macOS:
```bash
brew install nmap
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install nmap
```

#### Linux (CentOS/RHEL):
```bash
sudo yum install nmap
```

#### Windows:
Download and install Nmap from: https://nmap.org/download.html

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or using pip3:
```bash
pip3 install -r requirements.txt
```

### 4. Install as Package (Optional)

```bash
pip install -e .
```

## 📖 Usage

### Basic Usage

#### Full Scan (All Modules)
```bash
python -m nexvuln.scanner --target example.com --full-scan
```

#### Quick Port Scan (Common Ports)
```bash
python -m nexvuln.scanner --target 192.168.1.1 --ports fast
```

#### Full Port Range Scan
```bash
python -m nexvuln.scanner --target example.com --ports full
```

#### HTTP Security Headers Only
```bash
python -m nexvuln.scanner --target https://example.com --headers
```

#### SSL/TLS Scan Only
```bash
python -m nexvuln.scanner --target example.com --ssl
```

#### Directory Brute Force Only
```bash
python -m nexvuln.scanner --target example.com --dirs
```

#### Custom Wordlist for Directory Scan
```bash
python -m nexvuln.scanner --target example.com --dirs --wordlist custom_wordlist.txt
```

#### Custom Output File
```bash
python -m nexvuln.scanner --target example.com --full-scan --output my_report.json
```

### Command-Line Options

```
--target, -t          Target URL or IP address (required)
--full-scan, -f       Run all scan modules
--ports {fast,full}   Port scan mode (fast: common ports, full: 1-65535)
--headers             Scan HTTP security headers
--ssl                 Scan SSL/TLS configuration
--dirs                Brute force directories and files
--wordlist, -w        Custom wordlist file for directory scanning
--output, -o          Output JSON file (default: report.json)
```

## 📊 Example Output

### Port Scan Results
```
🔍 Open Ports Scan Results
┌──────┬──────────┬────────┬──────────┬─────────────────────┬──────────┐
│ Port │ Protocol │ State  │ Service  │ Version             │ Product  │
├──────┼──────────┼────────┼──────────┼─────────────────────┼──────────┤
│ 22   │ TCP      │ OPEN   │ ssh      │ OpenSSH 8.2        │ N/A      │
│ 80   │ TCP      │ OPEN   │ http     │ Apache 2.4.41      │ N/A      │
│ 443  │ TCP      │ OPEN   │ https    │ Apache 2.4.41      │ N/A      │
└──────┴──────────┴────────┴──────────┴─────────────────────┴──────────┘
```

### Security Headers Results
```
🔒 HTTP Security Headers Scan
┌─────────────────────────────┬──────────────┬──────────┬──────────────────────────┐
│ Header                      │ Status       │ Severity │ Value                    │
├─────────────────────────────┼──────────────┼──────────┼──────────────────────────┤
│ Content-Security-Policy     │ ❌ Missing   │ HIGH     │ MISSING                  │
│ X-Frame-Options             │ ✅ Present   │ MEDIUM   │ DENY                     │
│ Strict-Transport-Security   │ ✅ Present   │ HIGH     │ max-age=31536000         │
└─────────────────────────────┴──────────────┴──────────┴──────────────────────────┘
```

### SSL/TLS Results
```
🔐 SSL/TLS Certificate Information
┌──────────────────────┬─────────────────────────────────────┐
│ Property             │ Value                               │
├──────────────────────┼─────────────────────────────────────┤
│ Status               │ ✅ Valid                            │
│ Subject              │ example.com                         │
│ Issuer               │ Let's Encrypt                       │
│ Expires              │ Dec 31 23:59:59 2024 GMT           │
│ Days Until Expiry    │ 45                                  │
└──────────────────────┴─────────────────────────────────────┘
```

### Directory Discovery Results
```
📁 Directory/File Discovery Results
┌──────────────┬─────────────┬──────────────┬──────────┬──────────────┐
│ Path         │ Status Code │ Status       │ Size     │ Response Time│
├──────────────┼─────────────┼──────────────┼──────────┼──────────────┤
│ /admin       │ 302         │ ↪️  Redirect │ 256 bytes│ 0.12s        │
│ /login       │ 200         │ ✅ Found     │ 1024 bytes│ 0.08s        │
│ /backup      │ 403         │ 🚫 Forbidden │ 0 bytes  │ 0.05s        │
└──────────────┴─────────────┴──────────────┴──────────┴──────────────┘
```

## 📁 Project Structure

```
nexvuln/
├── __init__.py              # Package initialization
├── scanner.py               # Main CLI entry point
├── port_scanner.py          # Port scanning module
├── header_scanner.py        # HTTP headers scanner
├── ssl_scanner.py           # SSL/TLS scanner
├── directory_scanner.py      # Directory brute force
└── utils.py                 # Utility functions

requirements.txt             # Python dependencies
wordlist.txt                 # Default wordlist for directory scanning
README.md                    # This file
```

## 🔧 Module Details

### Port Scanner (`port_scanner.py`)
- Uses `python-nmap` for port scanning
- Supports fast (common ports) and full (1-65535) scan modes
- Service and version detection
- Protocol identification (TCP/UDP)

### Header Scanner (`header_scanner.py`)
- Checks 6 critical security headers
- Severity classification (Critical, High, Medium, Low)
- Detects information disclosure
- Follows redirects automatically

### SSL Scanner (`ssl_scanner.py`)
- Certificate validation and expiry checking
- TLS version support detection
- Weak cipher identification
- Vulnerability reporting

### Directory Scanner (`directory_scanner.py`)
- Default 100+ word wordlist
- Custom wordlist support
- Status code analysis
- Response time tracking

## 📝 JSON Report Format

Results are exported to JSON with the following structure:

```json
{
  "target": "example.com",
  "scan_date": "2024-01-15T10:30:00",
  "port_scan": [
    {
      "port": 80,
      "protocol": "tcp",
      "state": "open",
      "service": "http",
      "version": "Apache 2.4.41"
    }
  ],
  "header_scan": [
    {
      "header": "Content-Security-Policy",
      "present": false,
      "value": "MISSING",
      "severity": "high"
    }
  ],
  "ssl_scan": {
    "certificate": {
      "valid": true,
      "subject": "example.com",
      "days_until_expiry": 45
    },
    "tls_versions": {
      "supported": ["TLSv1.2", "TLSv1.3"],
      "weak_versions": []
    }
  },
  "directory_scan": [
    {
      "url": "https://example.com/admin",
      "path": "admin",
      "status_code": 302,
      "status": "Found"
    }
  ]
}
```

## ⚠️ Important Notes

1. **Legal Usage**: Only scan systems you own or have explicit permission to test. Unauthorized scanning is illegal.

2. **Nmap Installation**: Nmap must be installed on your system for port scanning to work.

3. **SSL Warnings**: The scanner disables SSL verification for some checks. This is intentional for testing purposes but may show warnings.

4. **Performance**: Full port scans (1-65535) can take a long time. Use `--ports fast` for quicker results.

5. **Rate Limiting**: Be mindful of rate limiting when scanning. The scanner includes timeouts to prevent hanging.

## 🐛 Troubleshooting

### "Nmap not found" Error
- Ensure Nmap is installed: `nmap --version`
- On Linux, you may need to run with `sudo` for some scan types

### "SSL Certificate Verification Failed"
- This is expected behavior for testing. The scanner intentionally disables verification for some checks.

### "Connection Timeout"
- Check if the target is reachable: `ping example.com`
- Verify firewall settings
- Try with `--ports fast` for quicker scans

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.7 or higher

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Inspired by Nessus vulnerability scanner
- Uses `python-nmap` for port scanning
- Beautiful CLI output powered by `rich`
- Built with security best practices in mind

## 📧 Support

For issues, questions, or contributions, please open an issue on the project repository.

---

**⚠️ Disclaimer**: This tool is for authorized security testing only. Unauthorized use against systems you don't own or have permission to test is illegal and unethical.
