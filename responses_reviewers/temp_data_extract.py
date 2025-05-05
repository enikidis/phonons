import pandas as pd
import pathlib
import re

log_dir = pathlib.Path("/Users/nikidis/Documents/GitHub/phonons/responses_reviewers/lamps_logs")

summary_records = []

def parse_lammps_log(log_path: pathlib.Path) -> pd.DataFrame:
    header_found = False
    cols = []
    rows = []
    with log_path.open() as f:
        for line in f:
            if not header_found:
                if line.startswith("Step") and " Temp " in line:
                    cols = re.split(r"\s+", line.strip())
                    header_found = True
                continue
            if not line.strip() or not line[0].isdigit():
                break
            parts = re.split(r"\s+", line.strip())
            if len(parts) == len(cols):
                rows.append(parts)
    df = pd.DataFrame(rows, columns=cols).astype(float)
    df.columns = [c.lower() for c in df.columns]
    if "toteng" in df.columns:
        df.rename(columns={"toteng": "etotal"}, inplace=True)
    return df

for log_path in sorted(log_dir.glob("WP*.log")):
    df = parse_lammps_log(log_path)
    df_subset = df[["time", "temp", "etotal", "v_amp"]]
    out_csv = log_path.parent / f"{log_path.stem}_extracted.csv"
    df_subset.to_csv(out_csv, index=False)

    summary_records.append(
        {
            "case": log_path.stem,
            "T_max (K)": df_subset["temp"].max(),
            "T_final (K)": df_subset["temp"].iloc[-1],
            "Energy drift (%)": 100
            * (df_subset["etotal"].iloc[-1] - df_subset["etotal"].iloc[0])
            / df_subset["etotal"].iloc[0],
        }
    )

summary_df = pd.DataFrame(summary_records)
summary_csv = log_dir / "summary_cases.csv"
summary_df.to_csv(summary_csv, index=False)

print(f"Summary saved to {summary_csv}")
