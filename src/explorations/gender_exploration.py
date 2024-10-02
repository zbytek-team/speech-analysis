from .base_exploration import BaseExploration

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class GenderExploration(BaseExploration):
    def prepare_data(self):
        # connect all data frames into one by columns 'language' and 'gender'
        self.concatenated_data = pd.concat(self.data, ignore_index=True)

    def plot_data(self):
        plt.figure(figsize=(10, 6))

        # Plot the gender distribution
        sns.countplot(x='language', hue='gender', data=self.concatenated_data)

        plt.title("Gender distribution by language", fontsize=16)
        plt.xlabel("Language", fontsize=14)
        plt.ylabel("Count", fontsize=14)

        plt.show()