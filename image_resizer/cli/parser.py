"""Command line interface parser."""

import argparse
from typing import Any, Dict, List, Optional
from pathlib import Path

from ..utils.size_parser import SizeParser
from ..core import ProcessingMode


class CLIParser:
    """Command line argument parser for image resizer"""
    
    def __init__(self):
        self.parser = self._create_parser()
        self.size_parser = SizeParser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser with subcommands"""
        parser = argparse.ArgumentParser(
            description='Resize images to target file size using quality or DPI adjustment',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''Examples:
  Size mode (adjust quality):
    %(prog)s size input.jpg 500KB
    %(prog)s size *.jpg 1MB --suffix _resized
  
  DPI mode (adjust DPI):  
    %(prog)s dpi photo.jpg 2MB
    %(prog)s dpi images/ 800KB --output resized/
            '''
        )
        
        # Global arguments
        parser.add_argument('--no-progress', action='store_true',
                          help='Disable progress bar')
        parser.add_argument('--verbose', '-v', action='store_true',
                          help='Verbose output')
        
        # Create subparsers
        subparsers = parser.add_subparsers(dest='mode', help='Processing mode')
        
        # Size mode subcommand
        size_parser = subparsers.add_parser(
            'size', help='Adjust image quality to reach target size',
            description='Resize images by adjusting quality (JPEG, WebP only)'
        )
        self._add_common_args(size_parser)
        
        # DPI mode subcommand  
        dpi_parser = subparsers.add_parser(
            'dpi', help='Adjust image DPI to reach target size',
            description='Resize images by adjusting DPI (all formats)'
        )
        self._add_common_args(dpi_parser)
        
        return parser
    
    def _add_common_args(self, parser: argparse.ArgumentParser):
        """Add common arguments to a subparser"""
        parser.add_argument('input', 
                          help='Input image file, directory, or glob pattern')
        parser.add_argument('target_size',
                          help='Target file size (e.g., 500KB, 1.2MB, 2048)')
        parser.add_argument('--output', '-o',
                          help='Output directory (default: same as input)')
        parser.add_argument('--suffix',
                          help='Suffix to add to output filenames')
        parser.add_argument('--overwrite', action='store_true',
                          help='Overwrite existing output files')
    
    def parse_args(self, args: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Parse command line arguments and return configuration
        
        Args:
            args: List of arguments (None for sys.argv)
            
        Returns:
            Dictionary with parsed configuration
        """
        parsed = self.parser.parse_args(args)
        
        if parsed.mode is None:
            self.parser.error("Must specify processing mode (size or dpi)")
        
        # Parse processing mode
        mode = ProcessingMode.SIZE if parsed.mode == 'size' else ProcessingMode.DPI
        
        # Parse target size
        try:
            target_bytes = self.size_parser.parse(parsed.target_size)
        except ValueError as e:
            self.parser.error(f"Invalid target size: {e}")
        
        # Resolve input paths
        input_paths = self._resolve_input_paths(parsed.input)
        if not input_paths:
            self.parser.error(f"No input files found: {parsed.input}")
        
        # Determine output directory
        output_dir = Path(parsed.output) if parsed.output else None
        
        return {
            'mode': mode,
            'target_bytes': target_bytes,
            'input_paths': input_paths,
            'output_dir': output_dir,
            'suffix': parsed.suffix,
            'overwrite': parsed.overwrite,
            'show_progress': not parsed.no_progress,
            'verbose': parsed.verbose
        }
    
    def _resolve_input_paths(self, input_arg: str) -> List[Path]:
        """
        Resolve input argument to list of image file paths
        
        Args:
            input_arg: Input file, directory, or glob pattern
            
        Returns:
            List of Path objects for image files
        """
        input_path = Path(input_arg)
        paths = []
        
        # Supported image extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.tiff', '.tif'}
        
        if input_path.is_file():
            # Single file
            if input_path.suffix.lower() in image_extensions:
                paths.append(input_path)
        elif input_path.is_dir():
            # Directory - find all image files
            for ext in image_extensions:
                paths.extend(input_path.glob(f"*{ext}"))
                paths.extend(input_path.glob(f"*{ext.upper()}"))
        else:
            # Glob pattern
            from glob import glob
            for match in glob(input_arg):
                match_path = Path(match)
                if match_path.is_file() and match_path.suffix.lower() in image_extensions:
                    paths.append(match_path)
        
        # Sort paths for consistent ordering
        return sorted(paths)
    
    def print_help(self):
        """Print help message"""
        self.parser.print_help()