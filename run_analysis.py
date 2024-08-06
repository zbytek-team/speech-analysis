import os
import argparse

from speech_analysis.data_loader import load_data
from speech_analysis.preprocessing import process_language_data
from speech_analysis.analysis import perform_frequency_analysis
from speech_analysis.plotting import plot_frequency_analysis

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run speech analysis on dataset.")
    parser.add_argument(
        "--data_path", type=str, default="data", help="Path to the main data directory"
    )
    parser.add_argument(
        "--plot_path", type=str, default="plots", help="Path to save the plots"
    )
    args = parser.parse_args()

    data_path = args.data_path
    plot_path = args.plot_path

    # Load and process the data
    data = load_data(data_path)

    all_processed_data = {}
    all_frequency_spectra = {}

    # Process audio files for each language and gender
    for language, gender_data in data.items():
        print(f"Processing audio files for language: {language}")
        processed_data = process_language_data(gender_data, data_path)
        all_processed_data[language] = processed_data

        # Perform frequency analysis
        all_frequency_spectra[language] = {}
        for gender, audio_data in processed_data.items():
            frequency_spectra = perform_frequency_analysis(audio_data)
            all_frequency_spectra[language][gender] = frequency_spectra

            # Plot the frequency analysis
            if audio_data:
                plot_frequency_analysis(
                    frequency_spectra, audio_data[0][1], language, gender, plot_path
                )

    print("Audio processing and frequency analysis complete.")
    print(f"Plots have been saved to {plot_path}")
