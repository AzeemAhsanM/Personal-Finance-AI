import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

# Configure logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# File handler (rotating logs)
file_handler = RotatingFileHandler(
    "logs/app.log", maxBytes=5_000_000, backupCount=3
)
file_handler.setFormatter(formatter)

# Stream handler (console)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Add handlers only once
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
