"""Data models and result classes for the image resizer."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ResizeResult:
    """Result of an image resize operation"""
    success: bool
    message: str
    input_size: Optional[int] = None
    output_size: Optional[int] = None
    quality: Optional[int] = None
    processing_time: Optional[float] = None
    dpi: Optional[int] = None