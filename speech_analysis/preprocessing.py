import os
import librosa
import numpy as np
import shutil
import pandas as pd


def normalize_audio(y: np.ndarray) -> np.ndarray:
    """Normalize audio to -1 to 1 range."""
    return y / np.max(np.abs(y))


def remove_silence(y: np.ndarray, sr: int) -> np.ndarray:
    """Remove silence from the beginning and end of the audio."""
    non_silent_intervals = librosa.effects.split(y, top_db=20)
    non_silent_audio = np.concatenate(
        [y[start:end] for start, end in non_silent_intervals]
    )
    return non_silent_audio


def process_audio_file(file_path: str) -> tuple[np.ndarray, int]:
    """Load, normalize, and remove silence from an audio file."""
    y, sr = librosa.load(file_path, sr=None)
    y = normalize_audio(y)
    y = remove_silence(y, sr)
    return y, sr


def process_language_data(
    language_data: dict[str, pd.DataFrame], data_path: str
) -> dict[str, dict[str, list[tuple[np.ndarray, int]]]]:
    """
    Process all audio files for a given language, normalizing and removing silence.

    Args:
        language_data (dict): Dictionary containing dataframes for male and female speakers.
        data_path (str): The path to the main data directory.

    Returns:
        dict[str, dict[str, list[tuple[np.ndarray, int]]]]: Processed audio data.
    """
    processed_data = {"male": [], "female": []}

    for gender, df in language_data.items():
        for index, row in df.iterrows():
            file_path = os.path.join(data_path, row["locale"], "clips", row["path"])
            try:
                processed_audio, sr = process_audio_file(file_path)
                processed_data[gender].append((processed_audio, sr))
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

    return processed_data
