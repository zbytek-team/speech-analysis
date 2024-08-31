import os
import matplotlib.pyplot as plt
import logging
from abc import ABC, abstractmethod

class AnalysisBase(ABC):
    def __init__(self, preprocessed_audio, output_dir: str):
        """
        Base class for specific audio analyses.

        :param preprocessed_audio: Dictionary of preprocessed audio data and sample rates.
        :param output_dir: Directory to save analysis results.
        """
        self.preprocessed_audio = preprocessed_audio
        self.output_dir = output_dir

    def run(self):
        """
        Execute the analysis and create plots.
        """
        self.perform_analysis()
        self.create_plots()

    @abstractmethod
    def perform_analysis(self):
        """
        Perform the specific analysis on the audio data.
        This method must be overridden in each subclass.
        """
        pass

    @abstractmethod
    def create_plots(self):
        """
        Generate and save plots of the analysis results.
        This method must be overridden in each subclass.
        """
        pass

    def save_plot(self, plot_name: str, fig: plt.Figure):
        """
        Save a plot to the output directory.

        :param plot_name: Name of the plot file.
        :param fig: Matplotlib figure object.
        """
        plot_path = os.path.join(self.output_dir, plot_name)
        fig.savefig(plot_path)
        plt.close(fig)
        logging.info(f"Plot saved: {plot_path}")
