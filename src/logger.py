"""
Logging utility for TB Global Analysis project.
Provides consistent logging across all modules.
"""

import logging
import sys
from pathlib import Path

from config import LOG_LEVEL, LOG_FILE


def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if setup is called multiple times
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    simple_formatter = logging.Formatter("%(levelname)s: %(message)s")
    
    # File handler
    try:
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not set up file logging: {e}")
    
    # Console handler (INFO level and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    return logger
