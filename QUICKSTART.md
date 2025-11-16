# 🚀 NexVuln Quick Start Guide

## Installation (3 Steps)

### 1. Install Nmap (System Dependency)
```bash
# macOS
brew install nmap

# Linux (Ubuntu/Debian)
sudo apt-get install nmap

# Linux (CentOS/RHEL)
sudo yum install nmap
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python -m nexvuln.scanner --help
```

## Quick Examples

### Scan a Website (Full Scan)
```bash
python -m nexvuln.scanner --target example.com --full-scan
```

### Quick Port Scan
```bash
python -m nexvuln.scanner --target 192.168.1.1 --ports fast
```

### Check Security Headers
```bash
python -m nexvuln.scanner --target https://example.com --headers
```

### SSL/TLS Analysis
```bash
python -m nexvuln.scanner --target example.com --ssl
```

### Find Hidden Directories
```bash
python -m nexvuln.scanner --target example.com --dirs
```

## Output

- **Console**: Beautiful formatted tables with color coding
- **JSON Report**: Automatically saved to `report.json` (or custom filename with `--output`)

## Tips

- Use `--ports fast` for quick scans (common ports only)
- Use `--ports full` for comprehensive port scanning (1-65535) - **takes longer**
- Custom wordlist: `--dirs --wordlist my_wordlist.txt`
- All scans: `--full-scan` runs everything

## Legal Notice

⚠️ **Only scan systems you own or have explicit permission to test!**

Unauthorized scanning is illegal and unethical.

