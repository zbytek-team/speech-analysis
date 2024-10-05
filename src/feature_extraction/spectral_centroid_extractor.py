import numpy as np
import librosa
from feature_extraction.base_extractor import BaseExtractor

class SpectralCentroidExtractor(BaseExtractor):
    def extract(self, audio: np.ndarray, sr: int | float) -> dict:
        try:
            spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
            sc_mean = np.mean(spectral_centroid)
            sc_var = np.var(spectral_centroid)

            spectral_centroid_features = {
                "spectral_centroid_mean": sc_mean,
                "spectral_centroid_var": sc_var
            }
            return spectral_centroid_features
        except Exception as e:
            return {"error": str(e)}
