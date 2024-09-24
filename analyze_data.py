import logging
import argparse
from pathlib import Path
from utils.file_utils import load_validated_data, ensure_directory_exists, delete_directory_if_exists
from analysis.analyzer import Analyzer
from utils.logging_utils import setup_logging

setup_logging()

# Constants
DEFAULT_DATA_DIR = Path('data')
DEFAULT_OUTPUT_DIR = Path('plots')

def main():
    parser = argparse.ArgumentParser(description="Analyze audio data from Mozilla Common Voice.")
    parser.add_argument("--data_dir", type=Path, default=DEFAULT_DATA_DIR, help="Path to the input data directory.")
    parser.add_argument("--output_dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Path to the output directory for plots.")
    args = parser.parse_args()

    data_dir = args.data_dir
    output_dir = args.output_dir

    # Iterate over each language directory in the data directory
    for language_dir in data_dir.iterdir():
        if not language_dir.is_dir():
            continue

        logging.info(f"Processing language: {language_dir.name}")

        # Check if the validated data file exists for the current language
        validated_data_path = language_dir / 'validated.tsv'
        if not validated_data_path.exists():
            logging.warning(f"Validated data file not found for language: {language_dir.name}. Skipping...")
            continue

        # Load validated data for the current language
        df = load_validated_data(validated_data_path)

        # Process each gender separately
        for gender in ['male', 'female']:
            # Filter DataFrame for the current gender
            gender_df = df[df['gender'].str.contains(gender, na=False)]
            if gender_df.empty:
                continue

            # Define output path for plots
            output_path = output_dir / language_dir.name / gender

            # Clear existing output directory if it exists, or create a new one
            if output_path.exists():
                delete_directory_if_exists(output_path)
            ensure_directory_exists(output_path)

            
            # Initialize the Analyzer with loaded data and paths
            analyzer = Analyzer(language, gender, gender_df, audio_dir, output_path)
            
            # Run analyses for the current language and gender
            analyzer.run_analyses()
            audio_dir = language_dir / 'clips'

        logging.info(f"Completed processing for language: {language_dir.name}")

if __name__ == '__main__':
    main()
