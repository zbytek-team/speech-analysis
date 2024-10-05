import argparse
import logging
import requests
from pathlib import Path
from tqdm import tqdm
import tarfile

from utils.logging_setup import setup_logging
from utils.file_manager import ensure_directory_exists, delete_directory_if_exists

setup_logging()

COMMONVOICE_API_URL = "https://commonvoice.mozilla.org/api/v1"
BYTES_PER_GB = 2**30


def list_available_languages() -> dict[str, str]:
    url = f"{COMMONVOICE_API_URL}/languages/en/translations"
    response = requests.get(url)
    response_text = response.text

    languages_section = response_text.split("## Languages")[1].split("# [/]")[0].strip()
    languages = [
        line.split(" = ") for line in languages_section.split("\n") if " = " in line
    ]

    return {symbol.strip(): name.strip() for symbol, name in languages}


def get_language_datasets(language: str) -> list:
    url = f"{COMMONVOICE_API_URL}/datasets/languages/{language}"
    response = requests.get(url)
    logging.info(f"Retrieved dataset information for language: {language}")
    return response.json()


def select_largest_dataset(datasets: list, max_bytes: int, language: str) -> dict | None:
    largest_dataset = None
    largest_size = 0
    smallest_dataset_above_limit = None
    smallest_size_above_limit = float("inf")

    for dataset in datasets:
        size = dataset["size"]
        if size > largest_size and size <= max_bytes:
            largest_size = size
            largest_dataset = dataset
        if size > max_bytes and size < smallest_size_above_limit:
            smallest_size_above_limit = size
            smallest_dataset_above_limit = dataset

    if largest_size < max_bytes * 0.5:
        logging.warning(
            f"The largest {language} dataset found within the limit is quite small ({largest_size / BYTES_PER_GB:.2f} GB)."
        )
        if smallest_dataset_above_limit:
            logging.warning(
                f"The next available {language} dataset is {smallest_size_above_limit / BYTES_PER_GB:.2f} GB. Consider increasing the size limit."
            )
        else:
            logging.warning(f"No larger {language} dataset available.")

    return largest_dataset


def download_file_from_url(url: str, save_path: Path) -> None:
    file_name = url.split("/")[-1].split("?")[0]
    logging.info(f"Starting download of file: {file_name}")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    with open(save_path, "wb") as file, tqdm(
        desc=file_name,
        total=total_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=block_size):
            file.write(data)
            bar.update(len(data))

    logging.info(f"Download completed for file: {file_name}")


def extract_files_from_tar(file_path: Path, extract_path: Path) -> None:
    logging.info(f"Extracting contents from tar file: {file_path}")
    with tarfile.open(file_path) as tar:
        for member in tar.getmembers():
            if member.isfile():
                if member.name.endswith("validated.tsv"):
                    member.name = "validated.tsv"
                    tar.extract(member, path=extract_path, set_attrs=False)
                elif "clips/" in member.name:
                    member.name = str(Path("clips") / Path(member.name).name)
                    tar.extract(member, path=extract_path, set_attrs=False)
    logging.info(f"Extraction completed for tar file: {file_path}")
    file_path.unlink()


def download_and_extract_language_data(language: str, max_bytes: int, zips_dir: Path, destination: Path) -> Path | None:
    datasets = get_language_datasets(language)
    selected_dataset = select_largest_dataset(datasets, max_bytes, language)

    if not selected_dataset:
        logging.warning(f"No suitable dataset found for language {language}")
        return None

    download_path = selected_dataset["download_path"].replace("{locale}", language)
    download_url = f"{COMMONVOICE_API_URL}/bucket/dataset/{download_path.replace('/', '%2F')}"

    response = requests.get(download_url)
    download_info = response.json()
    file_url = download_info["url"]

    file_name = zips_dir / f"{language}.tar.gz"
    download_file_from_url(file_url, file_name)

    extract_path = destination / language
    delete_directory_if_exists(extract_path)
    ensure_directory_exists(extract_path)

    extract_files_from_tar(file_name, extract_path)

    return extract_path


def download_datasets(languages: list[str], size_limit_gb: float, destination: str, zips_dir: str) -> None:
    max_bytes = int(size_limit_gb * BYTES_PER_GB)
    zips_path = Path(zips_dir)
    ensure_directory_exists(zips_path)

    for language in languages:
        logging.info(f"Downloading dataset for language: {language}")
        try:
            download_and_extract_language_data(language, max_bytes, zips_path, Path(destination))
        except Exception as e:
            logging.error(f"Error downloading dataset for language {language}: {e}")
            continue

    logging.info("All downloads and extractions completed.")


def main():
    parser = argparse.ArgumentParser(description="Download and extract Mozilla Common Voice datasets.")
    parser.add_argument("--languages", nargs="+", help="List of languages to download")
    parser.add_argument("--size", type=float, help="Maximum dataset size to download in GB")
    parser.add_argument("--destination", type=str, default="data/raw", help="Destination path for downloaded and extracted data")
    parser.add_argument("--zips-dir", type=str, default="data/zips", help="Directory to store zip files during download")
    parser.add_argument("--list-languages", action="store_true", help="List available languages from Common Voice API")

    args = parser.parse_args()

    if args.list_languages:
        available_languages = list_available_languages()
        print("Available languages:")
        for symbol, name in available_languages.items():
            print(f"{symbol}: {name}")
        return

    if not args.languages:
        parser.error("The --languages argument is required unless --list-languages is specified.")
    if not args.size:
        parser.error("The --size argument is required unless --list-languages is specified.")

    download_datasets(args.languages, args.size, args.destination, args.zips_dir)


if __name__ == "__main__":
    main()
