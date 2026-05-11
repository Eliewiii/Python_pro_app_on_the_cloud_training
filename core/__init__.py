"""
Core algorithmic engine for the BUA framework.
"""

from .processor import FileProcessor

# Explicitly define what is available when someone imports 'core'
__all__ = ["FileProcessor"]
