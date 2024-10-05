import numpy as np
import librosa
from feature_extraction.base_extractor import BaseExtractor

class PitchExtractor(BaseExtractor):
    def extract(self, audio: np.ndarray, sr: int | float) -> dict:
        try:
            pitches, magnitudes = librosa.core.piptrack(y=audio, sr=sr)
            pitch_mean = np.mean([np.max(pitch) for pitch in pitches if np.max(pitch) > 0])
            pitch_var = np.var([np.max(pitch) for pitch in pitches if np.max(pitch) > 0])

            pitch_features = {
                "pitch_mean": pitch_mean,
                "pitch_var": pitch_var
            }
            return pitch_features
        except Exception as e:
            return {"error": str(e)}
