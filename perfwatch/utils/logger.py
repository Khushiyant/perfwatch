import logging
import os
from logging.handlers import RotatingFileHandler

import dotenv

dotenv.load_dotenv()


def get_logger(name: str, file_path: str = None) -> logging.Logger:
    """
    Get a logger instance with the specified name and optional file path.

    Args:
        name (str): The name of the logger.
        file_path (str, optional): The file path to save the log messages. If not provided, log messages will be printed to the console.

    Returns:
        logging.Logger: The logger instance.

    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    if file_path:
        # Use a RotatingFileHandler to rotate the log file when it reaches 10MB
        file_handler = RotatingFileHandler(
            file_path, maxBytes=10 * 1024 * 1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = get_logger("perfai", file_path=os.getenv("LOG_FILE_PATH", None))
