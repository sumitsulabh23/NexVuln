# 🚀 Quick Start - NexVuln Web Interface

## Start the Web Application

### Method 1: Easy Launcher (Recommended)
```bash
./run_web.sh
```

### Method 2: Direct Python
```bash
python3 -m nexvuln.web_app
```

## Access the Interface

Open your browser and go to:
```
http://localhost:5000
```

## First Steps

1. **Enter a Target**
   - Type a URL like `https://example.com`
   - Or an IP like `192.168.1.1`

2. **Click "Validate"** (optional)
   - Checks if target is reachable

3. **Select Scan Options**
   - ☑ HTTP Security Headers
   - ☑ SSL/TLS Configuration
   - ☐ Port Scanner (requires Nmap)
   - ☑ Directory Discovery

4. **Start Scanning**
   - Click "Start Scan" for selected options
   - Or "Full Scan" for everything

5. **View Results**
   - Results appear in formatted tables
   - Download JSON report if needed

## Example Workflow

```bash
# 1. Start the server
./run_web.sh

# 2. Open browser to http://localhost:5000

# 3. Enter target: https://example.com

# 4. Select: Headers + SSL + Directories

# 5. Click "Start Scan"

# 6. Wait for results...

# 7. Review findings and download report
```

## Features

✅ **Beautiful Dark Theme UI**
✅ **Real-time Progress Updates**
✅ **Color-coded Results**
✅ **Download JSON Reports**
✅ **Responsive Design** (works on mobile)
✅ **All Scanner Modules Available**

## Troubleshooting

**Port 5000 already in use?**
- Change port in `nexvuln/web_app.py` (last line)
- Or kill the process: `lsof -ti:5000 | xargs kill`

**Module not found?**
```bash
pip3 install -r requirements.txt
pip3 install -e .
```

**Can't access from other devices?**
- Change `host='0.0.0.0'` in `web_app.py` (already set)
- Make sure firewall allows port 5000

---

**Enjoy the web interface!** 🌐✨

