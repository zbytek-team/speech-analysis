import librosa
from pathlib import Path
from tqdm import tqdm
from feature_extraction.base_extractor import BaseExtractor

class ZeroCrossingExtractor(BaseExtractor):
    def extract(self, source: Path, feature_list: list[dict]):
        """Extract Zero Crossing Rate from audio files and update the shared feature list."""
        for file_dict in tqdm(feature_list, desc="Extracting Zero Crossing Rate"):
            file_name = file_dict["file"]
            audio_path = source / file_name
            y, _ = librosa.load(str(audio_path))
            zcr = librosa.feature.zero_crossing_rate(y).mean()

            file_dict["zero_crossing_rate"] = zcr

