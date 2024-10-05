import argparse
import logging
from pathlib import Path
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import librosa
from tqdm import tqdm
from feature_extraction.base_extractor import BaseExtractor
from feature_extraction.pitch_extractor import PitchExtractor
from feature_extraction.mfcc_extractor import MFCCExtractor
from feature_extraction.harmonic_noise_ratio_extractor import HarmonicNoiseRatioExtractor
from feature_extraction.spectral_centroid_extractor import SpectralCentroidExtractor
from feature_extraction.spectral_bandwidth_extractor import SpectralBandwidthExtractor
from feature_extraction.spectral_flatness_extractor import SpectralFlatnessExtractor
from feature_extraction.spectral_contrast_extractor import SpectralContrastExtractor
from feature_extraction.chroma_extractor import ChromaExtractor
from feature_extraction.zero_crossing_extractor import ZeroCrossingExtractor
from utils.file_manager import ensure_directory_exists
from utils.logging_setup import setup_logging

setup_logging()

def get_available_extractors() -> dict[str, BaseExtractor]:
    return {
        "pitch": PitchExtractor(),
        "mfcc": MFCCExtractor(),
        "hnr": HarmonicNoiseRatioExtractor(),
        "spectral_centroid": SpectralCentroidExtractor(),
        "spectral_bandwidth": SpectralBandwidthExtractor(),
        "spectral_flatness": SpectralFlatnessExtractor(),
        "spectral_contrast": SpectralContrastExtractor(),
        "chroma": ChromaExtractor(),
        "zero_crossing": ZeroCrossingExtractor(),
    }

def extract_features(language: str, source: Path, destination: Path, features: list[str] | None = None):
    validated_tsv_path = source / "validated.tsv"
    
    if not validated_tsv_path.exists():
        logging.warning(f"validated.tsv not found for language {language}")
        return

    df = load_metadata(validated_tsv_path)

    extractors = get_available_extractors()

    if features is None:
        features = list(extractors.keys())

    extractors = {k: v for k, v in extractors.items() if k in features}

    results = []

    def process_row(row):
        file_path = source / "clips" / row['path']
        row_results = {"path": row['path'], "gender": row['gender'], "age": row['age']}
        
        try:
            audio, sr = librosa.load(file_path, sr=None)

            audio_trimmed, _ = librosa.effects.trim(audio)

            for feature_name, extractor in extractors.items():
                extracted_features = extractor.extract(audio_trimmed, sr)
                row_results.update(extracted_features)
        except Exception as e:
            logging.error(f"Error processing {row['path']}: {e}")
            return None
        
        return row_results

    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_row, [row for _, row in df.iterrows()]), total=len(df), desc=f"Extracting features for {language}"))

    results = [res for res in results if res is not None]

    results_df = pd.DataFrame(results)
    gender_csv_name = f"{language}_features.csv"
    results_df.to_csv(destination / gender_csv_name, index=False)


def load_metadata(validated_tsv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(validated_tsv_path, sep='\t', usecols=["path", "gender", "age"])  # type: ignore
    df = df.dropna()

    df = df[df['path'].str.endswith('.mp3')]

    return df


def main():
    parser = argparse.ArgumentParser(description="Extract features from preprocessed speech data.")
    parser.add_argument("--languages", nargs="+", required=True, help="List of languages to extract features for")
    parser.add_argument("--source", type=str, default="data/raw", help="Path to preprocessed data")
    parser.add_argument("--destination", type=str, default="data/features", help="Path to save extracted features")
    parser.add_argument("--features", nargs="*", help="List of features to extract (e.g., pitch, mfcc, formant). If not provided, all features will be extracted.")
    parser.add_argument("--list-features", action="store_true", help="List available features and exit")

    args = parser.parse_args()

    if args.list_features:
        extractors = get_available_extractors()
        print("Available features:")
        for feature_name in extractors.keys():
            print(f" - {feature_name}")
        return

    languages: list[str] = args.languages
    features: list[str] | None = args.features if args.features else None
    source_dir = Path(args.source)
    destination_dir = Path(args.destination)
    
    ensure_directory_exists(destination_dir)

    for language in languages:
        extract_features(language, source_dir / language, destination_dir, features)


if __name__ == "__main__":
    main()
