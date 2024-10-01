import parselmouth
from pathlib import Path
from tqdm import tqdm
from feature_extraction.base_extractor import BaseExtractor

class PitchExtractor(BaseExtractor):
    def extract(self, source: Path, feature_list: list[dict]):
        """Extract pitch from audio files and update the shared feature list."""
        for file_dict in tqdm(feature_list, desc="Extracting Pitch"):
            file_name = file_dict["file"]
            audio_path = source / file_name
            snd = parselmouth.Sound(str(audio_path))
            pitch = snd.to_pitch()

            pitch_values = pitch.selected_array['frequency']
            pitch_mean = pitch_values.mean() if pitch_values.size > 0 else 0

            file_dict["pitch_mean"] = pitch_mean

