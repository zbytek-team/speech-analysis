import parselmouth
from pathlib import Path
from feature_extraction.base_extractor import BaseExtractor

class PitchExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        sound = parselmouth.Sound(str(file))
        pitch = sound.to_pitch()

        pitch_values = pitch.selected_array['frequency']
        entry["pitch_mean"] = pitch_values.mean() if pitch_values.size > 0 else 0
