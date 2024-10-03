import parselmouth
from pathlib import Path
from feature_extraction.base_extractor import BaseExtractor

class HNRExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        sound = parselmouth.Sound(str(file))
        hnr = sound.to_harmonicity_cc()
        entry['hnr'] = hnr.values.mean() if hnr.values.size > 0 else 0
