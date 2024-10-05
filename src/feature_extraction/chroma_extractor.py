import numpy as np
import librosa
from feature_extraction.base_extractor import BaseExtractor

class ChromaExtractor(BaseExtractor):
    def extract(self, audio: np.ndarray, sr: int | float) -> dict:
        try:
            chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
            chroma_mean = np.mean(chroma, axis=1)
            chroma_var = np.var(chroma, axis=1)

            chroma_features = {
                "chroma_mean": chroma_mean,
                "chroma_var": chroma_var
            }
            return chroma_features
        except Exception as e:
            return {"error": str(e)}
