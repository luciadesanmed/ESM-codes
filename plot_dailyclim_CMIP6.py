
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

dat_path = Path("/home/desan/ESM-data/")

variab = ('pr', 'tas', 'hurs')
units = ('mm/day', '°C', '%')
exps = ('EC-Earth3', 'EC-Earth3-AerChem', 'EC-Earth3-Veg-LR')
texts = ('Precipitation', 'Temperature', 'Relative Humidity')
colors = ['#1f77b4', '#d62728', '#2ca02c']

#Central days of each month to center labels
month_mid = [15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]
month_labels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']

for idx, v_name in enumerate(variab):
    plt.figure(figsize=(14, 7))
    fz = 18
    plt.rcParams.update({'font.size': fz})
    ax = plt.axes()
    
    for j, exp_name in enumerate(exps):
        file_name = f"{v_name}_dailyclim_{exp_name}.nc"

        data = xr.open_dataset(dat_path / file_name)
        data[v_name] = data[v_name].where(data[v_name] > -1000)
        var_data = data[v_name].squeeze()
            
        days = np.arange(1, len(var_data) + 1)
            
        if v_name=='tas':
            var_data=var_data-273.15
        elif v_name=='pr':
            var_data=var_data*86400

        ax.plot(days, var_data, 
                color=colors[j], 
                label=exp_name, 
                linewidth=1.5,
                alpha=0.8)
            
    #x axis configuration:
    ax.set_xticks(month_mid) # tick at the middle of the month
    ax.set_xticklabels(month_labels)
    
    month_bounds = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
    for m in month_bounds:
        ax.axvline(m, color='gray', linestyle=':', alpha=0.3)

    ax.set_xlim(0, 365)
    ax.set_ylabel(f"{texts[idx]} ({units[idx]})", fontweight='bold')
    ax.set_xlabel('Month', fontweight='bold')
    ax.set_title(f'Daily Climatology: {texts[idx]}', fontweight='bold')
    
    ax.grid(True, axis='y', linestyle='--', alpha=0.5)
    ax.legend(loc='upper right', fontsize=fz-6, frameon=True)
    
    plt.tight_layout()
    plt.savefig(f'daily_annual_clim_{v_name}.png', dpi=300)
