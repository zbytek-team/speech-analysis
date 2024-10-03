import parselmouth
from pathlib import Path
from tqdm import tqdm
from feature_extraction.base_extractor import BaseExtractor

class FormantExtractor(BaseExtractor):
    def extract(self, source: Path, feature_list: list[dict]):
        """Extract formant frequencies from audio files and update the shared feature list."""
        for file_dict in tqdm(feature_list, desc="Extracting Formants"):
            file_name = file_dict["file"]
            audio_path = source / file_name
            snd = parselmouth.Sound(str(audio_path))
            formant = snd.to_formant_burg()

            file_dict["f1_mean"] = formant.get_mean(1) if formant.get_mean(1) else 0
            file_dict["f2_mean"] = formant.get_mean(2) if formant.get_mean(2) else 0
            file_dict["f3_mean"] = formant.get_mean(3) if formant.get_mean(3) else 0

