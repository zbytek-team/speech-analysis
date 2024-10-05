import numpy as np
import librosa
from feature_extraction.base_extractor import BaseExtractor

class SpectralBandwidthExtractor(BaseExtractor):
    def extract(self, audio: np.ndarray, sr: int | float) -> dict:
        try:
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr)[0]
            sb_mean = np.mean(spectral_bandwidth)
            sb_var = np.var(spectral_bandwidth)

            spectral_bandwidth_features = {
                "spectral_bandwidth_mean": sb_mean,
                "spectral_bandwidth_var": sb_var
            }
            return spectral_bandwidth_features
        except Exception as e:
            return {"error": str(e)}
