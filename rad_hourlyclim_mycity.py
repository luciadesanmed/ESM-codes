import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

# Data path
era_path = Path("/home/desan/ESM-data/")
months = ('jul', 'dec')
styles = {'jul': '-', 'dec': '--'}

# Increased Font Sizes
label_fz = 16    # Axis titles
tick_fz = 14     # Axis numbers
legend_fz = 12   # Legend text
title_fz = 18    # Main title

mth = np.arange(1, 25, 1)

fig, ax1 = plt.subplots(figsize=(12, 7)) # Slightly larger figure for larger fonts

for m in months:
    # --- Data Loading ---
    ds_heat = xr.open_dataset(era_path / f'heatstor_ags_{m}.nc')['ssr'].squeeze()
    ds_sh   = xr.open_dataset(era_path / f'sshf_ags_{m}_hourlyclim.nc')['sshf'].squeeze() * -1
    ds_lh   = xr.open_dataset(era_path / f'slhf_ags_{m}_hourlyclim.nc')['slhf'].squeeze() * -1
    ds_rad  = xr.open_dataset(era_path / f'ssr_ags_{m}_hourlyclim.nc')['ssr'].squeeze()
    
    ls = styles[m]
    
    # --- Plotting ---
    ax1.plot(mth, ds_rad, color='k', linestyle=ls, label=f'Rn ({m})')
    ax1.plot(mth, ds_lh,   color='b', linestyle=ls, label=f'LE ({m})',   linewidth=2)
    ax1.plot(mth, ds_sh,   color='r', linestyle=ls, label=f'SH ({m})',   linewidth=2)
    ax1.plot(mth, ds_heat, color='y', linestyle=ls, label=f'G ({m})', linewidth=2)
# --- X-Axis (Every hour) ---
ax1.set_xlabel("Hour", fontsize=label_fz, fontweight='bold')
ax1.set_xticks(np.arange(1, 25, 1)) # Labels for every single hour
ax1.tick_params(axis='x', labelsize=tick_fz)

# --- Primary Y-Axis (Water Balance) ---
ax1.set_ylabel(r"W/m$^{2}$", fontsize=label_fz, fontweight='bold')
ax1.tick_params(axis='y', labelsize=tick_fz)
#ax1.set_ylim(-0.1, 16.5)

# --- Combined Legend ---
lines1, labels1 = ax1.get_legend_handles_labels()
#lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(lines1, labels1, 
           loc='upper left', 
           ncol=2, 
           edgecolor='white', 
           fontsize=legend_fz,
           framealpha=0.8)

ax1.grid(True, linestyle='--', alpha=0.5)
# Add a black horizontal line at y=0
plt.axhline(0, color='gray', linestyle=':', linewidth=1.2)

plt.title('Heat budget (ERA5 1991-2020)\nAguascalientes, Mexico', 
          fontsize=title_fz, fontweight='bold')

plt.tight_layout()
#plt.show()
plt.savefig('hourlyclim_rad.png',dpi=300, bbox_inches='tight')

