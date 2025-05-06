import pandas as pd
import pathlib


# Path to new case files
DATA_DIR = pathlib.Path("/home/nikidis/Documents/GitHub/phonons/responses_reviewers/csv")
csv_paths = sorted(DATA_DIR.glob("case_*_w_extracted.csv"))

# Compute summary for each case
summary = []
for csv_path in csv_paths:
    df = pd.read_csv(csv_path)
    df_short = df[df["time"] <= 6.0]
    summary.append({
        "Case": csv_path.stem.replace("_extracted", ""),
        "Peak Temp (K)": df_short["temp"].max(),
        "Peak v_amp (Å/ps)": df_short["v_amp"].abs().max(),
        "Min etotal": df_short["etotal"].min()
    })

# Create DataFrame and calculate averages
df_summary = pd.DataFrame(summary).set_index("Case")
avg_df = pd.DataFrame(df_summary.mean()).T
avg_df.index = ["Average"]

# Print the results
print("Summary for each case:")
print(df_summary)
print("\nAverage values:")
print(avg_df)