import numpy as np
import librosa
from feature_extraction.base_extractor import BaseExtractor

class HarmonicNoiseRatioExtractor(BaseExtractor):
    def extract(self, audio: np.ndarray, sr: int | float) -> dict:
        try:
            harmonic_signal = librosa.effects.harmonic(y=audio)
            hnr_mean = np.mean(harmonic_signal)
            hnr_var = np.var(harmonic_signal)

            hnr_features = {
                "hnr_mean": hnr_mean,
                "hnr_var": hnr_var
            }
            return hnr_features
        except Exception as e:
            return {"error": str(e)}
