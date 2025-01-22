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

## Clustering Evaluation

To ensure the selected features are indeed the best, a clustering check was performed on every feature. The clustering results were evaluated using two metrics: Adjusted Rand Index (ARI) and Normalized Mutual Information (NMI).

### Clustering Process

1. **KMeans Clustering**: The KMeans algorithm was used to divide the data into clusters. Each feature was used individually to perform clustering.
2. **Label Mapping**: After clustering, the cluster labels were mapped to the most common true label in each cluster. This mapping helps in comparing the clustering results with the actual labels.
3. **Evaluation Metrics**:
   - **Adjusted Rand Index (ARI)**: Measures the similarity between the clustering labels and the true labels, adjusted for chance.
   - **Normalized Mutual Information (NMI)**: Measures the mutual information between the clustering labels and the true labels, normalized to account for the size of the clusters.

### Results

The best features were selected based on their combined scores of ARI and NMI. The top three pairs of features were then used to perform clustering on the dataset, and the results were visualized on 2D graphs.

### Visualization

The clustering results for the top three pairs of features were visualized on 2D graphs. Each graph shows the clusters formed by the KMeans algorithm, with colors representing different clusters. The graphs help in understanding the effectiveness of the selected features in distinguishing between different classes.

## Conclusion

The combined scores of ARI and NMI were used to identify the top features, and the visualizations provided a clear understanding of the clustering results. Interestingly, the clustering analysis revealed that the features identified as the best by the feature selection algorithms did not necessarily yield the best clustering results, suggesting that different features may be more effective for clustering purposes.
