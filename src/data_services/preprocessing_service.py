import logging
import subprocess
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.file_manager import ensure_directory_exists
from utils.constants import GENDER_MAP

MIN_AUDIO_DURATION = 2.0

def preprocess_language_data(language: str, extract_path: Path, save_path: Path):
    validated_tsv_path = extract_path / "validated.tsv"
    
    if not validated_tsv_path.exists():
        logging.warning(f"validated.tsv not found for language {language}")
        return
    
    df = load_and_filter_metadata(validated_tsv_path)
    create_output_directories(language, save_path, df)
    
    process_and_save_audio_files_concurrent(language, extract_path, save_path, df)
    remove_short_audio_files_concurrent(language, save_path)


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
    
    total_files = len(df)
    processed_files = 0
    mp3_files_found = False

    with ThreadPoolExecutor() as executor:
        futures = []
        for _, row in df.iterrows():
            if row['path'].endswith('.mp3'):
                mp3_files_found = True
                futures.append(executor.submit(process_single_file, row, clips_path, save_path, language))
        
        if not mp3_files_found:
            logging.warning(f"No valid .mp3 files found for language {language}. Check your validated.tsv file.")
            return

        for future in tqdm(as_completed(futures), total=len(futures), desc=f"Processing {language}"):
            if future.result():
                processed_files += 1

    logging.info(f"Processed {processed_files}/{total_files} audio files for language: {language}")


def process_single_file(row, clips_path: Path, save_path: Path, language: str) -> bool:
    audio_file_name = row['path']
    audio_path = clips_path / audio_file_name
    if not audio_path.exists():
        logging.warning(f"Audio file not found: {audio_path}")
        return False

    try:
        output_file_path = save_path / language / row['gender'] / audio_file_name
        ensure_directory_exists(output_file_path.parent)

        if not audio_path.is_file() or not audio_path.stat().st_size > 0:
            logging.error(f"File is unreadable or corrupted: {audio_path}")
            return False
        
        output_file_path = output_file_path.with_suffix('.wav')

        remove_silence(audio_path, output_file_path)

        return True

    except Exception as e:
        logging.error(f"Error processing {audio_path}: {e}")
        return False


def remove_short_audio_files_concurrent(language: str, save_path: Path):
    """Concurrently remove short audio files."""
    gender_dirs = [save_path / language / gender for gender in GENDER_MAP.values() if (save_path / language / gender).exists()]
    
    total_files = sum(len(list(gender_dir.glob("*.wav"))) for gender_dir in gender_dirs)
    removed_files = 0

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(check_and_remove_short_audio, audio_file)
            for gender_dir in gender_dirs
            for audio_file in gender_dir.glob("*.wav")
        ]
        
        for future in tqdm(as_completed(futures), total=total_files, desc=f"Removing short audio for {language}"):
            if future.result():
                removed_files += 1

    logging.info(f"Removed {removed_files}/{total_files} short audio files for language: {language}")


def check_and_remove_short_audio(audio_path: Path) -> bool:
    """Check if the audio file is shorter than the minimum duration and remove it."""
    if not is_audio_duration_valid(audio_path):
        audio_path.unlink()
        return True
    return False


def is_audio_duration_valid(audio_path: Path) -> bool:
    try:
        ffmpeg_command = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_path)
        ]
        result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        duration_str = result.stdout.decode().strip()

        if duration_str == 'N/A' or not duration_str:
            return False

        duration = float(duration_str)
        return duration >= MIN_AUDIO_DURATION

    except ValueError as e:
        logging.error(f"Error converting duration to float for {audio_path}: {e}")
        return False
    except Exception as e:
        logging.error(f"Error getting duration for {audio_path}: {e}")
        return False


def remove_silence(input_path: Path, output_path: Path):
    """Remove silence from the audio file."""
    try:
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

