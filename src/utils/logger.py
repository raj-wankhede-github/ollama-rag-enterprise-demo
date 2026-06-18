"""
Logging configuration for the application.
"""

import logging
import sys
from typing import Optional


class Logger:
    """Custom logger wrapper"""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
        """Get or create a logger with the given name"""
        if name in Logger._loggers:
            return Logger._loggers[name]
        
        logger = logging.getLogger(name)
        
        # Set level
        log_level = level or "INFO"
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, log_level.upper()))
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
        
        Logger._loggers[name] = logger
        return logger


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Convenience function to get logger"""
    return Logger.get_logger(name, level)
