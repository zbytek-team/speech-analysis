from .base_analyzer import BaseAnalyzer
import parselmouth
import numpy as np

class FormantAnalyzer(BaseAnalyzer):
    def analyze(self, audio_path):
        snd = parselmouth.Sound(str(audio_path))
        formant = snd.to_formant_burg()
        num_frames = formant.get_number_of_frames()
        times = [formant.get_time_from_frame_number(i) for i in range(1, num_frames + 1)]

        f1_values = []
        f2_values = []
        for t in times:
            f1 = formant.get_value_at_time(1, t)
            f2 = formant.get_value_at_time(2, t)
            if f1 is not None:
                f1_values.append(f1)
            if f2 is not None:
                f2_values.append(f2)

        mean_f1 = np.mean(f1_values) if f1_values else 0
        mean_f2 = np.mean(f2_values) if f2_values else 0

        return {'mean_formant1': mean_f1, 'mean_formant2': mean_f2}

