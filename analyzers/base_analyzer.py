from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, audio_path):
        pass

