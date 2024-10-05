import numpy as np
import librosa
from feature_extraction.base_extractor import BaseExtractor

class SpectralContrastExtractor(BaseExtractor):
    def extract(self, audio: np.ndarray, sr: int | float) -> dict:
        try:
            spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
            sc_mean = np.mean(spectral_contrast, axis=1)
            sc_var = np.var(spectral_contrast, axis=1)

            spectral_contrast_features = {
                "spectral_contrast_mean": sc_mean,
                "spectral_contrast_var": sc_var
            }
            return spectral_contrast_features
        except Exception as e:
            return {"error": str(e)}
