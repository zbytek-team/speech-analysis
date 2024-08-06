import numpy as np
import librosa


def perform_frequency_analysis(
    audio_data: list[tuple[np.ndarray, int]]
) -> list[np.ndarray]:
    """
    Perform Short-Time Fourier Transform (STFT) on the audio data to analyze frequency components.

    Args:
        audio_data (list[tuple[np.ndarray, int]]): List of tuples containing audio data and sample rate.

    Returns:
        list[np.ndarray]: List of frequency spectra for each audio file.
    """
    frequency_spectra = []
    for y, sr in audio_data:
        stft = np.abs(librosa.stft(y))
        frequency_spectra.append(np.mean(stft, axis=1))
    return frequency_spectra
