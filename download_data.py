import requests
import os
import argparse
from tqdm import tqdm
import tarfile
import shutil


def get_download_url(language: str) -> list[dict]:
    """
    Fetch dataset information for a given language.

    Args:
        language (str): The language code.

    Returns:
        list[dict]: A list of dataset information dictionaries.
    """
    url = f"https://commonvoice.mozilla.org/api/v1/datasets/languages/{language}"
    response = requests.get(url)
    return response.json()


def find_largest_dataset(datasets: list[dict], max_bytes: int) -> dict | None:
    """
    Find the largest dataset within the size limit.

    Args:
        datasets (list[dict]): List of dataset information dictionaries.
        max_bytes (int): The maximum size in bytes.

    Returns:
        dict | None: The largest dataset within the size limit or None if no dataset is found.
    """
    largest_dataset = None
    largest_size = 0

    for dataset in datasets:
        size = dataset["size"]
        if size > largest_size and size <= max_bytes:
            largest_size = size
            largest_dataset = dataset

    return largest_dataset


def download_file(url: str, save_path: str) -> None:
    """
    Download a file from a URL with a progress bar.

    Args:
        url (str): The URL of the file to download.
        save_path (str): The path to save the downloaded file.
    """
    file_name = url.split("/")[-1].split("?")[0]

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
            bar.update(len(data))
            file.write(data)

    print(f"Downloaded file saved to {save_path}")


def extract_tar_file(file_path: str, extract_path: str) -> None:
    """
    Extract a tar.gz file to a specified directory, avoiding nested directories.

    Args:
        file_path (str): The path of the tar.gz file.
        extract_path (str): The directory to extract the contents to.
    """
    print(f"Extracting {file_path} to {extract_path}")

    with tarfile.open(file_path) as tar:
        members = tar.getmembers()
        top_level_dir = members[0].name.split("/")[0]
        for member in members:
            # Adjust the path to remove the top-level directory
            member.path = os.path.relpath(member.path, top_level_dir)
            tar.extract(member, path=extract_path)

    # Move files from nested directory to the parent directory
    extracted_files = os.listdir(extract_path)
    for file_name in extracted_files:
        full_file_name = os.path.join(extract_path, file_name)
        if os.path.isdir(full_file_name):
            for nested_file in os.listdir(full_file_name):
                shutil.move(os.path.join(full_file_name, nested_file), extract_path)
            os.rmdir(full_file_name)

    os.remove(file_path)
    print(f"Extraction complete and removed {file_path}")


def process_language(language: str, max_bytes: int, save_path: str) -> None:
    """
    Process a language by downloading and extracting its dataset.

    Args:
        language (str): The language code.
        max_bytes (int): The maximum size in bytes.
        save_path (str): The path to save the extracted data.
    """
    try:
        datasets = get_download_url(language)
        dataset = find_largest_dataset(datasets, max_bytes)

        if dataset:
            # Get the download path and encode it
            download_path = dataset["download_path"].replace("{locale}", language)
            download_path_encoded = download_path.replace("/", "%2F")
            download_url = f"https://commonvoice.mozilla.org/api/v1/bucket/dataset/{download_path_encoded}"

            # Fetch the actual download URL
            response = requests.get(download_url)
            download_info = response.json()
            url = download_info["url"]

            # Create temporary path for download
            temp_path = os.path.join(save_path, "temp")
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)

            # Download the file
            file_name = os.path.join(temp_path, f"{language}.tar.gz")
            download_file(url, file_name)

            # Extract the file
            extract_path = os.path.join(save_path, language)

            # Remove existing directory if it exists
            if os.path.exists(extract_path):
                shutil.rmtree(extract_path)
                print(f"Removed existing directory {extract_path}")

            os.makedirs(extract_path)
            extract_tar_file(file_name, extract_path)

            print(f"Processed language {language}")
        else:
            print(
                f"No suitable dataset found for language {language} within the size limit."
            )
    except Exception as e:
        print(f"An error occurred for language {language}: {e}")


def download_and_extract(
    languages: list[str], data_size_gb: float, save_path: str
) -> None:
    """
    Download and extract datasets for a list of languages.

    Args:
        languages (list[str]): List of language codes to download.
        data_size_gb (float): The maximum size of data to download in GB.
        save_path (str): The path to save the extracted data.
    """
    bytes_per_gb = 2**30  # 1 GB in bytes
    max_bytes = int(data_size_gb * bytes_per_gb)

    # Create a temporary directory for downloads
    temp_path = os.path.join(save_path, "temp")
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    for language in languages:
        process_language(language, max_bytes, save_path)

    # Remove the temporary directory
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        print(f"Removed temporary directory {temp_path}")


def get_available_languages() -> dict[str, str]:
    """
    Fetch the list of available languages.

    Returns:
        dict[str, str]: A dictionary of language symbols and their names.
    """
    print("Fetching available languages")

    url = "https://commonvoice.mozilla.org/api/v1/languages/en/translations"
    response = requests.get(url)
    text = response.text

    # Extract the relevant section for languages
    languages_section = text.split("## Languages")[1].split("# [/]")[0].strip()
    languages = [
        line.split(" = ") for line in languages_section.split("\n") if " = " in line
    ]

    return {symbol.strip(): name.strip() for symbol, name in languages}


def main() -> None:
    """
    Main function to parse arguments and download datasets.
    """
    parser = argparse.ArgumentParser(
        description="Download speech data from Mozilla Common Voice."
    )
    parser.add_argument(
        "--languages", nargs="+", help="List of languages to download", required=True
    )
    parser.add_argument(
        "--size", type=float, help="Total size of data to download in GB", required=True
    )
    parser.add_argument(
        "--save_path", type=str, default="data", help="Path to save downloaded data"
    )

    args = parser.parse_args()

    available_languages = get_available_languages()

    if "help" in args.languages or any(
        lang not in available_languages for lang in args.languages
    ):
        print("Available languages:")
        for symbol, name in available_languages.items():
            print(f"{symbol}: {name}")
    else:
        download_and_extract(args.languages, args.size, args.save_path)


if __name__ == "__main__":
    main()
