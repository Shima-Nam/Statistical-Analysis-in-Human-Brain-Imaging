import matplotlib.pyplot as plt
import pandas as pd

# Example: plot PSD differences by band
#
# Args:
#   results (pd.DataFrame)
#   contrast_name (str)
def plot_psd_diff(results, contrast_name):
    diff_col = f"{contrast_name}_diff"
    results_grouped = results.groupby("band")[diff_col].mean()
    results_grouped.plot(kind="bar", title=f"{contrast_name} mean PSD differences")
    plt.ylabel("PSD Difference")
    plt.show()
