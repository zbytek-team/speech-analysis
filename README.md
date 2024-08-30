# Speech Analysis Project

This research project at the Gdańsk University of Technology aims to develop a method for identifying characteristic frequency ranges for different languages. The goal is to review methods of speech frequency analysis and, based on speech recordings for various languages, verify Dr. Alfred Tomatis's theory that different languages have distinct frequency ranges for specific phonemes.

## Requirements

- Python 3.12

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ack2406/speech-analysis
   ```

2. Navigate to the project directory:

   ```bash
   cd speech-analysis
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

The project consists of two main scripts and several modules:

1. **`download_data.py`**: This script downloads speech data from Mozilla Common Voice.
2. **`analyze_data.py`**: This script processes and analyzes the downloaded speech data.

### `download_data.py`

This script downloads speech datasets for specified languages from Mozilla Common Voice. It fetches the largest available dataset within a specified size limit and extracts the audio files and metadata.

#### Usage

```bash
python3 download_data.py --languages <language_codes> --size <size_in_GB> --save_path <save_path>
```

- `--languages`: List of language codes to download (e.g., `en`, `de`, `pl`).
- `--size`: Total size of data to download in GB.
- `--save_path`: Path to save downloaded data (default: `data`).

### `analyze_data.py`

This script processes the downloaded data and performs frequency analysis.

#### Usage

```bash
python3 analyze_data.py --data_dir <data_dir> --output_dir <output_dir>
```

- `--data_dir`: Path to the directory containing the downloaded data (default: `data`).
- `--output_dir`: Path to save the analysis results and plots (default: `plots`).

## How It Works

1. **Downloading Data**: The `download_data.py` script fetches and extracts the speech datasets from Mozilla Common Voice based on specified languages and size constraints.
2. **Frequency Analysis**: The `analyzer.py` script in `analysis/` preprocesses the audio data and performs the frequency analysis.
3. **Plotting Results**: Results from the analyses are plotted and saved in the specified output directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
