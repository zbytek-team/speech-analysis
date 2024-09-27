from .base_analyzer import BaseAnalyzer
import librosa
import numpy as np


class SpectralAnalyzer(BaseAnalyzer):
    def analyze(self, audio_path):
        y, sr = librosa.load(audio_path, sr=None)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        mean_centroid = np.mean(spectral_centroid)
        
        return {'mean_spectral_centroid': mean_centroid}

