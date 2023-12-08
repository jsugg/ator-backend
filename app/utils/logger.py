import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name, log_file, level=logging.INFO):
    """
    Sets up a logger with a rotating file handler.

    Args:
        name (str): Name of the logger.
        log_file (str): File path for the log file.
        level (int): Logging level.

    Returns:
        logging.Logger: Configured logger instance.
    """

    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    
    handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=3)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Example usage: Creating a logger for the authentication module
auth_logger = setup_logger('auth', 'logs/auth.log')
