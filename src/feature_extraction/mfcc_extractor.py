import librosa
from pathlib import Path
from tqdm import tqdm
from feature_extraction.base_extractor import BaseExtractor

class MFCCExtractor(BaseExtractor):
    def extract(self, source: Path, feature_list: list[dict]):
        """Extract MFCCs from audio files and update the shared feature list."""
        for file_dict in tqdm(feature_list, desc="Extracting MFCCs"):
            file_name = file_dict["file"]
            audio_path = source / file_name
            y, sr = librosa.load(str(audio_path))
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = mfccs.mean(axis=1)

            for i in range(13):
                file_dict[f"mfcc_{i+1}"] = mfcc_mean[i]

