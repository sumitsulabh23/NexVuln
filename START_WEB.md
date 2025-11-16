# 🌐 Starting the NexVuln Web Application

## Quick Start

### You're in the wrong directory!

The `run_web.sh` script is in the **HealBot** directory, not the `nexvuln` subdirectory.

### Solution 1: Navigate to HealBot Directory

```bash
# Go to the parent directory
cd /Users/sumitsulabh/HealBot

# Then run the script
./run_web.sh
```

### Solution 2: Run Directly from Anywhere

```bash
# From anywhere, run:
cd /Users/sumitsulabh/HealBot && ./run_web.sh
```

### Solution 3: Run Python Module Directly

```bash
# From the HealBot directory:
python3 -m nexvuln.web_app

# Or from anywhere (since package is installed):
python3 -m nexvuln.web_app
```

## After Starting

1. **Wait for the message:**
   ```
   🌐 Starting web server...
   📡 Access the interface at: http://localhost:5000
   ```

2. **Open your browser:**
   ```
   http://localhost:5000
   ```

3. **Start scanning!**

## Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

