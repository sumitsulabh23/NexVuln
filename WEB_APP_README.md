# 🌐 NexVuln Web Application

A beautiful, modern web interface for the NexVuln vulnerability scanner.

## 🚀 Quick Start

### Option 1: Using the Launcher Script (Easiest)
```bash
./run_web.sh
```

### Option 2: Manual Start
```bash
# Install dependencies
pip3 install -r requirements.txt

# Start the web server
python3 -m nexvuln.web_app
```

### Option 3: Using Flask Directly
```bash
export FLASK_APP=nexvuln.web_app
flask run
```

## 📡 Access the Interface

Once started, open your browser and navigate to:
```
http://localhost:5000
```

## ✨ Features

### 🎨 Modern Web Interface
- **Dark Theme** - Easy on the eyes
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Real-time Progress** - See scan progress as it happens
- **Beautiful Tables** - Formatted results with color coding

### 🔍 Scan Options
- **HTTP Security Headers** - Check for missing security headers
- **SSL/TLS Scanner** - Certificate and protocol analysis
- **Port Scanner** - Open port detection (requires Nmap)
- **Directory Discovery** - Find hidden directories and files
- **Full Scan** - Run all modules at once

### 📊 Results Display
- **Formatted Tables** - Easy to read scan results
- **Color-coded Severity** - Visual indicators for issues
- **Badge System** - Quick status identification
- **Download Reports** - Export results as JSON

## 🖥️ Interface Overview

### Main Sections

1. **Target Configuration**
   - Enter target URL or IP address
   - Validate target before scanning

2. **Scan Options**
   - Select which scans to run
   - Choose port scan type (fast/full)
   - Start individual or full scans

3. **Progress Indicator**
   - Real-time progress bar
   - Status messages during scanning

4. **Results Display**
   - Organized by scan type
   - Expandable sections
   - Download button for JSON export

## 📝 Usage Examples

### Scan Security Headers
1. Enter target: `https://example.com`
2. Check "HTTP Security Headers"
3. Click "Start Scan"

### Full Comprehensive Scan
1. Enter target: `example.com`
2. Click "Full Scan (All Modules)"
3. Wait for all scans to complete
4. Review results and download report

### Custom Scan Selection
1. Enter target
2. Select specific scan types
3. Configure port scan type if needed
4. Click "Start Scan"

## 🔧 API Endpoints

The web app uses a REST API. You can also use these endpoints directly:

- `POST /api/scan/headers` - Scan HTTP headers
- `POST /api/scan/ssl` - Scan SSL/TLS
- `POST /api/scan/ports` - Scan ports
- `POST /api/scan/directories` - Directory discovery
- `POST /api/scan/full` - Full scan
- `POST /api/validate` - Validate target
- `POST /api/download` - Download report

### Example API Usage

```bash
# Scan headers
curl -X POST http://localhost:5000/api/scan/headers \
  -H "Content-Type: application/json" \
  -d '{"target": "https://example.com"}'
```

## 🎨 UI Features

### Color Coding
- **Green** - Success, found, valid
- **Red** - Critical issues, missing headers
- **Yellow** - Warnings, medium severity
- **Blue** - Information, low severity

### Badges
- ✅ **Present** - Header found, port open
- ❌ **Missing** - Header not found
- ⚠️ **Warning** - Potential issue
- 🔒 **Unauthorized** - Access denied
- 🚫 **Forbidden** - Blocked access

## 🔒 Security Notes

- The web interface runs on `localhost:5000` by default
- For production, use a proper WSGI server (gunicorn, uWSGI)
- Add authentication if exposing to network
- Only scan systems you own or have permission to test

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in web_app.py
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Module Not Found
```bash
# Make sure package is installed
pip3 install -e .
```

### CORS Errors
- CORS is enabled by default
- If issues persist, check flask-cors installation

## 📱 Mobile Support

The interface is fully responsive and works on:
- Desktop browsers (Chrome, Firefox, Safari, Edge)
- Tablets (iPad, Android tablets)
- Mobile phones (iOS, Android)

## 🚀 Production Deployment

For production use:

1. **Use a Production Server**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 nexvuln.web_app:app
```

2. **Add Authentication**
- Implement login system
- Use Flask-Login or similar
- Add rate limiting

3. **Use HTTPS**
- Set up SSL certificate
- Use nginx as reverse proxy

4. **Environment Variables**
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

## 🎯 Next Steps

- Add user authentication
- Implement scan history
- Add email notifications
- Create scan scheduling
- Add more scan modules

---

**Enjoy scanning!** 🔒✨

