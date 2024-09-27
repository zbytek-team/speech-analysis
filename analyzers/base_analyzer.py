from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path

class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, audio_path: Path) -> dict[str, Any]:
        pass

