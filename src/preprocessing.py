import pandas as pd
import numpy as np

# Load CSV data and compute frequency band means for EEG PSD values
#
# Args:
#   file_path (str): Path to CSV file.
#   bands (dict): Frequency bands, e.g., {"delta": (0.5, 4), ...}
#
# Returns:
#   pd.DataFrame: Preprocessed long-format DataFrame ready for analysis
def load_and_preprocess(file_path, bands):
    df = pd.read_csv(file_path)
    
    # Compute band means
    for band, (low, high) in bands.items():
        indices = df[(df['freq_values'] > low) & (df['freq_values'] <= high)].index
        column_names = [f"psd_values_{i}" for i in indices]
        df[band] = df[column_names].mean(axis=1)
    
    # Drop unnecessary columns
    drop_cols = [col for col in df.columns if col.startswith("psd_values")] + ["freq_values", "Channel_number", "Session"]
    df_fit = df.drop(columns=drop_cols)
    
    # Rename columns
    df_fit = df_fit.rename(columns={"Sub_number": "sub", "Channel_label": "channel", "Condition": "condition"})
    
    # Convert to long format
    df_fit = df_fit.melt(id_vars=["sub", "channel", "condition"],
                         value_vars=list(bands.keys()),
                         var_name="band", value_name="psd")
    
    # Map days
    day_mapping = {
        "R1": "day1", "C1": "day1", "R2": "day1", "C2": "day1", "R3": "day1",
        "R4": "day2", "M1": "day2", "R5": "day2", "M2": "day2", "R6": "day2",
        "R7": "day3"
    }
    df_fit["day"] = df_fit["condition"].map(day_mapping)
    df_fit["sub"] = df_fit["sub"].astype(str)
    
    # Convert categorical columns
    df_fit["channel"] = df_fit["channel"].astype("category")
    df_fit["sub"] = df_fit["sub"].astype("category")
    df_fit["condition"] = pd.Categorical(df_fit["condition"],
                                         categories=["R1","C1","R2","C2","R3","R4","M1","R5","M2","R6","R7"],
                                         ordered=True)
    df_fit["band"] = pd.Categorical(df_fit["band"], categories=list(bands.keys()), ordered=True)
    
    return df_fit
