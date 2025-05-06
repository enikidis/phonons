# ---------------------------  plot_temp_traces.py  ---------------------------
import pathlib
import pandas as pd
import matplotlib.pyplot as plt

# 1) Point this to the directory that contains your WP1_extracted.csv … WP7_extracted.csv
DATA_DIR = pathlib.Path("/home/nikidis/Documents/GitHub/phonons/responses_reviewers/csv")      # <— change this if the CSVs sit elsewhere

# 2) Load every file that matches case_*_w_extracted.csv
csv_paths = sorted(DATA_DIR.glob("case_*_w_extracted.csv"))

if not csv_paths:
    raise FileNotFoundError("No WP*_extracted.csv files found in {}".format(DATA_DIR.resolve()))

plt.figure(figsize=(6, 4))

for csv_path in csv_paths:
    df = pd.read_csv(csv_path)

    # keep only the first 6 ps (adjust if you want a longer window)
    df_short = df[df["time"] <= 6.0]

    label = csv_path.stem.replace("_extracted", "")  # e.g. "WP1"
    plt.plot(df_short["time"], df_short["temp"], label=label)

# 3) Basic axis labels and legend
plt.xlabel("Time (ps)")
plt.ylabel("Kinetic temperature, T (K)")
plt.title("Transient temperature during phonon excitation – all cases")
plt.legend(fontsize=8, loc="upper left")

# 4) Save figure (and also show it on screen)
plt.tight_layout()
plt.savefig("FigS1_temp_curves.png", dpi=300)
plt.show()
# ---------------------------------------------------------------------------
