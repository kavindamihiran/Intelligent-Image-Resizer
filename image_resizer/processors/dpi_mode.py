"""DPI mode processor for DPI-based file size targeting."""

import time
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image

from .base import BaseImageProcessor  
from ..core import ImageFormat, ResizeResult


class DpiModeProcessor(BaseImageProcessor):
    """Processor for DPI mode - adjust DPI to reach target file size"""
    
    def binary_search_dpi(self, image: Image.Image, output_path: Path,
                         target_bytes: int, format_type: ImageFormat,
                         min_dpi: int = 25, max_dpi: int = 600,
                         tolerance: float = 0.05) -> Tuple[Optional[int], int]:
        """
        Use binary search to find optimal DPI for target file size
        
        Args:
            image: PIL Image object
            output_path: Path for output file
            target_bytes: Target file size in bytes  
            format_type: Image format enum
            min_dpi: Minimum DPI to try
            max_dpi: Maximum DPI to try
            tolerance: Acceptable tolerance as ratio of target size
        
        Returns:
            Tuple of (optimal_dpi, achieved_size)
            optimal_dpi is None if target cannot be achieved
        """
        def try_dpi(dpi: int) -> int:
            """Try saving with given DPI and return file size"""
            temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
            try:
                # Clone image and set DPI
                img_copy = image.copy()
                img_copy.info['dpi'] = (dpi, dpi)
                
                return self.save_image_with_params(img_copy, temp_path, format_type)
            finally:
                temp_path.unlink(missing_ok=True)
        
        # Quick boundary checks
        min_size = try_dpi(min_dpi)
        if min_size >= target_bytes:
            return min_dpi, min_size
            
        max_size = try_dpi(max_dpi)
        if max_size <= target_bytes:
            return max_dpi, max_size
        
        # Binary search
        low, high = min_dpi, max_dpi
        best_dpi, best_size = None, None
        tolerance_bytes = max(1, int(target_bytes * tolerance))
        
        while low <= high:
            mid = (low + high) // 2
            size = try_dpi(mid)
            
            if size <= target_bytes:
                best_dpi, best_size = mid, size
                # Try higher DPI while staying under target
                low = mid + 1
                
                # Check if we're close enough to target
                if target_bytes - size <= tolerance_bytes:
                    break
            else:
                high = mid - 1
        
        return best_dpi, best_size or max_size
    
    def process(self, input_path: Path, output_path: Path,
               target_bytes: int) -> ResizeResult:
        """
        Process image in DPI mode - adjust DPI to reach target file size
        
        Args:
            input_path: Path to input image
            output_path: Path for output image
            target_bytes: Target file size in bytes
        
        Returns:
            ResizeResult with operation details
        """
        start_time = time.time()
        
        # Validate output format  
        output_format = ImageFormat.from_extension(output_path.suffix)
        if not output_format:
            return ResizeResult(
                success=False,
                message=f"Unsupported output format: {output_path.suffix}",
                processing_time=time.time() - start_time
            )
        
        try:
            # Load image
            with Image.open(input_path) as image:
                input_size = input_path.stat().st_size
                
                # Get current DPI if available
                current_dpi = getattr(image, 'info', {}).get('dpi', (72, 72))[0]
                
                # Find optimal DPI
                dpi, output_size = self.binary_search_dpi(
                    image, output_path, target_bytes, output_format
                )
                
                if dpi is None:
                    # Save at maximum DPI as best effort
                    img_copy = image.copy()
                    img_copy.info['dpi'] = (600, 600)
                    actual_size = self.save_image_with_params(
                        img_copy, output_path, output_format
                    )
                    
                    return ResizeResult(
                        success=False,
                        message=f"Cannot reach {target_bytes:,} bytes. Best effort: {actual_size:,} bytes at 600 DPI",
                        input_size=input_size,
                        output_size=actual_size, 
                        dpi=600,
                        processing_time=time.time() - start_time
                    )
                
                # Save with optimal DPI
                img_copy = image.copy()
                img_copy.info['dpi'] = (dpi, dpi)
                actual_size = self.save_image_with_params(
                    img_copy, output_path, output_format
                )
                
                return ResizeResult(
                    success=True,
                    message=f"Success: {actual_size:,} bytes (target: {target_bytes:,}) at {dpi} DPI (was {current_dpi} DPI)",
                    input_size=input_size,
                    output_size=actual_size,
                    dpi=dpi,
                    processing_time=time.time() - start_time
                )
                
        except Exception as e:
            return ResizeResult(
                success=False,
                message=f"Error processing {input_path.name}: {str(e)}",
                processing_time=time.time() - start_time
            )