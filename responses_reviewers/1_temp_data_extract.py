import pandas as pd
import pathlib
import re

log_dir = pathlib.Path("/home/nikidis/Documents/GitHub/phonons/responses_reviewers/lammps_logs")
summary_records = []

def extract_last_data_block_with_v_amp(log_path: pathlib.Path) -> pd.DataFrame:
    with log_path.open() as f:
        lines = f.readlines()

    blocks = []
    current_block = []
    headers = []

    for line in lines:
        line = line.strip()

        if line.startswith("Step") and "v_amp" in line:
            if current_block:
                blocks.append((headers, current_block))
                current_block = []
            headers = re.split(r"\s+", line)
            continue

        if headers and line and line[0].isdigit():
            values = re.split(r"\s+", line)
            if len(values) == len(headers):
                current_block.append(values)
            else:
                if current_block:
                    blocks.append((headers, current_block))
                headers = []
                current_block = []

    if headers and current_block:
        blocks.append((headers, current_block))

    for headers, rows in reversed(blocks):
        cols = [h.lower() for h in headers]
        if all(c in cols for c in ("time", "temp", "toteng", "v_amp")):
            df = pd.DataFrame(rows, columns=cols).astype(float)
            df.rename(columns={"toteng": "etotal"}, inplace=True)
            return df[["time", "temp", "etotal", "v_amp"]]

    raise ValueError(f"No valid data block with required columns found in {log_path.name}")

# Process all files and extract summary
for log_path in sorted(log_dir.glob("case_*.out")):
    try:
        df = extract_last_data_block_with_v_amp(log_path)
        out_csv = log_path.with_name(f"{log_path.stem}_extracted.csv")
        df.to_csv(out_csv, index=False)
        print(f"[OK] Extracted: {out_csv.name}")

        # Add to summary
        T_max = df["temp"].max()
        T_final = df["temp"].iloc[-1]
        etot_start = df["etotal"].iloc[0]
        etot_end = df["etotal"].iloc[-1]
        drift = 100 * (etot_end - etot_start) / etot_start if etot_start != 0 else float('nan')

        summary_records.append({
            "case": log_path.stem,
            "T_max (K)": T_max,
            "T_final (K)": T_final,
            "Energy drift (%)": drift
        })

    except Exception as e:
        print(f"[ERROR] {log_path.name}: {e}")

# Write summary
summary_df = pd.DataFrame(summary_records)
summary_csv = log_dir / "summary_cases.csv"
summary_df.to_csv(summary_csv, index=False)
print(f"\n✅ Summary saved to: {summary_csv}")
