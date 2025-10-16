import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

# Run mixed linear models for each band and channel
#
# Args:
#   df_fit1, df_fit2, df_fit3 (pd.DataFrame): DataFrames prepared for contrasts
#
# Returns:
#   pd.DataFrame: Results table with diffs, SEs, and p-values for each contrast
def run_mixedlm_analysis(df_fit1, df_fit2, df_fit3):
    results = pd.DataFrame(columns=["channel", "band", 
                                    "MvsC_diff", "MvsC_se", "MvsC_p", 
                                    "MvsR_diff", "MvsR_se", "MvsR_p", 
                                    "CvsR_diff", "CvsR_se", "CvsR_p"])
    
    for iband in df_fit1["band"].cat.categories:
        for ichannel in df_fit1["channel"].cat.categories:
            # Day 1: C vs R
            filtered_data1 = df_fit1[(df_fit1["band"] == iband) & (df_fit1["channel"] == ichannel)]
            if filtered_data1.shape[0] > 0:
                model1 = smf.mixedlm("psd ~ condition", filtered_data1, groups=filtered_data1["sub"]).fit()
                CvsR_diff, CvsR_se, CvsR_p = model1.params["condition[T.R]"], model1.bse["condition[T.R]"], model1.pvalues["condition[T.R]"]
            else:
                CvsR_diff, CvsR_se, CvsR_p = np.nan, np.nan, np.nan

            # Day 2: M vs R
            filtered_data2 = df_fit2[(df_fit2["band"] == iband) & (df_fit2["channel"] == ichannel)]
            if filtered_data2.shape[0] > 0:
                model2 = smf.mixedlm("psd ~ condition", filtered_data2, groups=filtered_data2["sub"]).fit()
                MvsR_diff, MvsR_se, MvsR_p = model2.params["condition[T.R]"], model2.bse["condition[T.R]"], model2.pvalues["condition[T.R]"]
            else:
                MvsR_diff, MvsR_se, MvsR_p = np.nan, np.nan, np.nan

            # All: M vs C
            filtered_data3 = df_fit3[(df_fit3["band"] == iband) & (df_fit3["channel"] == ichannel)]
            if filtered_data3.shape[0] > 0:
                model3 = smf.mixedlm("psd ~ condition", filtered_data3, groups=filtered_data3["sub"]).fit()
                MvsC_diff, MvsC_se, MvsC_p = model3.params["condition[T.C]"], model3.bse["condition[T.C]"], model3.pvalues["condition[T.C]"]
            else:
                MvsC_diff, MvsC_se, MvsC_p = np.nan, np.nan, np.nan

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
    
    return results
