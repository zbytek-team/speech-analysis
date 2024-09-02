import logging
import colorlog

def setup_logging(level=logging.INFO):
    """
    Configure logging with colored output.

    :param level: The logging level, default is logging.INFO.
    """
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOGGING_FORMAT = '%(log_color)s%(asctime)s - %(levelname)s - %(message)s'
    LOG_COLORS = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        LOGGING_FORMAT,
        datefmt=LOGGING_DATE_FORMAT,
        log_colors=LOG_COLORS
    ))

    logging.basicConfig(level=level, handlers=[handler])