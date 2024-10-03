import argparse
import logging
from pathlib import Path

from utils.logging_setup import setup_logging
from data_services.download_service import (
    get_available_languages,
    download_language_dataset,
)
from utils.file_manager import ensure_directory_exists, delete_directory_if_exists
from utils.constants import BYTES_PER_GB

setup_logging()


def download_languages(languages: list[str], size: float, destination: str, zips_dir: str) -> None:
    """Download language datasets and extract them."""
    max_bytes = int(size * BYTES_PER_GB)
    zips_path = Path(zips_dir)
    ensure_directory_exists(zips_path)

    for language in languages:
        logging.info(f"Downloading dataset for language: {language}")
        try:
            extract_path = download_language_dataset(language, max_bytes, zips_path, Path(destination))
            if extract_path is None:
                continue
        except Exception as e:
            logging.error(f"Error downloading language {language}: {e}")
            continue

    logging.info("Download and extraction completed.")


def main():
    parser = argparse.ArgumentParser(description="Download and extract Mozilla Common Voice datasets.")
    parser.add_argument("--languages", nargs="+", help="List of languages to download")
    parser.add_argument("--size", type=float, help="Maximum size of the dataset to download in GB")
    parser.add_argument("--destination", type=str, default="data/raw", help="Path to save downloaded and extracted data")
    parser.add_argument("--zips-dir", type=str, default="data/zips", help="Path for storing zip files during download")
    parser.add_argument("--list-languages", action="store_true", help="List available languages from Common Voice API")
    parser.add_argument("--clean-zips", action="store_true", help="Delete zip directory after download")

    args = parser.parse_args()

    if args.list_languages:
        available_languages = get_available_languages()
        print("Available languages:")
        for symbol, name in available_languages.items():
            print(f"{symbol}: {name}")
        return

    if not args.list_languages:
        if not args.languages:
            parser.error("The --languages argument is required unless --list-languages is specified.")
        if not args.size:
            parser.error("The --size argument is required unless --list-languages is specified.")

    if args.languages and args.size:
        download_languages(args.languages, args.size, args.destination, args.zips_dir)

    if args.clean_zips:
        delete_directory_if_exists(Path(args.zips_dir))


if __name__ == "__main__":
    main()

