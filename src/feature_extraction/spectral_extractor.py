import librosa
from pathlib import Path
from tqdm import tqdm
from feature_extraction.base_extractor import BaseExtractor

class SpectralExtractor(BaseExtractor):
    def extract(self, source: Path, feature_list: list[dict]):
        """Extract spectral features from audio files and update the shared feature list."""
        for file_dict in tqdm(feature_list, desc="Extracting Spectral Features"):
            file_name = file_dict["file"]
            audio_path = source / file_name
            y, sr = librosa.load(str(audio_path))
            centroid = librosa.feature.spectral_centroid(y=y, sr=sr).mean()
            bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr).mean()

            file_dict["spectral_centroid"] = centroid
            file_dict["spectral_bandwidth"] = bandwidth

