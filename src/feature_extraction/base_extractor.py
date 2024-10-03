from abc import ABC, abstractmethod
from pathlib import Path

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, source: Path, feature_list: list[dict]):
        """Extract features from the source and update the shared feature list."""
        pass

