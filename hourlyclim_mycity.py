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
ax2 = ax1.twinx()

for m in months:
    # --- Data Loading ---
    ds_pet = xr.open_dataset(era_path / f'pev_ags_{m}_hourlyclim.nc')['pev'].squeeze() * -1000
    ds_p   = xr.open_dataset(era_path / f'tp_ags_{m}_hourlyclim.nc')['tp'].squeeze() * 1000
    ds_e   = xr.open_dataset(era_path / f'e_ags_{m}_hourlyclim.nc')['e'].squeeze() * -1000
    ds_t   = xr.open_dataset(era_path / f't2m_ags_{m}_hourlyclim.nc')['t2m'].squeeze() - 273.15
    
    ls = styles[m]
    
    # --- Plotting ---
    ax1.plot(mth, ds_pet*24, color='k', linestyle=ls, label=f'PET ({m})', linewidth=2)
    ax1.plot(mth, ds_p*24,   color='b', linestyle=ls, label=f'P ({m})',   linewidth=2)
    ax1.plot(mth, ds_e*24,   color='r', linestyle=ls, label=f'E ({m})',   linewidth=2)
    
    ax2.plot(mth, ds_t,   color='y', linestyle=ls, label=f'Temp ({m})', linewidth=2.5)

# --- X-Axis (Every hour) ---
ax1.set_xlabel("Hour", fontsize=label_fz, fontweight='bold')
ax1.set_xticks(np.arange(1, 25, 1)) # Labels for every single hour
ax1.tick_params(axis='x', labelsize=tick_fz)

# --- Primary Y-Axis (Water Balance) ---
ax1.set_ylabel(r"mm day$^{-1}$", fontsize=label_fz, fontweight='bold')
ax1.tick_params(axis='y', labelsize=tick_fz)
#ax1.set_ylim(-0.05, 0.7)

# --- Secondary Y-Axis (Temperature) - YELLOW ---
ax2.set_ylabel('Temperature (°C)', fontsize=label_fz, fontweight='bold', color='y')
ax2.tick_params(axis='y', labelcolor='y', color='y', labelsize=tick_fz)
ax2.spines['right'].set_color('y')
ax2.set_ylim(6, 30)

# --- Combined Legend ---
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(lines1 + lines2, labels1 + labels2, 
           loc='upper left', 
           ncol=2, 
           edgecolor='white', 
           fontsize=legend_fz,
           framealpha=0.8)

plt.title('Terrestrial Water Balance (ERA5 1991-2020)\nAguascalientes, Mexico', 
          fontsize=title_fz, fontweight='bold')

plt.tight_layout()
#plt.show()
plt.savefig('hourlyclim_prec.png',dpi=300, bbox_inches='tight')

