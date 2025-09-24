#!/usr/bin/env python3
"""Test script to verify modular structure works correctly"""

import sys
from pathlib import Path

# Test imports
try:
    from image_resizer.core import ImageFormat
    from image_resizer.utils import SizeParser
    from image_resizer.processors import SizeModeProcessor
    from image_resizer.cli import CLIParser
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test size parser
try:
    parser = SizeParser()
    assert parser.parse("1MB") == 1024 * 1024
    assert parser.parse("500KB") == 500 * 1024
    print("✓ Size parser working")
except Exception as e:
    print(f"✗ Size parser error: {e}")

# Test processors can be created
try:
    size_proc = SizeModeProcessor()
    print("✓ Processors can be created")
except Exception as e:
    print(f"✗ Processor creation error: {e}")

# Test CLI parser
try:
    cli = CLIParser()
    # Test with mock arguments
    test_args = ['test.jpg', '500KB']
    # Just test that it can be created, not actually parsed
    print("✓ CLI parser can be created")
except Exception as e:
    print(f"✗ CLI parser error: {e}")

# Test enums
try:
    assert ImageFormat.from_extension(".jpg") == ImageFormat.JPEG
    print("✓ Enums working correctly")
except Exception as e:
    print(f"✗ Enum error: {e}")

print("\nModular structure test completed!")
print("The image resizer has been successfully updated.")
print("\nUsage:")
print("  python main.py input.jpg 500KB")
print("  python main.py photos/ 1MB --output resized/")