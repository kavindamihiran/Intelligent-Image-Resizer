"""Progress bar utilities with optional tqdm support."""

# Optional progress bar - fallback if tqdm not available
try:
    from tqdm import tqdm as TqdmProgress
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    TqdmProgress = None


class SimpleTqdm:
    """Simple fallback progress indicator when tqdm is not available"""
    
    def __init__(self, iterable, desc="", disable=False):
        self.iterable = iterable
        self.desc = desc
        self.disable = disable
        self.n = 0
        self.total = len(iterable) if hasattr(iterable, '__len__') else None
        
    def __iter__(self):
        for item in self.iterable:
            yield item
            self.n += 1
            if not self.disable and self.total:
                percent = (self.n / self.total) * 100
                print(f"\r{self.desc}: {self.n}/{self.total} ({percent:.1f}%)", end="", flush=True)
        if not self.disable:
            print()  # New line after completion
            
    def set_description(self, desc):
        self.desc = desc
        
    def set_postfix_str(self, postfix):
        pass  # Simple fallback doesn't show postfix


def get_progress_bar(iterable, desc="", disable=False):
    """Get appropriate progress bar based on availability"""
    if HAS_TQDM and TqdmProgress:
        return TqdmProgress(iterable, desc=desc, disable=disable)
    else:
        return SimpleTqdm(iterable, desc=desc, disable=disable)