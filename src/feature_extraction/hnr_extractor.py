import parselmouth
from pathlib import Path
from tqdm import tqdm
from feature_extraction.base_extractor import BaseExtractor

class HNRExtractor(BaseExtractor):
    def extract(self, source: Path, feature_list: list[dict]):
        """Extract Harmonic-to-Noise Ratio (HNR) from audio files and update the shared feature list."""
        for file_dict in tqdm(feature_list, desc="Extracting HNR"):
            file_name = file_dict["file"]
            audio_path = source / file_name
            snd = parselmouth.Sound(str(audio_path))
            hnr = snd.to_harmonicity_cc()

            hnr_mean = hnr.values.mean() if hnr.values.size > 0 else 0
            file_dict["hnr_mean"] = hnr_mean

