import tarfile
import shutil
import logging
import requests
import polars as pl
from tqdm import tqdm
from pathlib import Path

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
                # Extract only validated.tsv and clips directory
                if member.name.endswith("validated.tsv"):
                    member.name = "validated.tsv"  # Set member name to prevent path issues
                    tar.extract(member, path=extract_path, filter="fully_trusted")
                elif "clips/" in member.name:
                    member.name = str(Path("clips") / Path(member.name).name)  # Using pathlib to construct path
                    tar.extract(member, path=extract_path, filter="fully_trusted")
    
    logging.info(f"Completed extraction of tar file: {file_path}")
    file_path.unlink()  # Remove the tar file after extraction

def ensure_directory_exists(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {path}")
    else:
        logging.info(f"Directory already exists: {path}")

def delete_directory_if_exists(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
        logging.info(f"Removed directory: {path}")
    else:
        logging.info(f"Directory does not exist: {path}")

def _simplify_genders(gender: str) -> str|None:
    match gender:
        case "male_masculine" | "male":
            return "male"
        case "female_feminine" | "female":
            return "female"
    return None

def load_validated_data(file_path: Path) -> pl.DataFrame:
    q = (
        pl.scan_csv(file_path, separator='\t')
        .select(
            pl.col("path"),
            pl.col("gender").map_elements(_simplify_genders, return_dtype=pl.String) 
        )
        .drop_nulls()
    )

    df = q.collect()
    
    return df

