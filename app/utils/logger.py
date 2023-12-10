import sys
import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    Sets up a logger with a rotating file handler.

    Args:
        name (str): Name of the logger.
        log_file (str): File path for the log file.
        level (int): Logging level.

    Returns:
        logging.Logger: Configured logger instance.
    """

    try:
        formatter: logging.Formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        handler: RotatingFileHandler = RotatingFileHandler(
            log_file, maxBytes=10000, backupCount=3)
        handler.setFormatter(formatter)

        logger: logging.Logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    except Exception as err:
        print(f"Error setting up logger: {err}")
        sys.exit(1)


# Creating loggers for different modules
app_logger: logging.Logger = setup_logger('app_logger', 'logs/app.log')
auth_logger: logging.Logger = setup_logger('auth', 'logs/auth.log')
api_logger: logging.Logger = setup_logger('api', 'logs/api.log')
db_logger: logging.Logger = setup_logger('db', 'logs/db.log')
service_logger: logging.Logger = setup_logger('service', 'logs/service.log')
