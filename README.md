# Speech Analysis Project

This research project at the Gdańsk University of Technology aims to develop a method for identifying characteristic frequency ranges for different languages. The goal is to review methods of speech frequency analysis and, based on speech recordings for various languages, verify Dr. Alfred Tomatis's theory that different languages have distinct frequency ranges for specific phonemes.

## Requirements

- Python 3.12+

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ack2406/speech-analysis
   cd speech-analysis
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

This project uses a `Makefile` to streamline various tasks like downloading datasets, extracting features, and listing available options.

### Download and Extract Data

To download speech data and extract features for specific languages in one step:

```bash
make download_and_extract LANGUAGES="pl en" DATA_SIZE=2 FEATURES="pitch mfcc"
```

- `LANGUAGES`: List of languages to download and extract features for (e.g., `"pl en"`).
- `DATA_SIZE`: Total size of the dataset to download in GB (e.g., `2`).
- `FEATURES`: List of features to extract (e.g., `"pitch mfcc"`). If not provided, all available features will be extracted.
- `RAW_DATA_DIR`: Directory to save the downloaded data (default: `data/raw`).
- `FEATURES_DIR`: Directory to save the extracted features (default: `data/features`).
- `ZIPS_DIR`: Temporary directory for storing downloaded zip files (default: `data/zips`).

### Download Data

To only download speech data for specific languages:

```bash
make download LANGUAGES="pl en" DATA_SIZE=2
```

- `LANGUAGES`: List of languages to download (e.g., `"pl en"`).
- `DATA_SIZE`: Total size of the dataset in GB (e.g., `2`).
- `RAW_DATA_DIR`: Directory to save the downloaded data (default: `data/raw`).
- `ZIPS_DIR`: Temporary directory for storing downloaded zip files (default: `data/zips`).

### Extract Features

To only extract features from already downloaded data:

```bash
make extract LANGUAGES="pl en" FEATURES="pitch mfcc"
```

- `LANGUAGES`: List of languages to extract features for (e.g., `"pl en"`).
- `FEATURES`: List of features to extract (e.g., `"pitch mfcc"`). If not provided, all available features will be extracted.
- `RAW_DATA_DIR`: Directory where the downloaded data is stored (default: `data/raw`).
- `FEATURES_DIR`: Directory to save the extracted features (default: `data/features`).

### List Available Languages

To list all available languages from Mozilla Common Voice:

```bash
make list-languages
```

### List Available Features

To list all available features that can be extracted:

```bash
make list-features
```

## Directory Structure

- `data/raw`: Stores raw, downloaded audio files.
- `data/features`: Contains extracted features (e.g., pitch, MFCC) in CSV format.
- `data/zips`: Temporary folder for downloaded zip files.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
