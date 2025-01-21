# Clusterization

This folder contains a Jupyter notebook (`clusterization.ipynb`) that performs preprocessing and clusterization on CSV files containing information about different languages. The notebook includes the following steps:

## Preprocessing

1. **Select Males**: Only male speakers are selected from the dataset.
2. **Remove Teens**: Records of teens are removed from the dataset.
3. **Remove ZRC Columns**: Columns related to zero-crossing rate (ZRC) are removed because they have proven to be unimportant in other analyses.
4. **Divide List Columns**: Columns containing lists of data instead of single floats are divided using the following functions:

   ```python
   import re
   import ast
   import numpy as np
   import pandas as pd

   def fix_array_format(arr_str):
       arr_str = re.sub(r"\s+", ",", arr_str.strip())
       arr_str = arr_str.replace("[,", "[").replace(",]", "]")
       return np.array(ast.literal_eval(arr_str))

   def fix_list_values(df):
       list_columns = ['mfcc_mean', 'mfcc_var', 'spectral_contrast_mean', 'spectral_contrast_var', 'chroma_mean', 'chroma_var']
       for col in list_columns:
           features_df = df[col].apply(fix_array_format).apply(pd.Series)
           features_df.columns = [f'{col}_{i}' for i in range(features_df.shape[1])]
           df = pd.concat([df.drop(columns=[col]), features_df], axis=1)

       return df
   ```

5. **Drop Non-Numeric Columns**: The first three non-numeric columns are dropped.
6. **Scale Values**: Values are scaled using `StandardScaler` from `sklearn.preprocessing`.

## Feature Selection

The notebook defines the most differentiable features from the dataset using different methods:

1. **Recursive Feature Elimination (RFE)**
2. **Mutual Information**
3. **RandomForestClassifier**
4. **Gradient Boosting**
5. **L1 Feature Selection with LogisticRegression**
6. **Linear Discriminant Analysis (LDA)**

## Clusterization

In the end, the notebook selects the best feature from each method and tries to perform clusterization using each feature, measuring the silhouette score for 12 clusters for each feature.
