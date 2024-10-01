import logging
import pandas as pd
from pathlib import Path
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from tqdm import tqdm

from utils.file_manager import ensure_directory_exists
from utils.constants import GENDER_MAP


def preprocess_language_data(language: str, extract_path: Path, save_path: Path):
    """Preprocess the audio data by removing silence and organizing by gender."""
    validated_tsv_path = extract_path / "validated.tsv"
    
    if not validated_tsv_path.exists():
        logging.warning(f"validated.tsv not found for language {language}")
        return
    
    df = load_and_filter_metadata(validated_tsv_path)
    create_output_directories(language, save_path, df)

    process_and_save_audio_files(language, extract_path, save_path, df)


def load_and_filter_metadata(validated_tsv_path: Path) -> pd.DataFrame:
    """Load metadata and filter relevant columns."""
    df = pd.read_csv(validated_tsv_path, sep='\t', usecols=["path", "gender"]) # type: ignore
    df = df[df['gender'].notna()]
    df['gender'] = df['gender'].apply(lambda x: GENDER_MAP.get(x.strip().lower(), None))
    return df[df["gender"].isin(["male", "female"])]


def create_output_directories(language: str, save_path: Path, df: pd.DataFrame):
    """Create directories for gender-based audio files."""
    genders = df['gender'].unique()
    for gender in genders:
        output_path = save_path / language / gender
        ensure_directory_exists(output_path)


def process_and_save_audio_files(language: str, extract_path: Path, save_path: Path, df: pd.DataFrame):
    """Process and save audio files by removing silence."""
    clips_path = extract_path / "clips"
    
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc=f"Processing {language}"):
        audio_file_name = row['path']
        audio_path = clips_path / audio_file_name
        if not audio_path.exists():
            logging.warning(f"Audio file not found: {audio_path}")
            continue

        try:
            trimmed_audio = remove_silence(audio_path)
            gender = row['gender']
            output_file_path = save_path / language / gender / audio_file_name
            trimmed_audio.export(output_file_path, format='mp3')
        except Exception as e:
            logging.error(f"Error processing {audio_path}: {e}")


def remove_silence(audio_path, silence_thresh=-16, min_silence_len=500):
    """Remove silence from the beginning and end of an audio file."""
    audio = AudioSegment.from_file(audio_path)
    dBFS = audio.dBFS
    silence_threshold = dBFS + silence_thresh
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)
    
    if nonsilent_ranges:
        start_trim = nonsilent_ranges[0][0]
        end_trim = nonsilent_ranges[-1][1]
        trimmed_audio = audio[start_trim:end_trim]
    else:
        trimmed_audio = audio

    return trimmed_audio

