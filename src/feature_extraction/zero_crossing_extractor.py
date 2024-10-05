import numpy as np
import librosa
from feature_extraction.base_extractor import BaseExtractor

class ZeroCrossingExtractor(BaseExtractor):
    def extract(self, audio: np.ndarray, sr: int | float) -> dict:
        try:
            zero_crossings = librosa.feature.zero_crossing_rate(audio)[0]
            zcr_mean = np.mean(zero_crossings)
            zcr_var = np.var(zero_crossings)

            
            zero_crossing_features = {
                "zcr_mean": zcr_mean,
                "zcr_var": zcr_var,

            }
            return zero_crossing_features
        except Exception as e:
            return {"error": str(e)}