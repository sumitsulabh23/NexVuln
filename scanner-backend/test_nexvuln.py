#!/usr/bin/env python3
"""
Quick test script for NexVuln scanner.
Tests each module individually to verify installation.
"""

import sys
import subprocess
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    try:
        import nmap
        print("  ✅ python-nmap")
    except ImportError as e:
        print(f"  ❌ python-nmap: {e}")
        return False
    
    try:
        import requests
        print("  ✅ requests")
    except ImportError as e:
        print(f"  ❌ requests: {e}")
        return False
    
    try:
        import rich
        print("  ✅ rich")
    except ImportError as e:
        print(f"  ❌ rich: {e}")
        return False
    
    try:
        from nexvuln import port_scanner, header_scanner, ssl_scanner, directory_scanner, utils
        print("  ✅ nexvuln modules")
    except ImportError as e:
        print(f"  ❌ nexvuln modules: {e}")
        return False
    
    return True

def test_nmap_installed():
    """Check if nmap is installed on system."""
    print("\n🔍 Checking Nmap installation...")
    result = subprocess.run(['which', 'nmap'], capture_output=True, text=True)
    if result.returncode == 0:
        nmap_path = result.stdout.strip()
        print(f"  ✅ Nmap found at: {nmap_path}")
        # Get version
        version_result = subprocess.run(['nmap', '--version'], capture_output=True, text=True)
        if version_result.returncode == 0:
            version_line = version_result.stdout.split('\n')[0]
            print(f"  📋 {version_line}")
        return True
    else:
        print("  ❌ Nmap not found in PATH")
        print("  💡 Install with: brew install nmap (macOS) or sudo apt-get install nmap (Linux)")
        return False

def test_basic_functionality():
    """Test basic scanner functionality."""
    print("\n🔍 Testing basic functionality...")
    
    try:
        from nexvuln.utils import validate_target, normalize_url
        from nexvuln.header_scanner import HeaderScanner
        from nexvuln.directory_scanner import DirectoryScanner
        
        # Test URL validation
        is_valid, host, port = validate_target("example.com")
        if is_valid:
            print(f"  ✅ URL validation works (example.com -> {host}:{port})")
        else:
            print("  ❌ URL validation failed")
            return False
        
        # Test header scanner initialization
        header_scanner = HeaderScanner()
        print("  ✅ HeaderScanner initialized")
        
        # Test directory scanner initialization
        dir_scanner = DirectoryScanner()
        print(f"  ✅ DirectoryScanner initialized (wordlist: {len(dir_scanner.wordlist)} entries)")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def run_quick_test_scan():
    """Run a quick test scan on a safe target."""
    print("\n🔍 Running quick test scan...")
    print("  ℹ️  Testing on scanme.nmap.org (authorized for testing)")
    
    try:
        # Test header scan (fastest and doesn't require nmap)
        from nexvuln.header_scanner import HeaderScanner
        
        scanner = HeaderScanner()
        print("  📡 Scanning HTTP headers on scanme.nmap.org...")
        results = scanner.scan("http://scanme.nmap.org")
        
        if results:
            print(f"  ✅ Header scan completed ({len(results)} headers checked)")
            return True
        else:
            print("  ⚠️  Header scan returned no results")
            return False
    except Exception as e:
        print(f"  ❌ Test scan failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 NexVuln Scanner - Installation Test")
    print("=" * 60)
    
    all_passed = True
    
    # Test 1: Imports
    if not test_imports():
        all_passed = False
    
    # Test 2: Nmap
    nmap_installed = test_nmap_installed()
    if not nmap_installed:
        all_passed = False
    
    # Test 3: Basic functionality
    if not test_basic_functionality():
        all_passed = False
    
    # Test 4: Quick scan (only if basic tests pass)
    if all_passed:
        if not run_quick_test_scan():
            print("  ⚠️  Test scan had issues, but basic functionality works")
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ All tests passed! NexVuln is ready to use.")
        print("\n📝 Quick start:")
        print("   python3 -m nexvuln.scanner --target example.com --headers")
        print("   python3 -m nexvuln.scanner --target example.com --full-scan")
    else:
        print("⚠️  Some tests failed. Please install missing dependencies:")
        print("   pip3 install -r requirements.txt")
        if not nmap_installed:
            print("   brew install nmap  # macOS")
            print("   sudo apt-get install nmap  # Linux")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())

