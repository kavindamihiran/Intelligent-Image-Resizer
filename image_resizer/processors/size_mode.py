"""Size mode processor for quality-based file size targeting."""

import time
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image

from .base import BaseImageProcessor
from ..core import ImageFormat, SIZE_MODE_FORMATS, ResizeResult


class SizeModeProcessor(BaseImageProcessor):
    """Processor for size mode - adjust quality to reach target file size"""
    
    def binary_search_quality(self, image: Image.Image, output_path: Path,
                            target_bytes: int, format_type: ImageFormat,
                            min_quality: int = 10, max_quality: int = 95,
                            tolerance: float = 0.05) -> Tuple[Optional[int], int]:
        """
        Use binary search to find optimal quality for target file size
        
        Args:
            image: PIL Image object
            output_path: Path for output file
            target_bytes: Target file size in bytes
            format_type: Image format enum
            min_quality: Minimum quality to try
            max_quality: Maximum quality to try  
            tolerance: Acceptable tolerance as ratio of target size
        
        Returns:
            Tuple of (optimal_quality, achieved_size)
            optimal_quality is None if target cannot be achieved
        """
        def try_quality(quality: int) -> int:
            """Try saving with given quality and return file size"""
            temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
            try:
                return self.save_image_with_params(image, temp_path, format_type, quality)
            finally:
                temp_path.unlink(missing_ok=True)
        
        # Quick boundary checks
        max_size = try_quality(max_quality)
        if max_size <= target_bytes:
            return max_quality, max_size
            
        min_size = try_quality(min_quality)
        if min_size > target_bytes:
            return None, min_size
        
        # Binary search
        low, high = min_quality, max_quality
        best_quality, best_size = None, None
        tolerance_bytes = max(1, int(target_bytes * tolerance))
        
        while low <= high:
            mid = (low + high) // 2
            size = try_quality(mid)
            
            if size <= target_bytes:
                best_quality, best_size = mid, size
                # Try higher quality while staying under target
                low = mid + 1
                
                # Check if we're close enough to target
                if target_bytes - size <= tolerance_bytes:
                    break
            else:
                high = mid - 1
        
        return best_quality, best_size or min_size
    
    def process(self, input_path: Path, output_path: Path, 
               target_bytes: int) -> ResizeResult:
        """
        Process image in size mode - adjust quality to reach target file size
        
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
        if not output_format or output_format not in SIZE_MODE_FORMATS:
            supported = [fmt.value[0] for fmt in SIZE_MODE_FORMATS]
            return ResizeResult(
                success=False,
                message=f"Size mode only supports {supported}. Got: {output_path.suffix}",
                processing_time=time.time() - start_time
            )
        
        try:
            # Load image
            with Image.open(input_path) as image:
                input_size = input_path.stat().st_size
                
                # Find optimal quality
                quality, output_size = self.binary_search_quality(
                    image, output_path, target_bytes, output_format
                )
                
                if quality is None:
                    # Save at minimum quality as best effort
                    actual_size = self.save_image_with_params(
                        image, output_path, output_format, 10
                    )
                    
                    return ResizeResult(
                        success=False,
                        message=f"Cannot reach {target_bytes:,} bytes. Best effort: {actual_size:,} bytes at quality 10",
                        input_size=input_size,
                        output_size=actual_size,
                        quality=10,
                        processing_time=time.time() - start_time
                    )
                
                # Save with optimal quality
                actual_size = self.save_image_with_params(
                    image, output_path, output_format, quality
                )
                
                return ResizeResult(
                    success=True,
                    message=f"Success: {actual_size:,} bytes (target: {target_bytes:,}) at quality {quality}",
                    input_size=input_size,
                    output_size=actual_size,
                    quality=quality,
                    processing_time=time.time() - start_time
                )
                
        except Exception as e:
            return ResizeResult(
                success=False,
                message=f"Error processing {input_path.name}: {str(e)}",
                processing_time=time.time() - start_time
            )