import parselmouth
from pathlib import Path
from feature_extraction.base_extractor import BaseExtractor

class FormantExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        sound = parselmouth.Sound(str(file))
        formant = sound.to_formant_burg()

        entry['f1'] = formant.get_value_at_time(1, 0.5)
        entry['f2'] = formant.get_value_at_time(2, 0.5)
        entry['f3'] = formant.get_value_at_time(3, 0.5)

