#!/usr/bin/env python3
"""
Image Resizer - Intelligently resize images to achieve target file sizes

This tool resizes images to match your desired file size automatically.
It features two processing modes to handle different image types optimally:
- Size mode: Uses quality adjustment (best for JPEG, WebP, TIFF)  
- DPI mode: Uses DPI adjustment (works with all formats)

Usage:
    python main.py size input.jpg 500KB
    python main.py dpi photos/ 1MB --output resized/
"""

import sys
from pathlib import Path
from typing import List, Optional

from image_resizer.cli import CLIParser
from image_resizer.core import ProcessingMode
from image_resizer.processors import SizeModeProcessor, DpiModeProcessor
from image_resizer.utils.progress import get_progress_bar
from image_resizer.utils.file_utils import determine_output_path


def process_images(input_paths: List[Path], config: dict) -> None:
    """
    Process list of images according to configuration
    
    Args:
        input_paths: List of input image paths
        config: Configuration dictionary from CLI parser
    """
    # Create processor based on mode
    if config['mode'] == ProcessingMode.SIZE:
        processor = SizeModeProcessor()
        mode_name = "Size"
    else:
        processor = DpiModeProcessor()
        mode_name = "DPI"
    
    # Create output directory if specified
    if config['output_dir']:
        config['output_dir'].mkdir(parents=True, exist_ok=True)
    
    # Setup progress bar
    if config['show_progress']:
        input_iter = get_progress_bar(
            enumerate(input_paths), 
            desc=f"{mode_name} Mode", 
            disable=False
        )
    else:
        input_iter = enumerate(input_paths)
    
    # Process images
    total_processed = 0
    total_success = 0
    total_input_size = 0
    total_output_size = 0
    
    for i, input_path in input_iter:
        # Determine output path with auto-increment (unless overwrite is enabled)
        output_path = determine_output_path(
            input_path, config['output_dir'], config['suffix'],
            auto_increment=config['auto_increment']
        )
        
        # Process image
        result = processor.process(input_path, output_path, config['target_bytes'])
        
        total_processed += 1
        if result.success:
            total_success += 1
        
        if result.input_size:
            total_input_size += result.input_size
        if result.output_size:
            total_output_size += result.output_size
        
        # Print result
        if config['verbose'] or not result.success:
            print(f"{input_path.name}: {result.message}")
    
    # Print summary
    if total_processed > 0:
        success_rate = (total_success / total_processed) * 100
        print(f"\nSummary:")
        print(f"  Mode: {mode_name}")
        print(f"  Processed: {total_processed} images")
        print(f"  Success: {total_success} ({success_rate:.1f}%)")
        
        if total_input_size > 0 and total_output_size > 0:
            reduction = ((total_input_size - total_output_size) / total_input_size) * 100
            print(f"  Total input size: {total_input_size:,} bytes")
            print(f"  Total output size: {total_output_size:,} bytes")
            print(f"  Size reduction: {reduction:.1f}%")


def main():
    """Main entry point"""
    try:
        # Parse command line arguments
        parser = CLIParser()
        config = parser.parse_args()
        
        # Process images
        process_images(config['input_paths'], config)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()