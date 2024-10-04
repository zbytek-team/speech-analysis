import parselmouth
import logging
from pathlib import Path
import numpy as np
from feature_extraction.base_extractor import BaseExtractor

class FormantExtractor(BaseExtractor):
    def extract_single(self, file: Path, entry: dict):
        """Extract average formants from a single audio file."""
        snd = parselmouth.Sound(str(file))
        
        formant = snd.to_formant_burg()

        duration = snd.get_total_duration()

        num_points = 5
        time_points = np.linspace(0, duration, num_points)

        f1_values = []
        f2_values = []
        f3_values = []

        for time in time_points:
            f1 = formant.get_value_at_time(1, time)
            f2 = formant.get_value_at_time(2, time)
            f3 = formant.get_value_at_time(3, time)

            if f1 is not None:
                f1_values.append(f1)
            if f2 is not None:
                f2_values.append(f2)
            if f3 is not None:
                f3_values.append(f3)

        entry["f1"] = np.mean(f1_values) if f1_values else 'NA'
        entry["f2"] = np.mean(f2_values) if f2_values else 'NA'
        entry["f3"] = np.mean(f3_values) if f3_values else 'NA'
       

