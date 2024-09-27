from .base_analyzer import BaseAnalyzer
import librosa
import numpy as np

class PitchAnalyzer(BaseAnalyzer):
    def analyze(self, audio_path):
        y, sr = librosa.load(audio_path, sr=None)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = pitches[magnitudes > np.median(magnitudes)]
        mean_pitch = np.mean(pitch_values) if len(pitch_values) > 0 else 0
        return {'mean_pitch': mean_pitch}

