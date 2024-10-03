import librosa
from pathlib import Path
from feature_extraction.base_extractor import BaseExtractor

class SpectralExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        y, sr = librosa.load(file, sr=None)
        centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
        bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()

        entry["spectral_centroid"] = centroid
        entry["spectral_bandwidth"] = bandwidth

