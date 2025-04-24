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

#%%%

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Prepare data for model
# Day 1: C vs R
df_fit1 = df_fit[df_fit["day"] == "day1"].drop(columns=["day"]).copy()
df_fit1["condition"] = df_fit1["condition"].str[0]
df_fit1["condition"] = pd.Categorical(df_fit1["condition"], categories=["C", "R"], ordered=True)

# Day 2: M vs R
df_fit2 = df_fit[df_fit["day"] == "day2"].drop(columns=["day"]).copy()
df_fit2["condition"] = df_fit2["condition"].str[0]
df_fit2["condition"] = pd.Categorical(df_fit2["condition"], categories=["M", "R"], ordered=True)

# All: M vs C vs R
df_fit3 = df_fit.copy()
df_fit3["condition"] = df_fit3["condition"].str[0]
df_fit3["condition"] = pd.Categorical(df_fit3["condition"], categories=["M", "C", "R"], ordered=True)

# Initialize results dataframe
results = pd.DataFrame(columns=["channel", "band", "MvsC_diff", "MvsC_se", "MvsC_p", "MvsR_diff", "MvsR_se", "MvsR_p", "CvsR_diff", "CvsR_se", "CvsR_p"])

for iband in df_fit["band"].unique():
    print(f"Computing for band: {iband}")

    for ichannel in df_fit["channel"].unique():
        print(f"Channel: {ichannel}")

        # Day 1: C vs R
        filtered_data1 = df_fit1[(df_fit1["band"] == iband) & (df_fit1["channel"] == ichannel)]
        # Check if filtered data has enough observations
        if filtered_data1.shape[0] > 0:  # Check if the DataFrame is not empty
            model1 = smf.mixedlm("psd ~ condition", filtered_data1, groups=filtered_data1["sub"]).fit()
            CvsR_diff, CvsR_se, CvsR_p = model1.params["condition[T.R]"], model1.bse["condition[T.R]"], model1.pvalues["condition[T.R]"]
        else:
            print(f"Skipping band: {iband}, channel: {ichannel} for Day 1 due to insufficient data.")
            CvsR_diff, CvsR_se, CvsR_p = np.nan, np.nan, np.nan  # Assign NaN values for empty dataframes

        # Day 2: M vs R
        filtered_data2 = df_fit2[(df_fit2["band"] == iband) & (df_fit2["channel"] == ichannel)]
        # Check if filtered data has enough observations
        if filtered_data2.shape[0] > 0:  # Check if the DataFrame is not empty
            model2 = smf.mixedlm("psd ~ condition", filtered_data2, groups=filtered_data2["sub"]).fit()
            MvsR_diff, MvsR_se, MvsR_p = model2.params["condition[T.R]"], model2.bse["condition[T.R]"], model2.pvalues["condition[T.R]"]
        else:
            print(f"Skipping band: {iband}, channel: {ichannel} for Day 2 due to insufficient data.")
            MvsR_diff, MvsR_se, MvsR_p = np.nan, np.nan, np.nan # Assign NaN values for empty dataframes

        # All: M vs C
        filtered_data3 = df_fit3[(df_fit3["band"] == iband) & (df_fit3["channel"] == ichannel)]
        # Check if filtered data has enough observations
        if filtered_data3.shape[0] > 0:  # Check if the DataFrame is not empty
            model3 = smf.mixedlm("psd ~ condition", filtered_data3, groups=filtered_data3["sub"]).fit()
            MvsC_diff, MvsC_se, MvsC_p = model3.params["condition[T.C]"], model3.bse["condition[T.C]"], model3.pvalues["condition[T.C]"]
        else:
            print(f"Skipping band: {iband}, channel: {ichannel} for All Days due to insufficient data.")
            MvsC_diff, MvsC_se, MvsC_p = np.nan, np.nan, np.nan # Assign NaN values for empty dataframes

        # Append to results using concat
        results = pd.concat([results, pd.DataFrame([{
            "channel": ichannel,
            "band": iband,
            "MvsC_diff": MvsC_diff,
            "MvsC_se": MvsC_se,
            "MvsC_p": MvsC_p,
            "MvsR_diff": MvsR_diff,
            "MvsR_se": MvsR_se,
            "MvsR_p": MvsR_p,
            "CvsR_diff": CvsR_diff,
            "CvsR_se": CvsR_se,
            "CvsR_p": CvsR_p
        }])], ignore_index=True)

#%%
#Printing the results of statistical analysis p-value < 0.01
from tabulate import tabulate

def print_contrast_table(results, contrast_name, alpha=0.01):
    """
    Print a formatted table for a given contrast from the results DataFrame

    Parameters:
    - results: DataFrame with contrast results
    - contrast_name: 'MvsC', 'MvsR', or 'CvsR'
    - alpha: significance threshold for p-values
    """
    diff_col = f"{contrast_name}_diff"
    se_col = f"{contrast_name}_se"
    p_col = f"{contrast_name}_p"

    filtered_results = results[results[p_col] < alpha].round(4)

    contrast_labels = {
        "MvsC": "M - C",
        "MvsR": "M - R",
        "CvsR": "C - R"
    }

    print(f"\nContrast: {contrast_labels.get(contrast_name, contrast_name)}\n")

    if filtered_results.empty:
        print(f"No results with p-values below {alpha}")
    else:
        table_data = filtered_results.reset_index(drop=True)
        table_data.insert(0, "#", range(1, len(table_data) + 1))

        # Convert to list of rows to avoid showing index
        print(tabulate(
            table_data[["#", "channel", "band", diff_col, se_col, p_col]].values.tolist(),
            headers=["#", "Channel", "Band", "Diff", "SE", "p-value"],
            tablefmt="pretty"
        ))

print_contrast_table(results, "MvsC")
print_contrast_table(results, "MvsR")
print_contrast_table(results, "CvsR")