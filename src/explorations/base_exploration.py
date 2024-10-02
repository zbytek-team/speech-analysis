import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class BaseExploration(object):        
    def initialize_data(self, data):
        """ Initialize data """
        self.data = data
  
    def describe_data(self):
        pass

    def plot_data(self):
        pass