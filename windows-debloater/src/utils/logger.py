import os
import logging
import datetime
from pathlib import Path

def setup_logger():
    """
    Sets up logging configuration for the application.
    Creates logs in the 'logs' directory with timestamp in filename.
    Returns the configured logger.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create a timestamp for the log filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"debloater_{timestamp}.log"
    
    # Configure logger
    logger = logging.getLogger("DebloaterLogger")
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger