"""
Logging configuration for the Experian API application
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Any

def setup_logging(debug: bool = False) -> logging.Logger:
    """
    Set up application logging with file and console handlers
    
    Args:
        debug: Whether to enable debug logging
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configure root logger
    logger = logging.getLogger('experian_api')
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # File handler for all logs
    log_file = os.path.join(logs_dir, f'experian_api_{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Error file handler
    error_file = os.path.join(logs_dir, f'experian_errors_{datetime.now().strftime("%Y%m%d")}.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_api_request(logger: logging.Logger, endpoint: str, params: Any) -> None:
    """Log API request details"""
    logger.info(f"API Request - Endpoint: {endpoint}")
    logger.debug(f"API Request - Parameters: {params}")

def log_api_response(logger: logging.Logger, endpoint: str, status_code: int, response_size: int) -> None:
    """Log API response details"""
    logger.info(f"API Response - Endpoint: {endpoint}, Status: {status_code}, Size: {response_size} bytes")

def log_experian_request(logger: logging.Logger, payload_size: int) -> None:
    """Log Experian API request"""
    logger.info(f"Experian API Request - Payload size: {payload_size} bytes")

def log_experian_response(logger: logging.Logger, status_code: int, response_size: int, processing_time: float) -> None:
    """Log Experian API response"""
    logger.info(f"Experian API Response - Status: {status_code}, Size: {response_size} bytes, Time: {processing_time:.2f}s")

def log_data_processing(logger: logging.Logger, stage: str, input_size: int, output_size: int) -> None:
    """Log data processing stages"""
    logger.debug(f"Data Processing - Stage: {stage}, Input: {input_size} items, Output: {output_size} items")

def log_error(logger: logging.Logger, error: Exception, context: str = "") -> None:
    """Log error with context"""
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)