import os
import argparse
import logging
import requests

from utils.file_utils import download_file, extract_validated_and_clips_from_tar, ensure_directory_exists, delete_directory_if_exists

from utils.logging_utils import setup_logging

setup_logging()

# Constants
COMMONVOICE_API_URL = "https://commonvoice.mozilla.org/api/v1"
DEFAULT_SAVE_DIR = "data"
TMP_FOLDER_NAME = "tmp"
DOWNLOAD_FILE_EXTENSION = ".tar.gz"
BYTES_PER_GB = 2**30


def get_download_url(language: str) -> list[dict]:
    url = f"{COMMONVOICE_API_URL}/datasets/languages/{language}"
    response = requests.get(url)
    logging.info(f"Retrieved dataset information for language: {language}")
    return response.json()

def find_largest_dataset(datasets: list[dict], max_bytes: int, language: str) -> dict | None:
    largest_dataset = None
    largest_size = 0
    smallest_dataset_above_max = None
    smallest_size_above_max = float("inf")

    for dataset in datasets:
        size = dataset["size"]
        if size > largest_size and size <= max_bytes:
            largest_size = size
            largest_dataset = dataset
        if size > max_bytes and size < smallest_size_above_max:
            smallest_size_above_max = size
            smallest_dataset_above_max = dataset

    if largest_size < max_bytes * 0.5:
        logging.warning(f"The largest found {language} dataset within the threshold is quite small ({largest_size / BYTES_PER_GB:.2f} GB). ")
        if smallest_dataset_above_max:
            logging.warning(f"The next larger {language} dataset is {smallest_size_above_max / BYTES_PER_GB:.2f} GB. Consider increasing the size parameter.")
        else:
            logging.warning(f"No larger {language} dataset available.")

    return largest_dataset

def process_language(language: str, max_bytes: int, save_path: str) -> None:
    logging.info(f"Processing language: {language}")
    try:
        datasets = get_download_url(language)
        dataset = find_largest_dataset(datasets, max_bytes, language)

        if not dataset:
            logging.warning(f"No suitable dataset found for language {language}")
            return

        download_path = dataset["download_path"].replace("{locale}", language)
        download_path_encoded = download_path.replace("/", "%2F")
        download_url = f"{COMMONVOICE_API_URL}/bucket/dataset/{download_path_encoded}"

        response = requests.get(download_url)
        download_info = response.json()
        url = download_info["url"]

        temp_path = os.path.join(save_path, TMP_FOLDER_NAME)
        ensure_directory_exists(temp_path)

        file_name = os.path.join(temp_path, f"{language}{DOWNLOAD_FILE_EXTENSION}")
        download_file(url, file_name)

        extract_path = os.path.join(save_path, language)

        delete_directory_if_exists(extract_path)
        ensure_directory_exists(extract_path)

        extract_validated_and_clips_from_tar(file_name, extract_path)

        logging.info(f"Completed processing language: {language}")

    except Exception as e:
        logging.error(f"Error processing language {language}: {e}")

def download_and_extract(languages: list[str], data_size_gb: float, save_path: str) -> None:
    max_bytes = int(data_size_gb * BYTES_PER_GB)
    temp_path = os.path.join(save_path, TMP_FOLDER_NAME)
    ensure_directory_exists(temp_path)

    for language in languages:
        process_language(language, max_bytes, save_path)

    delete_directory_if_exists(temp_path)

def get_available_languages() -> dict[str, str]:
    url = f"{COMMONVOICE_API_URL}/languages/en/translations"
    response = requests.get(url)
    text = response.text

    # Extract language information from response text
    languages_section = text.split("## Languages")[1].split("# [/]")[0].strip()
    languages = [
        line.split(" = ") for line in languages_section.split("\n") if " = " in line
    ]

    return {symbol.strip(): name.strip() for symbol, name in languages}

def main() -> None:
    parser = argparse.ArgumentParser(description="Download speech data from Mozilla Common Voice.")
    parser.add_argument("--languages", nargs="+", help="List of languages to download", required=True)
    parser.add_argument("--size", type=float, help="Total size of data to download in GB")
    parser.add_argument("--save_path", type=str, default=DEFAULT_SAVE_DIR, help="Path to save downloaded data")

    args = parser.parse_args()

    available_languages = get_available_languages()

    # Check if specified languages are available
    if "help" in args.languages or any(lang not in available_languages for lang in args.languages):
        print("Available languages:")
        for symbol, name in available_languages.items():
            print(f"{symbol}: {name}")
    elif args.size is None:
        print("Please specify the total size of data to download using the --size argument.")
    else:
        download_and_extract(args.languages, args.size, args.save_path)

if __name__ == "__main__":
    main()
