import numpy as np
import librosa
from feature_extraction.base_extractor import BaseExtractor

class SpectralFlatnessExtractor(BaseExtractor):
    def extract(self, audio: np.ndarray, sr: int | float) -> dict:
        try:
            spectral_flatness = librosa.feature.spectral_flatness(y=audio)[0]
            sf_mean = np.mean(spectral_flatness)
            sf_var = np.var(spectral_flatness)

            spectral_flatness_features = {
                "spectral_flatness_mean": sf_mean,
                "spectral_flatness_var": sf_var
            }
            return spectral_flatness_features
        except Exception as e:
            return {"error": str(e)}
