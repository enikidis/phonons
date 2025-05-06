import os
import pandas as pd
import matplotlib.pyplot as plt

# === Define input ===
# Propagation distances (nm) for each slice
x_positions = [12.27, 14.27, 16.27, 18.27, 20.27, 22.27, 25.27]  # 24.27 omitted

# Base directories
case1_dir = r"/home/nikidis/Documents/GitHub/phonons/lammps_output/slices/8_slices"
case4_dir = r"/home/nikidis/Documents/GitHub/phonons/lammps_output/slices/11_slices"

# Corresponding filenames for each case
case1_files = [
    os.path.join(case1_dir, fname) for fname in [
        "8_370.csv", "8_390.csv", "8_410.csv", "8_430.csv",
        "8_450.csv", "8_470.csv", "8_500.csv"
    ]
]

case4_files = [
    os.path.join(case4_dir, fname) for fname in [
        "11_370.csv", "11_390.csv", "11_410.csv", "11_430.csv",
        "11_450.csv", "11_470.csv", "11_500.csv"
    ]
]

# === Read and sum KE per slice ===
def load_total_ke(filenames):
    total_ke = []
    for fname in filenames:
        df = pd.read_csv(fname, header=None)
        ke_sum = df.iloc[:, 1].sum()
        total_ke.append(ke_sum)
    return total_ke

case1_ke = load_total_ke(case1_files)
case4_ke = load_total_ke(case4_files)

# === Calculate percentage difference ===
percent_diff = [
    100 * (c4 - c1) / c4 if c4 != 0 else 0
    for c1, c4 in zip(case1_ke, case4_ke)
]

# === Plotting ===
plt.figure(figsize=(10, 6))
plt.plot(x_positions, case1_ke, 'o-', label='Case 1 (d = 8.6 nm)', color='blue')
plt.plot(x_positions, case4_ke, 's-', label='Case 4 (d = 4.0 nm)', color='orange')
plt.xlabel('Propagation Distance (nm)')
plt.ylabel('Total Kinetic Energy (eV)')
plt.title('Kinetic Energy Transmission: Case 1 vs Case 4')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save the plot as a PNG file
output_path = os.path.join(os.getcwd(), "kinetic_energy_comparison.png")
plt.savefig(output_path, dpi=300)  # Save with high resolution
plt.show()

print(f"Plot saved as: {output_path}")
# === Optional: Print table for report ===
print("Distance (nm) | Case 1 KE | Case 4 KE | % Diff")
for x, c1, c4, d in zip(x_positions, case1_ke, case4_ke, percent_diff):
    print(f"{x:>12} | {c1:.3e} | {c4:.3e} | {d:+.2f}%")