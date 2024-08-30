import numpy as np
import matplotlib.pyplot as plt
import logging
from parselmouth import Sound
from .analysis_base import AnalysisBase

class FormantsAnalysis(AnalysisBase):
    def perform_analysis(self):
        """
        Perform formant analysis on the preprocessed audio data.
        """
        self.formant_data = []

        for path, (audio, sr) in self.preprocessed_audio.items():
            try:
                sound = Sound(audio, sr)
                formant = sound.to_formant_burg()
                num_frames = formant.get_number_of_frames()
                formant_frequencies = [
                    formant.get_value_at_time(1, formant.get_time_from_frame_number(i)) 
                    for i in range(1, num_frames + 1)
                ]
                formant_frequencies = [f for f in formant_frequencies if f is not None]

                if formant_frequencies:
                    self.formant_data.extend(formant_frequencies)

            except Exception as e:
                logging.error(f"Error processing audio for path {path}: {e}")

    def create_plots(self):
        """
        Generate and save plots based on formant analysis results.
        """
        if not self.formant_data:
            logging.warning("No formant data to visualize.")
            return

        mean_formants = np.mean(self.formant_data)
        median_formants = np.median(self.formant_data)
        std_formants = np.std(self.formant_data)

        plt.figure(figsize=(10, 6))
        plt.hist(self.formant_data, bins=50, alpha=0.75, color='blue', edgecolor='black')
        plt.axvline(mean_formants, color='r', linestyle='dashed', linewidth=1, label=f'Mean: {mean_formants:.2f} Hz')
        plt.axvline(median_formants, color='g', linestyle='dashed', linewidth=1, label=f'Median: {median_formants:.2f} Hz')
        plt.title('Formant Frequencies Distribution')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Count')
        plt.legend()

        self.save_plot('formants_distribution.png', plt.gcf())

        fig, ax = plt.subplots()
        ax.bar(['Mean', 'Median'], [mean_formants, median_formants], yerr=[std_formants, std_formants], capsize=5)
        ax.set_title('Formant Statistics')
        ax.set_ylabel('Frequency (Hz)')
        self.save_plot('formants_statistics.png', fig)
