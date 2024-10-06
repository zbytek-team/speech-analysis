import logging
import colorlog
from pathlib import Path
from datetime import datetime

def setup_logging(level=logging.INFO):
    """Setup logging with color formatting."""
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOGGING_FORMAT = '%(log_color)s%(asctime)s - %(levelname)s - %(message)s'
    LOGGING_FORMAT_FILE = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_COLORS = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True) #creates dir if not exits

    current_date = datetime.now().strftime("%Y-%m-%d")

    LOGGING_FILENAME = log_dir / f'log_{current_date}.log'

    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(colorlog.ColoredFormatter(
        LOGGING_FORMAT,
        datefmt=LOGGING_DATE_FORMAT,
        log_colors=LOG_COLORS
    ))

    file_handler = logging.FileHandler(LOGGING_FILENAME)
    file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT_FILE))

    logging.basicConfig(level=level, handlers=[console_handler, file_handler])

