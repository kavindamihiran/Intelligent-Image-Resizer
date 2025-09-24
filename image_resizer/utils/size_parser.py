"""Size parsing utilities for human-readable file sizes."""

import re


class SizeParser:
    """Parser for human-readable file sizes"""
    
    SIZE_UNITS = {
        'b': 1,
        'k': 1024, 'kb': 1024,
        'm': 1024**2, 'mb': 1024**2,
        'g': 1024**3, 'gb': 1024**3,
        't': 1024**4, 'tb': 1024**4
    }
    
    @classmethod
    def parse(cls, size_text: str) -> int:
        """
        Parse human-readable sizes like: 200KB, 1.5MB, 123456, 2m, 500k
        Returns size in bytes as integer
        
        Examples:
            parse("500KB") -> 512000
            parse("1.5MB") -> 1572864
            parse("100000") -> 100000
        """
        text = size_text.strip().lower().replace(" ", "")
        
        # Match number with optional decimal point and unit
        pattern = r"^([0-9]*\.?[0-9]+)\s*([kmgtb]*)?$"
        match = re.match(pattern, text)
        
        if not match:
            raise ValueError(f"Invalid size format: '{size_text}'. Use formats like '500KB', '1.5MB', or '100000'")
        
        number = float(match.group(1))
        unit = match.group(2) or 'b'
        
        if unit not in cls.SIZE_UNITS:
            raise ValueError(f"Unsupported unit: '{unit}'. Supported units: {', '.join(cls.SIZE_UNITS.keys())}")
        
        return int(number * cls.SIZE_UNITS[unit])