from src.preprocessing import load_and_preprocess
from src.contrasts import prepare_contrasts
from src.mixedlm_analysis import run_mixedlm_analysis
from src.results_utils import print_contrast_table

# Define EEG frequency bands
bands = {
    "delta": (0.5, 4),
    "theta": (4, 8),
    "alpha": (8, 13),
    "beta": (13, 30),
    "lowgamma": (30, 55)
}

# Load and preprocess data
df_fit = load_and_preprocess("data/PSD_Values.csv", bands)

# Prepare contrast datasets
df_fit1, df_fit2, df_fit3 = prepare_contrasts(df_fit)

# Run mixed linear model analysis
results = run_mixedlm_analysis(df_fit1, df_fit2, df_fit3)

# Print results
print_contrast_table(results, "MvsC")
print_contrast_table(results, "MvsR")
print_contrast_table(results, "CvsR")
