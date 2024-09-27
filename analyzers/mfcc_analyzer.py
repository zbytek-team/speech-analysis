from .base_analyzer import BaseAnalyzer
import librosa
import numpy as np


class MFCCAnalyzer(BaseAnalyzer):
    def analyze(self, audio_path):
        y, sr = librosa.load(audio_path, sr=None)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mean_mfccs = np.mean(mfccs, axis=1)
        mfcc_dict = {f'mfcc_{i+1}': mfcc for i, mfcc in enumerate(mean_mfccs)}
        
        return mfcc_dict

