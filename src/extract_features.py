import argparse
import logging
from pathlib import Path
import pandas as pd
from feature_extraction.pitch_extractor import PitchExtractor
from feature_extraction.mfcc_extractor import MFCCExtractor
from feature_extraction.formant_extractor import FormantExtractor
from feature_extraction.hnr_extractor import HNRExtractor
from feature_extraction.spectral_extractor import SpectralExtractor
from feature_extraction.zero_crossing_extractor import ZeroCrossingExtractor
from utils.logging_setup import setup_logging
from utils.constants import GENDERS

setup_logging()


def extract_features(language: str, source: Path, destination: Path, features: list[str]):
    """Extract features for a given language and save them as gender-specific CSV files."""
    for gender in GENDERS:
        gender_path = source / gender
        if not gender_path.exists():
            logging.warning(f"No data found for gender: {gender} in language: {language}")
            continue
        
        audio_files = list(gender_path.glob("**/*.mp3"))
        
        if not audio_files:
            logging.warning(f"No audio files found for gender: {gender} in language: {language}")
            continue

        feature_list = [{"file": file.name} for file in audio_files]
        
        extractors = {
            "pitch": PitchExtractor(),
            "mfcc": MFCCExtractor(),
            "formant": FormantExtractor(),
            "hnr": HNRExtractor(),
            "spectral": SpectralExtractor(),
            "zero_crossing": ZeroCrossingExtractor(),
        }
        
        for feature in features:
            if feature in extractors:
                logging.info(f"Extracting {feature} for language: {language}, gender: {gender}")
                extractors[feature].extract(gender_path, feature_list)
        
        df = pd.DataFrame(feature_list)
        gender_csv_name = f"{language}_{gender}_features.csv"
        df.to_csv(destination / gender_csv_name, index=False)

        logging.info(f"Saved features for language: {language}, gender: {gender} to {gender_csv_name}")


def main():
    parser = argparse.ArgumentParser(description="Extract features from preprocessed speech data.")
    parser.add_argument("--languages", nargs="+", required=True, help="List of languages to extract features for")
    parser.add_argument("--source", type=str, default="data/processed", help="Path to preprocessed data")
    parser.add_argument("--destination", type=str, default="data/features", help="Path to save extracted features")
    parser.add_argument("--features", nargs="+", required=True, help="List of features to extract (e.g., pitch, mfcc, formant)")

    args = parser.parse_args()

    languages = args.languages
    features = args.features
    source_dir = Path(args.source)
    destination_dir = Path(args.destination)

    for language in languages:
        extract_features(language, source_dir / language, destination_dir, features)


if __name__ == "__main__":
    main()

