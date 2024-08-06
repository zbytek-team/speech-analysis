import numpy as np
import matplotlib.pyplot as plt
import librosa
import os


def plot_frequency_analysis(
    frequency_spectra: list[np.ndarray],
    sr: int,
    language: str,
    gender: str,
    save_path: str,
) -> None:
    """
    Plot the frequency analysis for the given language and gender and save the plot.

    Args:
        frequency_spectra (list[np.ndarray]): List of frequency spectra.
        sr (int): Sample rate of the audio.
        language (str): Language code.
        gender (str): Gender ('male' or 'female').
        save_path (str): Path to save the plot.
    """
    freqs = librosa.fft_frequencies(sr=sr)
    mean_spectrum = np.mean(frequency_spectra, axis=0)

    plt.figure(figsize=(10, 6))
    plt.plot(freqs, mean_spectrum, label=f"{language} - {gender}")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title(f"Frequency Analysis for {language} - {gender}")
    plt.legend()

    # Ensure the save directory exists
    os.makedirs(save_path, exist_ok=True)
    file_name = f"{language}_{gender}_frequency_analysis.png"
    plot_path = os.path.join(save_path, file_name)
    plt.savefig(plot_path)
    plt.close()
