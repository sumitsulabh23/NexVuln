# 🧪 Testing NexVuln Scanner

## Step-by-Step Testing Guide

### Step 1: Install Dependencies

```bash
# Install Python packages
pip3 install -r requirements.txt

# Install Nmap (required for port scanning)
# macOS:
brew install nmap

# Linux:
sudo apt-get install nmap
```

### Step 2: Run Automated Test

```bash
python3 test_nexvuln.py
```

This will check:
- ✅ All Python imports
- ✅ Nmap installation
- ✅ Basic functionality
- ✅ Quick test scan

### Step 3: Test Individual Modules

#### Test 1: HTTP Security Headers (No Nmap Required)
```bash
python3 -m nexvuln.scanner --target https://example.com --headers
```

**Expected Output:**
- Table showing security headers
- Status (Present/Missing)
- Severity levels

#### Test 2: SSL/TLS Scanner
```bash
python3 -m nexvuln.scanner --target example.com --ssl
```

**Expected Output:**
- Certificate information
- TLS version support
- Vulnerability warnings (if any)

#### Test 3: Directory Scanner (No Nmap Required)
```bash
python3 -m nexvuln.scanner --target https://example.com --dirs
```

**Expected Output:**
- Progress bar
- Table of found directories/files
- Status codes

#### Test 4: Port Scanner (Requires Nmap)
```bash
# Quick scan (common ports)
python3 -m nexvuln.scanner --target scanme.nmap.org --ports fast
```

**Note:** `scanme.nmap.org` is authorized by Nmap for testing.

**Expected Output:**
- Progress indicator
- Table of open ports
- Service and version information

### Step 4: Full Scan Test

```bash
python3 -m nexvuln.scanner --target scanme.nmap.org --full-scan
```

This runs all modules and creates `report.json`.

### Step 5: Verify JSON Export

After running any scan, check the JSON report:

```bash
cat report.json | python3 -m json.tool
```

## Test Targets (Authorized for Testing)

1. **scanme.nmap.org** - Official Nmap test server
   - Ports: 22, 80, 9929
   - Safe for port scanning

2. **example.com** - Standard test domain
   - Good for header/SSL/directory scans
   - No port scanning needed

3. **httpbin.org** - HTTP testing service
   - Good for header testing
   - Various endpoints available

## Troubleshooting Tests

### Issue: "Module not found"
```bash
pip3 install -r requirements.txt
```

### Issue: "Nmap not found"
```bash
# macOS
brew install nmap

# Linux
sudo apt-get install nmap
```

### Issue: "Permission denied" (port scanning)
Some port scans require root privileges:
```bash
sudo python3 -m nexvuln.scanner --target localhost --ports fast
```

### Issue: SSL warnings
SSL warnings are normal - the scanner intentionally disables verification for testing.

## Quick Test Checklist

- [ ] Dependencies installed (`pip3 install -r requirements.txt`)
- [ ] Nmap installed (`nmap --version`)
- [ ] Test script passes (`python3 test_nexvuln.py`)
- [ ] Header scan works (`--headers`)
- [ ] SSL scan works (`--ssl`)
- [ ] Directory scan works (`--dirs`)
- [ ] Port scan works (`--ports fast`)
- [ ] JSON export works (check `report.json`)

## Expected Test Results

### Header Scan on example.com
- Should show 6+ security headers
- Some may be missing (expected)
- Severity levels displayed

### SSL Scan on example.com
- Certificate should be valid
- TLS 1.2 or 1.3 should be supported
- No weak ciphers (on modern sites)

### Directory Scan
- Progress bar should appear
- May find some common paths (admin, login, etc.)
- Status codes: 200, 301, 302, 403, 404

### Port Scan on scanme.nmap.org
- Should find ports: 22, 80, 9929
- Service detection should work
- Version information may vary

