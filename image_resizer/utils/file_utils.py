"""File handling utilities for image processing."""

from pathlib import Path
from typing import Optional


def generate_unique_filename(base_path: Path, max_attempts: int = 1000) -> Path:
    """
    Generate a unique filename by adding numeric suffix if file exists.
    
    This function ensures that multiple resize operations won't overwrite 
    existing files by automatically incrementing a numeric suffix.
    
    Args:
        base_path: The desired output path
        max_attempts: Maximum number of attempts to find unique name
        
    Returns:
        Path object with unique filename
        
    Examples:
        If 'image_resized.jpg' exists:
        - First call returns 'image_resized_1.jpg'
        - Second call returns 'image_resized_2.jpg'
        - And so on...
    """
    if not base_path.exists():
        return base_path
    
    # Extract components
    parent = base_path.parent
    stem = base_path.stem
    suffix = base_path.suffix
    
    # Try numbered variations
    for i in range(1, max_attempts + 1):
        new_name = f"{stem}_{i}{suffix}"
        new_path = parent / new_name
        
        if not new_path.exists():
            return new_path
    
    # If all attempts failed, use timestamp-based name
    import time
    timestamp = str(int(time.time() * 1000))
    fallback_name = f"{stem}_{timestamp}{suffix}"
    return parent / fallback_name


def determine_output_path(input_path: Path, output_dir: Optional[Path] = None, 
                         suffix: Optional[str] = None, 
                         auto_increment: bool = True) -> Path:
    """
    Determine output path for processed image with optional auto-increment.
    
    Args:
        input_path: Original image path
        output_dir: Output directory (None for same as input)  
        suffix: Suffix to add to filename
        auto_increment: Whether to auto-increment if file exists
        
    Returns:
        Path object for output file (guaranteed unique if auto_increment=True)
    """
    if output_dir:
        # Use specified output directory
        filename = input_path.name
        if suffix:
            name_part = input_path.stem
            ext_part = input_path.suffix
            filename = f"{name_part}{suffix}{ext_part}"
        base_path = output_dir / filename
    else:
        # Use same directory as input
        if suffix:
            name_part = input_path.stem
            ext_part = input_path.suffix
            base_path = input_path.parent / f"{name_part}{suffix}{ext_part}"
        else:
            base_path = input_path
    
    # Apply auto-increment if requested
    if auto_increment:
        return generate_unique_filename(base_path)
    else:
        return base_path