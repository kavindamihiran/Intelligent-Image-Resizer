"""Core enums and constants for the image resizer."""

from enum import Enum


class ProcessingMode(Enum):
    """Enumeration of available processing modes"""
    SIZE = "size"
    DPI = "dpi"


class ImageFormat(Enum):
    """Supported image formats with their properties"""
    JPEG = (".jpg", ".jpeg")
    PNG = (".png",)
    WEBP = (".webp",)
    TIFF = (".tiff", ".tif")
    
    @classmethod
    def from_extension(cls, ext: str) -> 'ImageFormat | None':
        """Get ImageFormat from file extension"""
        ext = ext.lower()
        for fmt in cls:
            if ext in fmt.value:
                return fmt
        return None
    
    @classmethod
    def get_supported_extensions(cls) -> set:
        """Get all supported file extensions"""
        extensions = set()
        for fmt in cls:
            extensions.update(fmt.value)
        return extensions


# Format support by processing mode
SIZE_MODE_FORMATS = {ImageFormat.JPEG, ImageFormat.WEBP}
DPI_MODE_FORMATS = {ImageFormat.JPEG, ImageFormat.PNG, ImageFormat.WEBP, ImageFormat.TIFF}