import logging
import subprocess
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.file_manager import ensure_directory_exists
from utils.constants import GENDER_MAP

def preprocess_language_data(language: str, extract_path: Path, save_path: Path):
    validated_tsv_path = extract_path / "validated.tsv"
    
    if not validated_tsv_path.exists():
        logging.warning(f"validated.tsv not found for language {language}")
        return
    
    df = load_and_filter_metadata(validated_tsv_path)
    create_output_directories(language, save_path, df)
    
    process_and_save_audio_files_concurrent(language, extract_path, save_path, df)


def load_and_filter_metadata(validated_tsv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(validated_tsv_path, sep='\t', usecols=["path", "gender"])  # type: ignore
    df = df[df['gender'].notna()]
    df['gender'] = df['gender'].apply(lambda x: GENDER_MAP.get(x.strip().lower(), None))
    return df[df["gender"].isin(["male", "female"])]


def create_output_directories(language: str, save_path: Path, df: pd.DataFrame):
    genders = df['gender'].unique()
    for gender in genders:
        output_path = save_path / language / gender
        ensure_directory_exists(output_path)


def process_and_save_audio_files_concurrent(language: str, extract_path: Path, save_path: Path, df: pd.DataFrame):
    clips_path = extract_path / "clips"
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_single_file, row, clips_path, save_path, language)
            for _, row in df.iterrows()
        ]
        for future in tqdm(as_completed(futures), total=len(futures), desc=f"Processing {language}"):
            future.result()


def process_single_file(row, clips_path: Path, save_path: Path, language: str):
    audio_file_name = row['path']
    audio_path = clips_path / audio_file_name
    if not audio_path.exists():
        logging.warning(f"Audio file not found: {audio_path}")
        return

    try:
        output_file_path = save_path / language / row['gender'] / audio_file_name
        ensure_directory_exists(output_file_path.parent)

        if not audio_path.is_file() or not audio_path.stat().st_size > 0:
            logging.error(f"File is unreadable or corrupted: {audio_path}")
            return

        remove_silence(audio_path, output_file_path)
    
    except Exception as e:
        logging.error(f"Error processing {audio_path}: {e}")


def remove_silence(input_path: Path, output_path: Path):
    try:
        output_path = output_path.with_suffix('.wav')

        ffmpeg_command = [
            'ffmpeg',
            '-i', str(input_path),
            '-af', (
                'silenceremove=start_periods=1:start_threshold=-50dB:start_duration=0.1,areverse,'
                'silenceremove=start_periods=1:start_threshold=-50dB:start_duration=0.1,areverse,'
                'loudnorm'
            ),
            '-y',
            str(output_path)
        ]

        process = subprocess.run(ffmpeg_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if process.returncode != 0:
            logging.error(f"FFmpeg returned non-zero exit code {process.returncode} for {input_path}")
            logging.error(f"FFmpeg stderr: {process.stderr.decode('utf-8')}")

    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg failed for {input_path}: {e}")
        logging.error(f"FFmpeg stderr: {e.stderr.decode('utf-8')}")

