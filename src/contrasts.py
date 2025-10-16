import pandas as pd

# Prepare contrast datasets for different days and conditions
#
# Args:
#   df_fit (pd.DataFrame): Preprocessed EEG DataFrame
#
# Returns:
#   Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Day1 (C vs R), Day2 (M vs R), All (M vs C vs R)
def prepare_contrasts(df_fit):
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

    return df_fit1, df_fit2, df_fit3
