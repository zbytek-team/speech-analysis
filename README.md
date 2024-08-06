# Speech Analysis Project

This research project at the Gdańsk University of Technology aims to develop a method for identifying characteristic frequency ranges for different languages. The goal is to review methods of speech frequency analysis and, based on speech recordings for various languages, verify Dr. Alfred Tomatis's theory that different languages have distinct frequency ranges for specific phonemes.

## Requirements

- Python 3.12

## Project Structure

The project consists of two main scripts and a module containing additional scripts:

1. **download_data.py**: This script downloads speech data from Mozilla Common Voice.
2. **run_analysis.py**: This script uses functions from the `speech_analysis` module to process and analyze the downloaded speech data.

### download_data.py

This script downloads speech datasets for specified languages from Mozilla Common Voice. It fetches the largest available dataset within a specified size limit and extracts the audio files and metadata.

#### Usage

```bash
python download_data.py --languages <language_codes> --size <size_in_GB> --save_path <save_path>
```

- `--languages`: List of language codes to download (e.g., `en`, `de`, `pl`).
- `--size`: Total size of data to download in GB.
- `--save_path`: Path to save downloaded data (default: `data`).

### run_analysis.py

This script processes the downloaded data, normalizes audio loudness, filters noise, removes silence, and performs frequency analysis. It uses the following submodules from the `speech_analysis` module:

- **preprocessing.py**: Handles the loading and preprocessing of audio data.
- **frequency_analysis.py**: Conducts frequency analysis on the preprocessed audio data.
- **plotting.py**: Generates plots of the frequency analysis results.

#### Usage

```bash
python run_analysis.py --data_path <data_path> --output_path <output_path>
```

- `--data_path`: Path to the directory containing the downloaded data.
- `--output_path`: Path to save the analysis results and plots (default: `plots`).

## How It Works

1. **Downloading Data**: The `download_data.py` script fetches and extracts the speech datasets from Mozilla Common Voice.
2. **Preprocessing**: The `preprocessing.py` script loads the audio files and performs normalization, noise filtering, and silence removal.
3. **Frequency Analysis**: The `frequency_analysis.py` script analyzes the frequency ranges of the processed audio files.
4. **Plotting Results**: The `plotting.py` script generates plots of the frequency analysis, which are saved in the `plots` directory.
