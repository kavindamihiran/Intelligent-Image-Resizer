"""Base processor class with common image processing functionality."""

import time
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from PIL import Image

from ..core import ImageFormat


class BaseImageProcessor:
    """Base class for image processors with common functionality"""
    
    def __init__(self, keep_metadata: bool = False):
        """
        Initialize BaseImageProcessor
        
        Args:
            keep_metadata: Whether to preserve image metadata (EXIF, etc.)
        """
        self.keep_metadata = keep_metadata
        
    def ensure_rgb_mode(self, image: Image.Image) -> Image.Image:
        """Ensure image is in RGB mode for saving to JPEG/WebP"""
        if image.mode in ("RGB", "RGBA", "L", "P"):
            if image.mode != "RGB":
                return image.convert("RGB")
        else:
            return image.convert("RGB")
        return image
    
    def get_save_params(self, image: Image.Image, format_type: ImageFormat, 
                       quality: int = 95, dpi: Optional[Tuple[int, int]] = None) -> Dict[str, Any]:
        """Get optimized save parameters for different image formats"""
        params: Dict[str, Any] = {}
        
        if format_type == ImageFormat.JPEG:
            params = {
                "format": "JPEG",
                "quality": quality,
                "optimize": True,
                "progressive": True,
                "subsampling": "4:2:0"
            }
            if dpi:
                params["dpi"] = dpi
            if self.keep_metadata and "exif" in image.info:
                exif_data = image.info.get("exif")
                if exif_data:
                    params["exif"] = exif_data
                
        elif format_type == ImageFormat.WEBP:
            params = {
                "format": "WEBP",
                "quality": quality,
                "method": 6,
                "optimize": True
            }
            if self.keep_metadata:
                exif_data = image.info.get("exif")
                if exif_data:
                    params["exif"] = exif_data
                icc_profile = image.info.get("icc_profile")
                if icc_profile:
                    params["icc_profile"] = icc_profile
                    
        elif format_type == ImageFormat.PNG:
            params = {
                "format": "PNG",
                "optimize": True
            }
            if dpi:
                params["dpi"] = dpi
            if self.keep_metadata:
                icc_profile = image.info.get("icc_profile")
                if icc_profile:
                    params["icc_profile"] = icc_profile
                
        elif format_type == ImageFormat.TIFF:
            params = {
                "format": "TIFF",
                "compression": "tiff_deflate"
            }
            if dpi:
                params["dpi"] = dpi
            if self.keep_metadata:
                icc_profile = image.info.get("icc_profile")
                if icc_profile:
                    params["icc_profile"] = icc_profile
        
        return params
    
    def save_image_with_params(self, image: Image.Image, output_path: Path, 
                              format_type: ImageFormat, quality: int = 95, 
                              dpi: Optional[Tuple[int, int]] = None) -> int:
        """
        Save image with specified parameters and return file size
        
        Args:
            image: PIL Image object
            output_path: Path to save the image
            format_type: Target image format
            quality: Quality setting for compressible formats
            dpi: DPI tuple for formats that support it
            
        Returns:
            File size in bytes
        """
        params = self.get_save_params(image, format_type, quality, dpi)
        
        # Ensure proper mode for compressible formats
        if format_type in [ImageFormat.JPEG, ImageFormat.WEBP]:
            processed_image = self.ensure_rgb_mode(image)
        else:
            processed_image = image
            
        processed_image.save(output_path, **params)
        return output_path.stat().st_size