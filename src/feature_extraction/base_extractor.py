from abc import ABC, abstractmethod
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import logging

class BaseExtractor(ABC):
    def extract(self, source: Path, feature_list: list[dict], max_workers=4):
        """Extract features from the source and update the shared feature list concurrently."""
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            with tqdm(total=len(feature_list), desc=f"Extracting {self.__class__.__name__}") as pbar:
                futures = [
                    executor.submit(self.extract_single, source / entry["file"], entry)
                    for entry in feature_list
                ]
                for future in futures:
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(f"Error processing file: {e}")
                    finally:
                        pbar.update(1)

    @abstractmethod
    def extract_single(self, file: Path, entry: dict):
        """Extract features from a single file and update the given entry."""
        pass

