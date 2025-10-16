from tabulate import tabulate
import pandas as pd

# Print formatted contrast table with significant p-values
#
# Args:
#   results (pd.DataFrame): Results from mixedlm_analysis
#   contrast_name (str): "MvsC", "MvsR", or "CvsR"
#   alpha (float): significance threshold
def print_contrast_table(results, contrast_name, alpha=0.01):
    diff_col = f"{contrast_name}_diff"
    se_col = f"{contrast_name}_se"
    p_col = f"{contrast_name}_p"

    filtered_results = results[results[p_col] < alpha].round(4)

    contrast_labels = {"MvsC": "M - C", "MvsR": "M - R", "CvsR": "C - R"}

    print(f"\nContrast: {contrast_labels.get(contrast_name, contrast_name)}\n")

    if filtered_results.empty:
        print(f"No results with p-values below {alpha}")
    else:
        table_data = filtered_results.reset_index(drop=True)
        table_data.insert(0, "#", range(1, len(table_data) + 1))
        print(tabulate(
            table_data[["#", "channel", "band", diff_col, se_col, p_col]].values.tolist(),
            headers=["#", "Channel", "Band", "Diff", "SE", "p-value"],
            tablefmt="pretty"
        ))
