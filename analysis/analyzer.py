import os
import importlib
import logging
import librosa
from .specific_analyses.analysis_base import AnalysisBase

class Analyzer:
    def __init__(self, language: str, gender: str, df, audio_dir: str, output_dir: str):
        """
        Initialize the Analyzer with language, gender, data, and directory paths.

        :param language: The language being processed.
        :param gender: The gender being processed.
        :param df: DataFrame containing metadata about audio files.
        :param audio_dir: Directory where the audio files are stored.
        :param output_dir: Directory to save analysis results.
        """
        self.language = language
        self.gender = gender
        self.df = df
        self.audio_dir = audio_dir
        self.output_dir = output_dir
        self.analysis_classes = self._load_analysis_classes()
        self.preprocessed_audio = self._load_and_preprocess_audio()

    def _load_and_preprocess_audio(self):
        """
        Load and preprocess audio files in-memory for analysis.

        :return: Dictionary mapping file paths to preprocessed audio data and sample rates.
        """
        preprocessed_audio = {}
        for _, row in self.df.iterrows():
            file_path = os.path.join(self.audio_dir, row['path'])
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
        return preprocessed_audio

    def _load_analysis_classes(self):
        """
        Dynamically load all analysis classes from the specific_analyses directory.

        :return: A list of analysis class types.
        """
        analyses_dir = os.path.join(os.path.dirname(__file__), 'specific_analyses')
        analysis_classes = []

        for file_name in os.listdir(analyses_dir):
            if file_name.endswith('_analysis.py'):
                module_name = f"analysis.specific_analyses.{file_name[:-3]}"
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, AnalysisBase) and attr is not AnalysisBase:
                        analysis_classes.append(attr)

        return analysis_classes

    def run_analyses(self):
        """
        Run all loaded analyses on the preprocessed audio data.
        """
        for AnalysisClass in self.analysis_classes:
            analysis_instance = AnalysisClass(self.preprocessed_audio, self.output_dir)
            logging.info(f"Running {AnalysisClass.__name__} for {self.language} ({self.gender})")
            analysis_instance.run()
            logging.info(f"Completed {AnalysisClass.__name__} for {self.language} ({self.gender})")
