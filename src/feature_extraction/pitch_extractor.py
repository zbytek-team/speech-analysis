import parselmouth
from pathlib import Path
from feature_extraction.base_extractor import BaseExtractor

class PitchExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        sound = parselmouth.Sound(str(file))
        pitch = sound.to_pitch()
        entry['pitch_mean'] = pitch.get_mean()
        entry['pitch_min'] = pitch.get_minimum()
        entry['pitch_max'] = pitch.get_maximum()
