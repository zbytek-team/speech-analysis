import logging
import tarfile
import shutil
import pandas as pd
from pathlib import Path


def extract_validated_and_clips_from_tar(file_path: Path, extract_path: Path):
    """Extract only the 'validated.tsv' and 'clips/' folder from a tar file."""
    logging.info(f"Starting extraction of tar file: {file_path}")
    with tarfile.open(file_path) as tar:
        for member in tar.getmembers():
            if member.isfile():
                if member.name.endswith("validated.tsv"):
                    member.name = "validated.tsv"
                    tar.extract(member, path=extract_path)
                elif "clips/" in member.name:
                    member.name = str(Path("clips") / Path(member.name).name)
                    tar.extract(member, path=extract_path)

    logging.info(f"Completed extraction of tar file: {file_path}")


def ensure_directory_exists(path: Path):
    """Create a directory if it doesn't exist."""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {path}")
    else:
        logging.debug(f"Directory already exists: {path}")


def delete_directory_if_exists(path: Path):
    """Delete a directory if it exists."""
    if path.exists():
        shutil.rmtree(path)
        logging.info(f"Removed directory: {path}")
    else:
        logging.debug(f"Directory does not exist: {path}")