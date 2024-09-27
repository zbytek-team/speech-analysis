# **Speech Analysis Project**

This research project at the Gdańsk University of Technology aims to develop a method for identifying characteristic frequency ranges for different languages. The goal is to review methods of speech frequency analysis and, based on speech recordings for various languages, verify Dr. Alfred Tomatis's theory that different languages have distinct frequency ranges for specific phonemes.

## **Requirements**

To run this project, you need the following libraries and tools:

- **Python** 3.6 or higher
- **pip** (Python package manager)

## **Installation**

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/speech-analysis-project.git

   cd speech-analysis-project
   ```

2. Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

## **Usage**

### 1. Downloading and Preprocessing Data

Use `download_data.py` to download and preprocess speech data from Mozilla Common Voice.

- Example command:

  ```bash
  python download_data.py --languages pl en --size 5
  ```

  This downloads speech data for Polish (`pl`) and English (`en`), assuming the size limit is 5 GB.
  You can skip the download step and proceed directly to preprocessing with the `--skip-download` flag if data is already present.

### 2. Running Speech Analysis

Use `analyze_data.py` to analyze preprocessed audio data and extract features.

- Example command:

  ```bash
  python analyze_data.py --languages pl en --analyzers pitch formant spectral mfcc zero_crossing hnr
  ```

  This analyzes the data for Polish and English, extracting features like pitch, formants, spectral features, MFCCs, zero-crossing rate, and harmonic-to-noise ratio (HNR).

### 3. Specifying Analyzers

You can specify which analyzers to run using the `--analyzers` flag. Available analyzers:

- `pitch`: Analyzes the fundamental frequency of the audio.
- `formant`: Extracts the first and second formant frequencies (F1, F2).
- `spectral`: Analyzes spectral features such as centroid, bandwidth, flatness, and rolloff.
- `mfcc`: Extracts Mel-Frequency Cepstral Coefficients (MFCCs).
- `zero_crossing`: Measures the zero-crossing rate (ZCR) of the audio.
- `hnr`: Measures the harmonic-to-noise ratio (HNR).

### 4. Output

The analysis results are saved as CSV files in the `analysis_results/` directory. Each file corresponds to a specific language and gender, containing the extracted features for the analyzed audio files.

- Example output: `pl_male_stats.csv`, `en_female_stats.csv`.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

