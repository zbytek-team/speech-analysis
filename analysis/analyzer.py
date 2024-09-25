from pathlib import Path
import importlib
import logging
import librosa
from .individual_analyses.analysis_base import AnalysisBase
import polars as pl

class Analyzer:
    def __init__(self, df: pl.DataFrame, language_dir: Path, clips_dir: Path, output_dir: Path):
        self.language_dir = language_dir
        self.gender: str = df.select(pl.col("gender")).item(0,0)
        self.df = df
        self.audio_dir = clips_dir
        self.output_dir = output_dir
        self.analysis_classes = self._load_analysis_classes()
        self.preprocessed_audio = self._load_and_preprocess_audio()

    def _load_and_preprocess_audio(self):
        logging.info(f"Preprocessing audio for {self.language_dir.name} ({self.gender})")

        preprocessed_audio = {}
        for row in self.df.iter_rows(named=True):
            file_path = self.audio_dir / row['path']
            try:
                # Load the audio file
                y, sr = librosa.load(file_path, sr=None)
                
                # Trim silence
                y_trimmed, _ = librosa.effects.trim(y)
                
                # Normalize audio
                y_normalized = librosa.util.normalize(y_trimmed)
                
                # Store preprocessed audio data
                preprocessed_audio[row['path']] = (y_normalized, sr)
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
        
        logging.info(f"Preprocessed {len(preprocessed_audio)} audio files for {self.language_dir.name} ({self.gender})")

        return preprocessed_audio

    def _load_analysis_classes(self):
        analyses_dir = Path(__file__).parent / 'individual_analyses'
        analysis_classes = []

        for file_path in analyses_dir.glob("*_analysis.py"):
            module_name = f"analysis.individual_analyses.{file_path.stem}"
            module = importlib.import_module(module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, AnalysisBase) and attr is not AnalysisBase:
                    analysis_classes.append(attr)

        return analysis_classes

    def run_analyses(self):
        for AnalysisClass in self.analysis_classes:
            analysis_instance = AnalysisClass(self.preprocessed_audio, self.output_dir)
            logging.info(f"Running {AnalysisClass.__name__} for {self.language_dir} ({self.gender})")
            analysis_instance.run()
            logging.info(f"Completed {AnalysisClass.__name__} for {self.language_dir} ({self.gender})")
