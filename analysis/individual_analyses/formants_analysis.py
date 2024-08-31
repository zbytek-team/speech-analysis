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
        self.formant_data = {'F1': [], 'F2': [], 'F3': []}

        for path, (audio, sr) in self.preprocessed_audio.items():
            try:
                # Convert the audio to a Parselmouth Sound object
                sound = Sound(audio, sr)
                
                # Extract formants using the Burg method
                formant = sound.to_formant_burg()
                
                # Iterate through each frame to extract formant frequencies
                for i in range(1, formant.get_number_of_frames() + 1):
                    time = formant.get_time_from_frame_number(i)
                    
                    # Extract F1, F2, F3 formant frequencies
                    f1 = formant.get_value_at_time(1, time)
                    f2 = formant.get_value_at_time(2, time)
                    f3 = formant.get_value_at_time(3, time)
                    
                    # Append the formant frequencies to the respective lists if they are not None
                    if f1 is not None:
                        self.formant_data['F1'].append(f1)
                    if f2 is not None:
                        self.formant_data['F2'].append(f2)
                    if f3 is not None:
                        self.formant_data['F3'].append(f3)

            except Exception as e:
                logging.error(f"Error processing audio for path {path}: {e}")

    def create_plots(self):
        """
        Generate and save plots based on formant analysis results.
        """
        # Check if there is data to visualize
        if not self.formant_data['F1'] or not self.formant_data['F2']:
            logging.warning("Not enough formant data to visualize.")
            return

        # Plot 2D vowel space (F1 vs. F2)
        plt.figure(figsize=(10, 6))
        plt.scatter(self.formant_data['F1'], self.formant_data['F2'], alpha=0.5)
        plt.title('Vowel Space (F1 vs. F2)')
        plt.xlabel('F1 Frequency (Hz)')
        plt.ylabel('F2 Frequency (Hz)')
        plt.grid(True)
        self.save_plot('vowel_space.png', plt.gcf())

        # Formant frequency distribution histograms
        plt.figure(figsize=(10, 6))
        plt.hist(self.formant_data['F1'], bins=50, alpha=0.75, label='F1', color='blue', edgecolor='black')
        plt.hist(self.formant_data['F2'], bins=50, alpha=0.75, label='F2', color='green', edgecolor='black')
        plt.hist(self.formant_data['F3'], bins=50, alpha=0.75, label='F3', color='red', edgecolor='black')
        plt.title('Formant Frequencies Distribution')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Count')
        plt.legend()
        self.save_plot('formants_distribution.png', plt.gcf())

        # Formant statistics bar plot
        f1_mean = np.mean(self.formant_data['F1'])
        f2_mean = np.mean(self.formant_data['F2'])
        f3_mean = np.mean(self.formant_data['F3'])
        f1_std = np.std(self.formant_data['F1'])
        f2_std = np.std(self.formant_data['F2'])
        f3_std = np.std(self.formant_data['F3'])

        fig, ax = plt.subplots()
        ax.bar(['F1', 'F2', 'F3'], [f1_mean, f2_mean, f3_mean], yerr=[f1_std, f2_std, f3_std], capsize=5)
        ax.set_title('Formant Statistics')
        ax.set_ylabel('Frequency (Hz)')
        self.save_plot('formants_statistics.png', fig)
