import librosa
import numpy as np
from pathlib import Path
from feature_extraction.base_extractor import BaseExtractor

class SpectralExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        y, sr = librosa.load(file, sr=None)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        entry['spectral_centroid_mean'] = np.mean(spectral_centroid)
