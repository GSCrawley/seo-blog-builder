"""
Logger utility for the SEO Blog Builder application.
"""
import os
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import settings

def setup_logging(
    log_level=logging.INFO,
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_file_path=None,
    max_file_size=10485760,  # 10MB
    backup_count=5
):
    """
    Set up logging for the application.
    
    Args:
        log_level: Logging level (default: INFO)
        log_format: Format string for log messages
        log_file_path: Path to log file (default: logs/app.log)
        max_file_size: Maximum size of log file before rotation
        backup_count: Number of backup log files to keep
    """
    # Create logs directory if it doesn't exist
    if log_file_path is None:
        logs_dir = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) / "logs"
        os.makedirs(logs_dir, exist_ok=True)
        log_file_path = logs_dir / "app.log"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Configure file handler with rotation
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=max_file_size,
        backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Set specific log levels for some noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    # Log the app startup
    root_logger.info(f"Logging initialized. Level: {logging.getLevelName(log_level)}")
    root_logger.info(f"Environment: {settings.APP_ENV}")

def get_logger(name):
    """
    Get a logger for a specific module.
    
    Args:
        name: Name of the module
        
    Returns:
        Logger: Configured logger instance
    """
    return logging.getLogger(name)
