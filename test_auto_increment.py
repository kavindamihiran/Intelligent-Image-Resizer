#!/usr/bin/env python3
"""Test script demonstrating auto-increment functionality"""

import subprocess
import sys
from pathlib import Path

def run_resize_command(target_size, suffix="", mode="size"):
    """Run the image resizer and return the result"""
    cmd = [sys.executable, "main.py", mode, "test.jpg", target_size, "--verbose"]
    if suffix:
        cmd.extend(["--suffix", suffix])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def main():
    """Test the auto-increment functionality"""
    print("Testing Auto-Increment Functionality")
    print("=" * 40)
    
    # Test basic auto-increment
    print("\n1. Testing basic auto-increment with default suffix:")
    for i, size in enumerate(["45KB", "48KB", "52KB"], 1):
        stdout, stderr, code = run_resize_command(size)
        if code == 0:
            print(f"   Run {i}: Target {size} - SUCCESS")
        else:
            print(f"   Run {i}: Target {size} - FAILED")
            print(f"   Error: {stderr}")
    
    # Test custom suffix auto-increment  
    print("\n2. Testing auto-increment with custom suffix '_small':")
    for i, size in enumerate(["35KB", "38KB", "42KB"], 1):
        stdout, stderr, code = run_resize_command(size, "_small")
        if code == 0:
            print(f"   Run {i}: Target {size} - SUCCESS")
        else:
            print(f"   Run {i}: Target {size} - FAILED")
            print(f"   Error: {stderr}")
    
    # Test DPI mode
    print("\n3. Testing DPI mode auto-increment:")
    for i, size in enumerate(["25KB", "28KB", "32KB"], 1):
        stdout, stderr, code = run_resize_command(size, "", "dpi")
        if code == 0:
            print(f"   Run {i}: Target {size} - SUCCESS")
        else:
            print(f"   Run {i}: Target {size} - FAILED")
            print(f"   Error: {stderr}")
    
    # List all created files
    print("\n4. Created files:")
    for file_path in sorted(Path(".").glob("test_*.jpg")):
        size = file_path.stat().st_size
        print(f"   {file_path.name}: {size:,} bytes")

if __name__ == "__main__":
    main()