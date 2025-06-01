import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging format
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)

file_handler = RotatingFileHandler(
    log_dir / "app.log",
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setFormatter(log_format)

# Configure root logger
def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
