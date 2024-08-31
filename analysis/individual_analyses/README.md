# Individual Analyses Guide

This guide explains how to create new analysis scripts in the `individual_analyses` directory. The purpose of each script is to perform a specific analysis on preprocessed audio data and generate visualizations of the results.

## How to Create a New Analysis Script

To create a new analysis script, follow these steps:

1. **Create a New Python File**: In the `individual_analyses` directory, create a new Python file named `<your_analysis_name>_analysis.py`. For example, if you are creating a pitch analysis, you could name the file `pitch_analysis.py`.

2. **Import the Base Class**: At the top of your new file, import the `AnalysisBase` class from `analysis_base.py`.

   ```python
   from .analysis_base import AnalysisBase
   ```

3. **Create a New Class**: Define a new class in your file that inherits from `AnalysisBase`. This class should implement the `perform_analysis` and `create_plots` methods.

   ```python
   class PitchAnalysis(AnalysisBase):
       def perform_analysis(self):
           # Your code for analyzing pitch goes here

       def create_plots(self):
           # Your code for creating plots goes here
   ```

4. **Implement `perform_analysis` Method**: This method should contain the logic for your analysis. It will have access to `self.preprocessed_audio`, a dictionary of preprocessed audio data, and should store the results of the analysis in an instance variable.

5. **Implement `create_plots` Method**: This method should generate and save plots based on the analysis results. Use the `save_plot` method provided by `AnalysisBase` to save your plots.

6. **Save Your File**: Once your analysis class is complete, save your file in the `analyses` directory.

## Example: Formants Analysis

Here is an example of a simple formant analysis implementation:

```python
from .analysis_base import AnalysisBase
import matplotlib.pyplot as plt

class ExampleAnalysis(AnalysisBase):
    def perform_analysis(self):
        # Initialize an empty list to store analysis results
        self.data = []

        for path, (audio, sr) in self.preprocessed_audio.items():
            # Perform analysis on the audio data
            # Example: Replace this with your actual analysis logic
            result = some_analysis_function(audio)
            self.data.append(result)

    def create_plots(self):
        # Example plot: replace with your actual plotting logic
        plt.figure()
        plt.plot(self.data)  # Replace this with your data and plotting code
        plt.title('Example Plot')
        plt.xlabel('X-axis label')
        plt.ylabel('Y-axis label')
        self.save_plot('example_plot.png', plt.gcf())
```
