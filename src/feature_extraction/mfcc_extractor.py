import numpy as np
import librosa
from feature_extraction.base_extractor import BaseExtractor

class MFCCExtractor(BaseExtractor):
    def extract(self, audio: np.ndarray, sr: int | float) -> dict:
        try:
            mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfccs, axis=1)
            mfcc_var = np.var(mfccs, axis=1)

            mfcc_features = {
                "mfcc_mean": mfcc_mean,
                "mfcc_var": mfcc_var
            }
            return mfcc_features
        except Exception as e:
            return {"error": str(e)}
