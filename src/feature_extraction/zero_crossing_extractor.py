import librosa
from pathlib import Path
from feature_extraction.base_extractor import BaseExtractor

class ZeroCrossingExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        y, _ = librosa.load(file, sr=None)
        zcr = librosa.feature.zero_crossing_rate(y)
        entry['zero_crossing_rate'] = zcr.mean()
