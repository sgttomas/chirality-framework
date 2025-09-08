"""
Logging utilities for Chirality Framework CLI.

Provides functions to properly separate logs (stderr) from data output (stdout).
"""

import sys
from typing import Any


def log_info(message: str) -> None:
    """
    Log informational message to stderr.
    
    Args:
        message: Message to log
    """
    print(message, file=sys.stderr)


def log_error(message: str) -> None:
    """
    Log error message to stderr.
    
    Args:
        message: Error message to log
    """
    print(f"❌ {message}", file=sys.stderr)


def log_success(message: str) -> None:
    """
    Log success message to stderr.
    
    Args:
        message: Success message to log  
    """
    print(f"✓ {message}", file=sys.stderr)


def log_progress(message: str) -> None:
    """
    Log progress message to stderr.
    
    Args:
        message: Progress message to log
    """
    print(f"🔄 {message}", file=sys.stderr)


def output_data(data: Any) -> None:
    """
    Output data to stdout for consumption by other tools.
    
    Args:
        data: Data to output (will be converted to string)
    """
    print(data, file=sys.stdout)


def log_with_prefix(prefix: str, message: str) -> None:
    """
    Log message with custom prefix to stderr.
    
    Args:
        prefix: Prefix for the message
        message: Message content
    """
    print(f"{prefix} {message}", file=sys.stderr)


def log_stats(stats: dict, prefix: str = "  -") -> None:
    """
    Log statistics dictionary to stderr with consistent formatting.
    
    Args:
        stats: Dictionary of statistics to log
        prefix: Prefix for each stat line
    """
    for key, value in stats.items():
        print(f"{prefix} {key}: {value}", file=sys.stderr)