# Speech Analysis Project

This research project at the Gdańsk University of Technology aims to develop a method for identifying characteristic frequency ranges for different languages. The goal is to review methods of speech frequency analysis and, based on speech recordings for various languages, verify Dr. Alfred Tomatis's theory that different languages have distinct frequency ranges for specific phonemes.

## Requirements

- Python 3.12


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

This project uses a `Makefile` to streamline various tasks like downloading datasets, preprocessing data, extracting features, and cleaning temporary files.

### Download Data

To download speech data for specific languages:

```bash
make download LANGUAGES="pl en" DATA_SIZE=2
```

- `LANGUAGES`: List of languages to download (e.g., `"pl en"`).
- `DATA_SIZE`: Total size of the dataset in GB (e.g., `2`).
- `DEST_DIR`: Directory to save the downloaded data (default: `data/raw`).
- `ZIPS_DIR`: Temporary directory for storing downloaded zip files (default: `data/zips`).

### Preprocess Data

To preprocess downloaded data (remove silence, organize by gender):

```bash
make preprocess LANGUAGES="pl en"
```

- `LANGUAGES`: List of languages to preprocess.
- `DEST_DIR`: Directory to save preprocessed data (default: `data/processed`).

### Extract Features

To extract features like pitch, MFCC, formants, and others:

```bash
make extract LANGUAGES="pl en" FEATURES="pitch mfcc formant"
```

- `LANGUAGES`: List of languages to extract features for.
- `FEATURES`: List of features to extract (e.g., `pitch mfcc formant`).
- `DEST_DIR`: Directory to save the extracted features (default: `data/features`).

### List Available Languages

To list all available languages from Mozilla Common Voice:

```bash
make list-languages
```

### Clean Zip Files

To delete the `zips` directory containing the downloaded `.tar.gz` files after processing:

```bash
make clean-zips
```

## Directory Structure

- `data/raw`: Stores raw, downloaded audio files.
- `data/processed`: Contains preprocessed audio files (organized by gender).
- `data/features`: Contains extracted features (e.g., pitch, MFCC) in CSV format.
- `data/zips`: Temporary folder for downloaded zip files.

## Additional Notes

- You can adjust the `DEST_DIR` for all commands to point to a custom location.
- The `ZIPS_DIR` can also be set to manage where zip files are temporarily stored.
- Features include `pitch`, `mfcc`, `formant`, `hnr`, `spectral`, and `zero_crossing`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
