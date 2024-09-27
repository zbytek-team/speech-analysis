from .base_analyzer import BaseAnalyzer
import parselmouth
import numpy as np

class HarmonicToNoiseRatioAnalyzer(BaseAnalyzer):
    def analyze(self, audio_path):
        snd = parselmouth.Sound(str(audio_path))
        harmonicity = snd.to_harmonicity()
        hnr_values = harmonicity.values[harmonicity.values != -200]  # Exclude undefined values
        mean_hnr = np.mean(hnr_values) if hnr_values.size > 0 else 0
        return {'mean_hnr': mean_hnr}

