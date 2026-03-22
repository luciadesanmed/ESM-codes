import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

# Data path
dat_path = Path("/home/desan/ESM-data/")

# Configuration
variab = ('pr', 'tas', 'hurs') 
variab_era5_map = {'pr': 'tp', 'tas': 't2m', 'hurs': 'rh'}
units = ('mm/day', '°C', '%')
exps = ('EC-Earth3', 'EC-Earth3-AerChem', 'EC-Earth3-Veg-LR', 'ERA5')
texts = ('Precipitation', 'Temperature', 'Relative Humidity')
colors = ['#1f77b4', '#d62728', '#2ca02c', '#000000'] 

# Time configuration (365-day year)
month_bounds = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
month_mid = [15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]
month_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']

for idx, v_name in enumerate(variab):
    plt.figure(figsize=(14, 7))
    fz = 18
    plt.rcParams.update({'font.size': fz})
    ax = plt.axes()
    
    for j, exp_name in enumerate(exps):
        current_v = variab_era5_map[v_name] if exp_name == 'ERA5' else v_name
        file_name = f"{current_v}_dailyclim_{exp_name}.nc" 
        
        # Open dataset
        ds = xr.open_dataset(dat_path / file_name)
        data_arr = ds[current_v].where(ds[current_v] > -1000).squeeze()

        # Check for correct dimension name ('time' vs 'valid_time')
        time_dim = 'time' if 'time' in data_arr.dims else 'valid_time'

        # --- Unit Conversions ---
        if v_name == 'tas':
            data_arr = data_arr - 273.15
        elif v_name == 'pr':
            if exp_name == 'ERA5':
                data_arr = data_arr * 1000 
            else:
                data_arr = data_arr * 86400

        # --- Plotting Logic ---
        if exp_name == 'ERA5':
            # Reference ERA5 Monthly
            ax.plot(month_mid, data_arr.values, 
                    color=colors[j], 
                    label=f"{exp_name} (Reference)", 
                    linewidth=4, 
                    marker='o', 
                    markersize=10, 
                    zorder=10)
        else:
            # 1. Plot Daily Model Data (Less transparent, more width)
            days = np.arange(1, len(data_arr) + 1)
            ax.plot(days, data_arr.values, 
                    color=colors[j], 
                    label=f"{exp_name} (daily)", 
                    linewidth=1.2, # Increased width
                    alpha=0.45,    # Less transparent
                    zorder=2)

            # 2. Calculate and Plot Monthly Mean for Model
            model_monthly = []
            for m in range(12):
                m_avg = data_arr.isel({time_dim: slice(month_bounds[m], month_bounds[m+1])}).mean()
                model_monthly.append(float(m_avg))
            
            # Plot thicker monthly line
            ax.plot(month_mid, model_monthly, 
                    color=colors[j], 
                    label=f"{exp_name} (monthly)", 
                    linewidth=3.5, 
                    marker='s', 
                    markersize=7,
                    zorder=5,
                    path_effects=None) # Default path effects

    # Grid and Aesthetics
    ax.set_xticks(month_mid)
    ax.set_xticklabels(month_labels)
    for m in month_bounds:
        ax.axvline(m, color='gray', linestyle=':', alpha=0.3)

    ax.set_xlim(0, 365)
    ax.set_ylabel(f"{texts[idx]} ({units[idx]})", fontweight='bold')
    ax.set_title(f'Climatology: {texts[idx]} (1970-2014)', fontweight='bold')
    
    # Updated legend with daily and monthly labels
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=fz-10, frameon=True)
    
    plt.tight_layout()
    
    # --- Save Figure ---
    save_name = f"climatology_detailed_{v_name}.png"
    plt.savefig(save_name, dpi=300, bbox_inches='tight')
    print(f"File saved: {save_name}")
    
    plt.show()