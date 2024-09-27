from .base_analyzer import BaseAnalyzer
import librosa
import numpy as np


class ZeroCrossingAnalyzer(BaseAnalyzer):
    def analyze(self, audio_path):
        y, _ = librosa.load(audio_path, sr=None)
        zcr = librosa.feature.zero_crossing_rate(y)
        mean_zcr = np.mean(zcr)
        
        return {'mean_zero_crossing_rate': mean_zcr}

