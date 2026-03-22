import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from pathlib import Path

# --- 1. Setup and Paths ---
dat_path = Path("/home/desan/ESM-data/")

# List of all 12 files (4 per variable: 3 EC-Earth + 1 ERA5)
all_cases = (
    'pr_annualmean_EC-Earth3.nc', 'pr_annualmean_EC-Earth3-AerChem.nc', 'pr_annualmean_EC-Earth3-Veg-LR.nc', 'tp_annualmean_ERA5.nc',
    'tas_annualmean_EC-Earth3.nc', 'tas_annualmean_EC-Earth3-AerChem.nc', 'tas_annualmean_EC-Earth3-Veg-LR.nc', 't2m_annualmean_ERA5.nc',
    'hurs_annualmean_EC-Earth3.nc', 'hurs_annualmean_EC-Earth3-AerChem.nc', 'hurs_annualmean_EC-Earth3-Veg-LR.nc', 'rh_annualmean_ERA5.nc'
)

# Experiment labels for titles
exps = ['EC-Earth3', 'EC-Earth3-AerChem', 'EC-Earth3-Veg-LR', 'ERA5 (1970-2014)']

# Metadata for plotting
texts = ('Precipitation', 'Temperature (surface)', 'Relative humidity (surface)')
units = ('mm/day', '°C', '%')
cmaps = ('YlGnBu', 'turbo', 'YlGnBu')
vmin1 = (0, -30, 0)
vmax1 = (10.1, 30.1, 100.1)
cticks = (1, 5, 20)
cbarext = ('max', 'both', 'neither')

# Internal variable names
var_map_ece = ['pr', 'tas', 'hurs']
var_map_era = ['tp', 't2m', 'rh']

nn = 0  # Counter for output filenames

# --- 2. Main Processing Loop ---
for v_idx in range(3):  # Loop through Precipitation, Temperature, Humidity
    
    for e_idx in range(4):  # Loop through 4 Experiments per variable
        
        file_name = all_cases[nn]
        print(f"Processing File {nn}: {file_name}")
        
        # Open dataset
        ds = xr.open_dataset(dat_path / file_name)
        
        # Coordinate Standardization: Rename 'longitude/latitude' to 'lon/lat'
        rename_dict = {}
        if 'longitude' in ds.coords: rename_dict['longitude'] = 'lon'
        if 'latitude' in ds.coords: rename_dict['latitude'] = 'lat'
        if rename_dict:
            ds = ds.rename(rename_dict)

        # Select correct variable name
        v_name = var_map_era[v_idx] if e_idx == 3 else var_map_ece[v_idx]
        var = ds[v_name]

        # Ensure we are working with a 2D spatial map (mean over time if exists)
        if 'time' in var.dims:
            var = var.mean(dim='time')

        # --- Unit Conversions ---
        # 1. Precipitation (Index 0)
        if v_idx == 0:
            if e_idx == 3:  # ERA5 'tp' is in meters
                var = var * 1000
            else:           # EC-Earth 'pr' is in kg/m2/s
                var = var * 86400
        
        # 2. Temperature (Index 1) - Kelvin to Celsius for both
        elif v_idx == 1:
            var = var - 273.15

        # --- 3. Plotting ---
        fig = plt.figure(figsize=(20, 10))
        ax = plt.axes(projection=ccrs.Robinson(central_longitude=0))

        # Colorbar and Normalization
        nlevels = 200
        vmin, vmax = vmin1[v_idx], vmax1[v_idx]
        levels = np.linspace(vmin, vmax, nlevels + 1)
        cmap = plt.get_cmap(cmaps[v_idx], nlevels)
        norm = colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False)

        # Plot Data
        pcm = var.plot(
            ax=ax, 
            x="lon", 
            y="lat",
            transform=ccrs.PlateCarree(),
            cmap=cmap, 
            norm=norm,
            add_colorbar=False
        )

        # Add Colorbar
        cbar = plt.colorbar(
            pcm, ax=ax,
            ticks=np.arange(vmin, vmax + 0.1, cticks[v_idx]),
            orientation='horizontal', pad=0.05, fraction=0.05,
            extend=cbarext[v_idx]
        )
        cbar.set_label(f"{texts[v_idx]} [{units[v_idx]}]", fontsize=16, fontweight='bold')
        cbar.ax.tick_params(labelsize=14)

        # Map Features
        ax.coastlines(resolution="50m", linewidth=1.0)
        ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

        # Gridlines
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color="black", alpha=0.3)
        gl.top_labels = False
        gl.right_labels = False

        # Titles
        ax.set_title(f'Annual mean {exps[e_idx]}: {texts[v_idx]}', fontsize=20, fontweight='bold')

        # --- 4. Save and Cleanup ---
        plt.savefig(f"annualmean_plot_{nn}.png", bbox_inches='tight')
        plt.close(fig) # Free up memory
        
        nn += 1
