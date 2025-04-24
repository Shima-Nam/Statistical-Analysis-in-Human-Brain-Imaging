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

# Select relevant columns, excluding certain ones
df_fit = df.drop(columns=[col for col in df.columns if col.startswith("psd_values")] + ["freq_values", "Channel_number", "Session"])

# Rename columns
df_fit = df_fit.rename(columns={
    "Sub_number": "sub",
    "Channel_label": "channel",
    "Condition": "condition"
})

# Convert to long format
df_fit = df_fit.melt(id_vars=["sub", "channel", "condition"], 
                      value_vars=["delta", "theta", "alpha", "beta", "lowgamma"],
                      var_name="band", value_name="psd")

# Assign day values based on condition
day_mapping = {
    "R1": "day1", "C1": "day1", "R2": "day1", "C2": "day1", "R3": "day1",
    "R4": "day2", "M1": "day2", "R5": "day2", "M2": "day2", "R6": "day2",
    "R7": "day3"
}
df_fit["day"] = df_fit["condition"].map(day_mapping)

# Convert 'sub' to string
df_fit["sub"] = df_fit["sub"].astype(str)

# # Merge with mrs dataframe
# df_fit = df_fit.merge(mrs, on=["sub", "condition", "day"], how="left")

# Convert categorical columns
df_fit["channel"] = df_fit["channel"].astype("category")
df_fit["sub"] = df_fit["sub"].astype("category")
df_fit["condition"] = pd.Categorical(df_fit["condition"], 
                                       categories=["R1", "C1", "R2", "C2", "R3", "R4", "M1", "R5", "M2", "R6", "R7"],
                                       ordered=True)
df_fit["band"] = pd.Categorical(df_fit["band"], 
                                  categories=["delta", "theta", "alpha", "beta", "lowgamma"],
                                  ordered=True)

