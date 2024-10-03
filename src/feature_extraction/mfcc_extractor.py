import librosa
import numpy as np
from pathlib import Path
from feature_extraction.base_extractor import BaseExtractor

class MFCCExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        y, sr = librosa.load(file, sr=None)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        entry['mfcc_mean'] = np.mean(mfccs, axis=1).tolist()  
