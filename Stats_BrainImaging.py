#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(108)


import os
print(os.getcwd())  # Check current working directory

#read the data file containing the EEG PSD values for each electrod and condition per subject
df = pd.read_csv("...\\PSD_Values.csv") 

df.shape

# Compute frequency band means for EEG Data
bands = {
    "delta": (0.5, 4),
    "theta": (4, 8),
    "alpha": (8, 13),
    "beta": (13, 30),
    "lowgamma": (30, 55)
}

for band, (low, high) in bands.items():
    indices = df[(df['freq_values'] > low) & (df['freq_values'] <= high)].index
    column_names = [f"psd_values_{i}" for i in indices]
    df[band] = df[column_names].mean(axis=1)

#%%