import argparse
import logging
from pathlib import Path
from typing import Any
import pandas as pd
from tqdm import tqdm

from utils.logging_utils import setup_logging
from utils.file_utils import ensure_directory_exists

from analyzers.base_analyzer import BaseAnalyzer

from analyzers.pitch_analyzer import PitchAnalyzer
from analyzers.formant_analyzer import FormantAnalyzer
from analyzers.spectral_analyzer import SpectralAnalyzer
from analyzers.mfcc_analyzer import MFCCAnalyzer
from analyzers.zero_crossing_analyzer import ZeroCrossingAnalyzer
from analyzers.hnr_analyzer import HarmonicToNoiseRatioAnalyzer

ANALYZER_MAP = {
    'pitch': PitchAnalyzer,
    'formant': FormantAnalyzer,
    'spectral': SpectralAnalyzer,
    'mfcc': MFCCAnalyzer,
    'zero_crossing': ZeroCrossingAnalyzer,
    'hnr': HarmonicToNoiseRatioAnalyzer,
}

setup_logging()


def analyze_language_data(languages: list[str], data_dir: str, output_dir: str, selected_analyzers: list[str]):
    analyzers: list[BaseAnalyzer] = [ANALYZER_MAP[name]() for name in selected_analyzers]
    ensure_directory_exists(Path(output_dir))

    for language in languages:
        language_dir = Path(data_dir) / language
        if not language_dir.exists():
            logging.warning(f"Language directory not found: {language_dir}")
            continue

        genders = [d.name for d in language_dir.iterdir() if d.is_dir()]
        for gender in genders:
            audio_dir = language_dir / gender
            if not audio_dir.exists():
                logging.warning(f"Directory not found: {audio_dir}")
                continue

            audio_files = list(audio_dir.glob('*.mp3'))
            stats: list[dict[str, Any]] = []

            for audio_file in tqdm(audio_files, desc=f"Analyzing {language}-{gender}"):
                file_stats = {'file': audio_file.name, 'language': language, 'gender': gender}

                for analyzer in analyzers:
                    try:
                        analysis_result = analyzer.analyze(audio_file)
                        file_stats.update(analysis_result)
                    except Exception as e:
                        logging.error(f"Error analyzing {audio_file} with {analyzer.__class__.__name__}: {e}")
                        continue

                stats.append(file_stats)

            output_file = Path(output_dir) / f"{language}_{gender}_stats.csv"
            df = pd.DataFrame(stats)
            df.to_csv(output_file, index=False)
            logging.info(f"Saved statistics to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Analyze preprocessed audio data and extract statistics.")
    parser.add_argument("--languages", nargs="+", required=True, help="List of languages to analyze")
    parser.add_argument("--data_dir", type=str, default="data", help="Path to the preprocessed data directory")
    parser.add_argument("--output_dir", type=str, default="analysis_results", help="Path to save analysis results")
    parser.add_argument("--analyzers", nargs="+", required=True, choices=ANALYZER_MAP.keys(),
                        help="List of analyzers to run")
    args = parser.parse_args()

    analyze_language_data(args.languages, args.data_dir, args.output_dir, args.analyzers)


if __name__ == "__main__":
    main()

