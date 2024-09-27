import argparse
import logging
from pathlib import Path

from utils.logging_utils import setup_logging
from utils.file_utils import ensure_directory_exists, delete_directory_if_exists
from utils.data_download_utils import download_language_dataset
from utils.data_preprocessing_utils import preprocess_language_data
from utils.constants import BYTES_PER_GB, DEFAULT_SAVE_DIR

setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Download and preprocess speech data from Mozilla Common Voice.")
    parser.add_argument("--languages", nargs="+", required=True, help="List of languages to process")
    parser.add_argument("--size", type=float, required=True, help="Total size of data to download in GB")
    parser.add_argument("--save_path", type=str, default=DEFAULT_SAVE_DIR, help="Path to save processed data")
    parser.add_argument("--skip-download", action="store_true", help="Skip the downloading step")
    parser.add_argument("--skip-preprocess", action="store_true", help="Skip the preprocessing step")
    args = parser.parse_args()

    languages = args.languages
    size = args.size
    save_path = args.save_path
    skip_download = args.skip_download
    skip_preprocess = args.skip_preprocess

    max_bytes = int(size * BYTES_PER_GB)

    temp_path = Path(save_path) / "tmp"
    ensure_directory_exists(temp_path)

    if not skip_download:
        for language in languages:
            logging.info(f"Downloading data for language: {language}")
            try:
                extract_path = download_language_dataset(language, max_bytes, temp_path)
                if extract_path is None:
                    continue
            except Exception as e:
                logging.error(f"Error downloading language {language}: {e}")
                continue
    else:
        logging.info("Skipping download step as per the argument.")

    if not skip_preprocess:
        for language in languages:
            logging.info(f"Preprocessing data for language: {language}")
            try:
                extract_path = temp_path / language
                if not extract_path.exists():
                    logging.warning(f"No data found for language {language} in temporary directory.")
                    continue
                preprocess_language_data(language, extract_path, save_path)
                # Clean up the extracted data
                delete_directory_if_exists(extract_path)
            except Exception as e:
                logging.error(f"Error preprocessing language {language}: {e}")
                continue
    else:
        logging.info("Skipping preprocessing step as per the argument.")

    # Clean up temp directory if not skipping download
    if not skip_download:
        delete_directory_if_exists(temp_path)

if __name__ == "__main__":
    main()

