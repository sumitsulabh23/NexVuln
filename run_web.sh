#!/bin/bash
# NexVuln Web Application Launcher

cd "$(dirname "$0")" || exit 1

echo "🔒 NexVuln Web Application"
echo "=========================="
echo ""
echo "📦 Installing/updating dependencies..."
pip3 install -q -r requirements.txt

echo ""
echo "🔍 Checking for existing servers..."
# Kill any existing NexVuln web servers
lsof -ti:5001,5002,5003,8080 2>/dev/null | xargs kill -9 2>/dev/null || true
ps aux | grep "nexvuln.web_app" | grep -v grep | awk '{print $2}' | xargs kill -9 2>/dev/null || true
sleep 1

echo ""
echo "🌐 Starting web server..."
echo "💡 Note: Will auto-find available port (5000 is used by macOS AirPlay)"
echo "⚠️  Press Ctrl+C to stop the server"
echo ""

python3 -m nexvuln.web_app

