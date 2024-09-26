import logging
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

from utils.file_utils import ensure_directory_exists


GENDER_MAP = {
    'male': 'male',
    'male_masculine': 'male',
    'female': 'female',
    'female_feminine': 'female'
}


def preprocess_language_data(language: str, extract_path: Path, save_path: str) -> None:
    validated_tsv_path = extract_path / "validated.tsv"

    if not validated_tsv_path.exists():
        logging.warning(f"validated.tsv not found for language {language}")
        return

    df = load_and_filter_metadata(validated_tsv_path)
    create_output_directories(language, save_path, df)

    process_and_save_audio_files(language, extract_path, save_path, df)


def load_and_filter_metadata(validated_tsv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(validated_tsv_path, sep='\t', usecols=["path", "gender"])
    df = df[df['gender'].notna()]

    df['gender'] = df['gender'].apply(
        lambda x: GENDER_MAP.get(x.strip().lower(), None)
    )

    df = df[df["gender"].isin(["male", "female"])]

    return df


def create_output_directories(language: str, save_path: str, df: pd.DataFrame) -> None:
    genders = df['gender'].unique()
    for gender in genders:
        output_path = Path(save_path) / language / gender
        ensure_directory_exists(output_path)


def process_and_save_audio_files(language: str, extract_path: Path, save_path: str, df: pd.DataFrame) -> None:
    clips_path = extract_path / "clips"
    for _, row in tqdm(df.iterrows(), total=df.shape[0], desc=f"Preprocessing {language}"):
        audio_file_name = row['path']
        audio_path = clips_path / audio_file_name
        if not audio_path.exists():
            logging.warning(f"Audio file not found: {audio_path}")
            continue

        try:
            trimmed_audio = remove_silence(audio_path)

            gender = row['gender']
            output_file_path = Path(save_path) / language / gender / audio_file_name
            trimmed_audio.export(output_file_path, format='mp3')

            logging.debug(f"Processed and saved: {output_file_path}")

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
