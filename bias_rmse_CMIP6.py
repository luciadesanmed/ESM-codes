import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from pathlib import Path

# Data path
dat_path = Path("/home/desan/ESM-data/")

# Configuration: Variable keys and descriptive titles
variab = ('pr', 'tas', 'hurs')
texts = ('Precipitation', 'Surface Temperature', 'Surface Relative Humidity')
units = ('mm/day', '°C', '%')

# Model list (ERA5 is the reference)
models = ('EC-Earth3', 'EC-Earth3-AerChem', 'EC-Earth3-Veg-LR')

# Visualization settings for BIAS (Divergent)
cmaps_bias = ('RdBu', 'RdBu', 'RdBu_r') 
vmin_bias = (-3, -5, -10)
vmax_bias = (3, 5, 10)
cticks_bias = (1, 1, 2.5)

# Visualization settings for RMSE (Sequential)
# Fixed max values to allow comparison between models
vmax_rmse = (3, 5, 15) 

for idx, v_name in enumerate(variab):
    for mod_name in models:
        
        # --- PART 1: PLOTTING BIAS ---
        bias_file = f"{v_name}_bias_{mod_name}-ERA5.nc"
        bias_path = dat_path / bias_file
        
        if bias_path.exists():
            ds_bias = xr.open_dataset(bias_path)
            # Accessing the variable directly by its short name (pr, tas, hurs)
            bias_data = ds_bias[v_name].squeeze()
            
            fig = plt.figure(figsize=(16, 8))
            ax = plt.axes(projection=ccrs.Robinson(central_longitude=0))
            
            # Setup discrete levels for the colorbar
            levels_b = np.linspace(vmin_bias[idx], vmax_bias[idx], 21)
            cmap_b = plt.get_cmap(cmaps_bias[idx])
            norm_b = mcolors.BoundaryNorm(levels_b, ncolors=cmap_b.N, clip=False)

            pcm_b = bias_data.plot(
                ax=ax, x="lon", y="lat",
                transform=ccrs.PlateCarree(),
                cmap=cmap_b, norm=norm_b, add_colorbar=False
            )

            # Map Aesthetics
            ax.coastlines(resolution="110m", linewidth=0.8)
            ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.4)
            
            # Add Horizontal Colorbar
            cbar_b = plt.colorbar(
                pcm_b, ax=ax,
                ticks=np.arange(vmin_bias[idx], vmax_bias[idx] + 0.1, cticks_bias[idx]),
                orientation='horizontal', pad=0.05, fraction=0.05, extend='both'
            )
            cbar_b.set_label(f'BIAS ({units[idx]})', fontsize=14, fontweight='bold')

            ax.set_title(f'BIAS: {mod_name} vs ERA5\n{texts[idx]}', fontsize=18, fontweight='bold')
            
            plt.savefig(f"map_bias_{v_name}_{mod_name}.png", dpi=300, bbox_inches='tight')
            plt.close()
            print(f"Successfully saved Bias map: {bias_file}")
        else:
            print(f"Warning: Bias file not found: {bias_file}")


        # --- PART 2: PLOTTING RMSE ---
        rmse_file = f"{v_name}_rmse_{mod_name}-ERA5.nc"
        rmse_path = dat_path / rmse_file
        
        if rmse_path.exists():
            ds_rmse = xr.open_dataset(rmse_path)
            rmse_data = ds_rmse[v_name].squeeze()
            
            fig = plt.figure(figsize=(16, 8))
            ax = plt.axes(projection=ccrs.Robinson(central_longitude=0))
            
            # Using a sequential colormap for error magnitude
            pcm_r = rmse_data.plot(
                ax=ax, x="lon", y="lat",
                transform=ccrs.PlateCarree(),
                cmap='YlOrRd', vmin=0, vmax=vmax_rmse[idx],
                add_colorbar=False
            )

            ax.coastlines(resolution="110m", linewidth=0.8)
            ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.4)
            
            cbar_r = plt.colorbar(
                pcm_r, ax=ax, orientation='horizontal', 
                pad=0.05, fraction=0.05, extend='max'
            )
            cbar_r.set_label(f'RMSE ({units[idx]})', fontsize=14, fontweight='bold')

            ax.set_title(f'RMSE: {mod_name} vs ERA5\n{texts[idx]}', fontsize=18, fontweight='bold')
            
            plt.savefig(f"map_rmse_{v_name}_{mod_name}.png", dpi=300, bbox_inches='tight')
            plt.close()
            print(f"Successfully saved RMSE map: {rmse_file}")
        else:
            print(f"Warning: RMSE file not found: {rmse_file}")