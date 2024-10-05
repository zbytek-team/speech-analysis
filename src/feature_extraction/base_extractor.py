import librosa
import numpy as np
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, audio: np.ndarray, sr: int | float) -> dict[str, float]:
        """
        Extract features from the provided audio data.
        
        Parameters:
            audio (numpy.ndarray): The audio signal from which to extract features.
            sr (int): The sampling rate of the audio signal.
        
        Returns:
            dict: A dictionary of extracted features.
        """
        pass