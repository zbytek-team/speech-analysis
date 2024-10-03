import argparse
import logging
from pathlib import Path

from utils.logging_setup import setup_logging
from data_services.preprocessing_service import preprocess_language_data

setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Preprocess downloaded speech data.")
    parser.add_argument("--languages", nargs="+", required=True, help="List of languages to preprocess")
    parser.add_argument("--source", type=str, default="data/raw", help="Path to raw downloaded data")
    parser.add_argument("--destination", type=str, default="data/processed", help="Path to save preprocessed data")
    
    args = parser.parse_args()

    languages = args.languages
    source_dir = Path(args.source)
    destination_dir = Path(args.destination)

    for language in languages:
        logging.info(f"Preprocessing data for language: {language}")
        try:
            preprocess_language_data(language, source_dir / language, destination_dir)
        except Exception as e:
            logging.error(f"Error preprocessing language {language}: {e}")

if __name__ == "__main__":
    main()

