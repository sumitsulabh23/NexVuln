# Fix: ModuleNotFoundError: No module named 'nexvuln'

## The Problem

You're getting this error because Python can't find the `nexvuln` module. This happens when:

1. **Running from the wrong directory** - You're inside the `nexvuln/` folder instead of the parent `HealBot/` folder
2. **Python path issue** - Python doesn't know where to find the module

## Solutions

### Solution 1: Run from the Correct Directory (Easiest)

**Always run from the `HealBot` directory (parent of `nexvuln/`):**

```bash
# Make sure you're in HealBot directory
cd /Users/sumitsulabh/HealBot

# Then run the scanner
python3 -m nexvuln.scanner --target example.com --headers
```

### Solution 2: Use the Wrapper Script

I've created a wrapper script that handles the directory automatically:

```bash
# From anywhere, run:
./run_scanner.sh --target example.com --headers
```

### Solution 3: Install as a Package

Install the package so it works from anywhere:

```bash
cd /Users/sumitsulabh/HealBot
pip3 install -e .
```

Then you can run from anywhere:
```bash
python3 -m nexvuln.scanner --target example.com --headers
```

### Solution 4: Add to Python Path

Add the HealBot directory to PYTHONPATH:

```bash
export PYTHONPATH="/Users/sumitsulabh/HealBot:$PYTHONPATH"
python3 -m nexvuln.scanner --target example.com --headers
```

## Quick Check

To verify you're in the right place:

```bash
# Should show: /Users/sumitsulabh/HealBot
pwd

# Should show: nexvuln/ directory exists
ls -d nexvuln
```

## Recommended Approach

**Always run from `/Users/sumitsulabh/HealBot` directory:**

```bash
cd /Users/sumitsulabh/HealBot
python3 -m nexvuln.scanner --target example.com --headers
```

Or use the wrapper script:
```bash
/Users/sumitsulabh/HealBot/run_scanner.sh --target example.com --headers
```

