import logging
import shutil
from pathlib import Path

def ensure_directory_exists(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {path}")
    else:
        logging.debug(f"Directory already exists: {path}")

def delete_directory_if_exists(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
        logging.info(f"Removed directory: {path}")
    else:
        logging.debug(f"Directory does not exist: {path}")
