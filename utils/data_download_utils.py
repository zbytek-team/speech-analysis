import logging
import requests
from pathlib import Path
from tqdm import tqdm
import tarfile

from utils.file_utils import ensure_directory_exists, delete_directory_if_exists
from utils.constants import COMMONVOICE_API_URL, BYTES_PER_GB


def get_download_url(language: str) -> list:
    url = f"{COMMONVOICE_API_URL}/datasets/languages/{language}"
    response = requests.get(url)
    logging.info(f"Retrieved dataset information for language: {language}")
    return response.json()


def find_largest_dataset(datasets: list, max_bytes: int, language: str) -> dict:
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
        logging.warning(
            f"The largest found {language} dataset within the threshold is quite small ({largest_size / BYTES_PER_GB:.2f} GB)."
        )
        if smallest_dataset_above_max:
            logging.warning(
                f"The next larger {language} dataset is {smallest_size_above_max / BYTES_PER_GB:.2f} GB. Consider increasing the size parameter."
            )
        else:
            logging.warning(f"No larger {language} dataset available.")

    return largest_dataset


def download_file(url: str, save_path: Path) -> None:
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

    logging.info(f"Completed download of file: {file_name}")


def extract_validated_and_clips_from_tar(file_path: Path, extract_path: Path) -> None:
    logging.info(f"Starting extraction of tar file: {file_path}")
    with tarfile.open(file_path) as tar:
        for member in tar.getmembers():
            if member.isfile():
                if member.name.endswith("validated.tsv"):
                    member.name = "validated.tsv"
                    tar.extract(member, path=extract_path, set_attrs=False)
                elif "clips/" in member.name:
                    member.name = str(Path("clips") / Path(member.name).name)
                    tar.extract(member, path=extract_path, set_attrs=False)
    logging.info(f"Completed extraction of tar file: {file_path}")
    file_path.unlink()


def download_language_dataset(language: str, max_bytes: int, temp_path: Path) -> Path:
    datasets = get_download_url(language)
    dataset = find_largest_dataset(datasets, max_bytes, language)

    if not dataset:
        logging.warning(f"No suitable dataset found for language {language}")
        return None

    download_path = dataset["download_path"].replace("{locale}", language)
    download_path_encoded = download_path.replace("/", "%2F")
    download_url = f"{COMMONVOICE_API_URL}/bucket/dataset/{download_path_encoded}"

    response = requests.get(download_url)
    download_info = response.json()
    url = download_info["url"]

    file_name = temp_path / f"{language}.tar.gz"
    download_file(url, file_name)

    extract_path = temp_path / language
    delete_directory_if_exists(extract_path)
    ensure_directory_exists(extract_path)

    extract_validated_and_clips_from_tar(file_name, extract_path)

    return extract_path
