import os
import logging
import argparse
from utils.file_utils import load_validated_data
from analysis.analyzer import Analyzer
from utils.file_utils import ensure_directory_exists, delete_directory_if_exists
from utils.logging_utils import setup_logging

setup_logging()

# Constants
DEFAULT_DATA_DIR = 'data'
DEFAULT_OUTPUT_DIR = 'plots'

def main():
    parser = argparse.ArgumentParser(description="Analyze audio data from Mozilla Common Voice.")
    parser.add_argument("--data_dir", type=str, default=DEFAULT_DATA_DIR, help="Path to the input data directory.")
    parser.add_argument("--output_dir", type=str, default=DEFAULT_OUTPUT_DIR, help="Path to the output directory for plots.")
    args = parser.parse_args()

    data_dir = args.data_dir
    output_dir = args.output_dir

    # Iterate over each language directory in the data directory
    for language in os.listdir(data_dir):
        lang_path = os.path.join(data_dir, language)
        if not os.path.isdir(lang_path):
            continue

        logging.info(f"Processing language: {language}")
        

        # Check if the validated data file exists for the current language
        if not os.path.exists(os.path.join(lang_path, 'validated.tsv')):
            logging.warning(f"Validated data file not found for language: {language}. Skipping...")
            continue

        # Load validated data for the current language
        validated_data_path = os.path.join(lang_path, 'validated.tsv')
        df = load_validated_data(validated_data_path)

        # Process each gender separately
        for gender in ['male', 'female']:
            # Filter DataFrame for the current gender
            gender_df = df[df['gender'].str.contains(gender, na=False)]
            if gender_df.empty:
                continue

            # Define output path for plots
            output_path = os.path.join(output_dir, language, gender)
            
            # Clear existing output directory if it exists, or create a new one
            if os.path.exists(output_path):
                delete_directory_if_exists(output_path)
            ensure_directory_exists(output_path)

            audio_dir = os.path.join(lang_path, 'clips')
            
            # Initialize the Analyzer with loaded data and paths
            analyzer = Analyzer(language, gender, gender_df, audio_dir, output_path)
            
            # Run analyses for the current language and gender
            analyzer.run_analyses()

        logging.info(f"Completed processing for language: {language}")

if __name__ == '__main__':
    main()
