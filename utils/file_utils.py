import os
import tarfile
import shutil
import logging
import requests
import pandas as pd
from tqdm import tqdm

def download_file(url: str, save_path: str) -> None:
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

def extract_validated_and_clips_from_tar(file_path: str, extract_path: str) -> None:
    logging.info(f"Starting extraction of tar file: {file_path}")
    with tarfile.open(file_path) as tar:
        for member in tar.getmembers():
            if member.isfile():
                # Extract only validated.tsv and clips directory
                if member.name.endswith("validated.tsv"):
                    member.name = "validated.tsv"  # Set member name to prevent path issues
                    tar.extract(member, path=extract_path, filter="fully_trusted")
                elif "clips/" in member.name:
                    member.name = os.path.join("clips", os.path.basename(member.name))
                    tar.extract(member, path=extract_path, filter="fully_trusted")
    
    logging.info(f"Completed extraction of tar file: {file_path}")
    os.remove(file_path)

def ensure_directory_exists(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f"Created directory: {path}")
    else:
        logging.info(f"Directory already exists: {path}")

def delete_directory_if_exists(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
        logging.info(f"Removed directory: {path}")
    else:
        logging.info(f"Directory does not exist: {path}")


def load_validated_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, sep='\t', usecols=['path', 'gender'])
    
    # Remove rows where gender is NaN
    df = df[df['gender'].notna()]
    
    # Simplify gender categories
    df['gender'] = df['gender'].apply(lambda x: 'male' if x in ['male_masculine', 'male'] else 'female' if x in ['female_feminine', 'female'] else None)
    
    return df
