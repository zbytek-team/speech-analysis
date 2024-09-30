import argparse
import logging
from pathlib import Path

from utils.logging_utils import setup_logging
from utils.file_utils import ensure_directory_exists, delete_directory_if_exists
from utils.data_download_utils import download_language_dataset, get_available_languages
from utils.data_preprocessing_utils import preprocess_language_data
from utils.constants import BYTES_PER_GB, DEFAULT_SAVE_DIR

setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Download and preprocess speech data from Mozilla Common Voice.")
    
    parser.add_argument("--languages", nargs="+", help="List of languages to process (or 'help' to list available languages)")
    parser.add_argument("--size", type=float, help="Total size of data to download in GB")
    parser.add_argument("--save-path", type=str, default=DEFAULT_SAVE_DIR, help="Path to save downloaded/preprocessed data")
    
    parser.add_argument("--skip-download", action="store_true", help="Skip the downloading step")
    parser.add_argument("--skip-preprocess", action="store_true", help="Skip the preprocessing step")
    parser.add_argument("--list-languages", action="store_true", help="List available languages without downloading or preprocessing")
    
    parser.add_argument("--download-path", type=str, help="Path to save the downloaded data (default is --save-path)")
    parser.add_argument("--preprocess-path", type=str, help="Path where preprocessed data is stored or should be processed (default is --save-path)")
    parser.add_argument("--clean-tmp", action="store_true", help="Delete the temporary folder after the process (default is not to delete)")
    
    args = parser.parse_args()

    if args.list_languages:
        available_languages = get_available_languages()
        print("Available languages:")
        for symbol, name in available_languages.items():
            print(f"{symbol}: {name}")
        return

    languages = args.languages
    size = args.size
    save_path = args.save_path
    download_path = args.download_path or save_path
    preprocess_path = args.preprocess_path or save_path
    skip_download = args.skip_download
    skip_preprocess = args.skip_preprocess
    clean_tmp = args.clean_tmp

    if not skip_download and (not languages or not size):
        parser.error("--languages and --size are required when downloading data.")
    
    max_bytes = int(size * BYTES_PER_GB) if size else 0
    temp_path = Path(save_path) / "tmp"
    ensure_directory_exists(temp_path)

    if not skip_download:
        available_languages = get_available_languages()

        if any(lang not in available_languages for lang in languages):
            print("Available languages:")
            for symbol, name in available_languages.items():
                print(f"{symbol}: {name}")
        else:
            for language in languages:
                logging.info(f"Downloading data for language: {language}")
                try:
                    extract_path = download_language_dataset(language, max_bytes, Path(download_path) / "tmp")
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
                extract_path = Path(temp_path) / language
                if not extract_path.exists():
                    logging.warning(f"No data found for language {language} in temporary directory.")
                    continue
                preprocess_language_data(language, extract_path, preprocess_path)
                if clean_tmp:
                    delete_directory_if_exists(extract_path)
            except Exception as e:
                logging.error(f"Error preprocessing language {language}: {e}")
                continue
    else:
        logging.info("Skipping preprocessing step as per the argument.")

    if clean_tmp and not skip_download:
        delete_directory_if_exists(temp_path)

if __name__ == "__main__":
    main()

