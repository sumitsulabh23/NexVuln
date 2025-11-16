#!/bin/bash
# NexVuln Scanner Wrapper Script
# This script ensures you're in the correct directory and runs the scanner

cd "$(dirname "$0")" || exit 1

# Suppress urllib3 warnings
export PYTHONWARNINGS=ignore

# Run the scanner
python3 -m nexvuln.scanner "$@"

