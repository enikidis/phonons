import pandas as pd
import numpy as np


# Given summary data
summary = pd.DataFrame({
    "Case": ["case_1_w", "case_2_w", "case_3_w", "case_4_w", "case_5_w", "case_6_w", "case_7_w"],
    "Peak v_amp (Å/ps)": [0.000351]*7
})

# Physical constants
amu_to_kg = 1.6605e-27
m_Si = 28 * amu_to_kg  # mass of Si atom in kg
angstrom_per_ps_to_m_per_s = 1e-10 / 1e-12  # 1 Å/ps = 100 m/s
k_B = 1.380649e-23  # Boltzmann constant J/K

# Compute energy injection per case
N_src = 64
N_tot = 4096  # total atoms in cell for temperature distribution
energies = []
delta_Ts = []
for v_amp in summary["Peak v_amp (Å/ps)"]:
    v_si = v_amp * angstrom_per_ps_to_m_per_s
    E1 = 0.5 * m_Si * v_si**2     # J per atom
    E_injected = N_src * E1       # J total
    E_eV = E_injected / 1.602e-19 # convert to eV
    delta_T = 2 * E_injected / (3 * N_tot * k_B)
    energies.append(E_eV)
    delta_Ts.append(delta_T)

summary["Injected Energy (eV)"] = energies
summary["ΔT (K)"] = delta_Ts

# Compute averages
avg_row = pd.DataFrame({
    "Case": ["Average"],
    "Peak v_amp (Å/ps)": [summary["Peak v_amp (Å/ps)"].mean()],
    "Injected Energy (eV)": [summary["Injected Energy (eV)"].mean()],
    "ΔT (K)": [summary["ΔT (K)"].mean()]
})

result = pd.concat([summary, avg_row], ignore_index=True)

# Print the results
print(result)