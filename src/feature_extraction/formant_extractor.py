import parselmouth
from pathlib import Path
from feature_extraction.base_extractor import BaseExtractor

class FormantExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        sound = parselmouth.Sound(str(file))
        formant = sound.to_formant_burg()

        entry['f1_mean'] = formant.get_mean(1) if formant.get_mean(1) else 0
        entry['f2_mean'] = formant.get_mean(2) if formant.get_mean(2) else 0        
        entry['f3_mean'] = formant.get_mean(3) if formant.get_mean(3) else 0
