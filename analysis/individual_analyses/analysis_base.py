import os
import matplotlib.pyplot as plt
import logging
from abc import ABC, abstractmethod

class AnalysisBase(ABC):
    def __init__(self, preprocessed_audio, output_dir: str):
        self.preprocessed_audio = preprocessed_audio
        self.output_dir = output_dir

    def run(self):
        self.perform_analysis()
        self.create_plots()

    @abstractmethod
    def perform_analysis(self):
        pass

    @abstractmethod
    def create_plots(self):
        pass

    def save_plot(self, plot_name: str, fig: plt.Figure):
        plot_path = os.path.join(self.output_dir, plot_name)
        fig.savefig(plot_path)
        plt.close(fig)
        logging.info(f"Plot saved: {plot_path}")
