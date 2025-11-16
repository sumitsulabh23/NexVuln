# 🔧 Port 5000 Issue - Fixed!

## The Problem

You got a **403 Forbidden** error because **port 5000 is used by macOS AirPlay Receiver**.

This is a common issue on macOS - the AirPlay service automatically uses port 5000.

## ✅ Solution Applied

I've changed the web app to use **port 5001** instead.

## 🚀 How to Start Now

### Option 1: Use the Updated Script
```bash
cd /Users/sumitsulabh/HealBot
./run_web.sh
```

Then open: **http://localhost:5001**

### Option 2: Run Directly
```bash
python3 -m nexvuln.web_app 5001
```

### Option 3: Use a Different Port
```bash
# Use any port you want:
python3 -m nexvuln.web_app 8080
```

## 🌐 New Access URL

**http://localhost:5001**

(Instead of port 5000)

## 🔍 Why This Happened

macOS has a service called "AirPlay Receiver" that uses port 5000 by default. When you tried to access `localhost:5000`, you were hitting the AirPlay service (which requires authorization), not the Flask app.

## 💡 Alternative: Disable AirPlay (Not Recommended)

If you really want to use port 5000:

1. Go to **System Preferences** → **General** → **AirDrop & Handoff**
2. Uncheck **"AirPlay Receiver"**
3. Restart your Flask app on port 5000

But using port 5001 is easier! ✅

## ✅ Status

- ✅ Web app now uses port 5001
- ✅ No conflicts with macOS services
- ✅ Ready to use!

---

**Start the server and access it at: http://localhost:5001** 🎉

