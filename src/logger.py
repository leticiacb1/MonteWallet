import logging


def get_logger(name: str) -> logging.Logger:
    """
    Create and configure a simple logger that outputs messages to the console.

    The logger will display messages at DEBUG, INFO, WARNING, ERROR, and CRITICAL
    levels using the format: [LEVEL] message.

    Parameters
    ----------
    name : str
        Name of the logger (currently not used, reserved for future customization).

    Returns
    -------
    logging.Logger
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
