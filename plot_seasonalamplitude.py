import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from pathlib import Path


# Data path
era_path = Path("/home/desan/ESM-data/")
#Temperature diff jul-jan:
seasonal_cycle = era_path / 'ERA5_DiffTemp.nc' 

# Open dataset
data = xr.open_dataset(seasonal_cycle)
#Variable:
var = data['t2m']
#remove time dimension:
var2d=var.squeeze()

# Figure and map projection
fig = plt.figure(figsize=(20, 5))
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
fz= 15

#Colormap for segmented colorbar:
#According to the presentation plots:
nlevels = 7
levels = np.array([0, 5, 10, 20, 30, 40, 50])
cmap = plt.get_cmap('turbo', nlevels)

cs = var2d.plot.contour(
        ax=ax, 
        x="longitude", 
        y="latitude", 
        transform=ccrs.PlateCarree(),
        levels=levels,
        cmap= cmap, 
        add_colorbar=False)

ax.clabel(cs,
          levels=levels,
          inline=True,
          fontsize=fz,
          fmt='%d')

ax.set_ylim(0, 90)
ax.set_yticks(np.arange(0, 90.1, 10))
ax.set_yticklabels(['EQ','10N', '20N', '30N', '40N', '50N', '60N', '70N', '80N', '90N'],
                   fontsize=fz)
ax.set_ylabel('')
ax.set_xticks(np.arange(-180, 180.05, 60))
ax.set_xticklabels(['0', '60E', '120E', '180', '120W', '60W', '0'],
                   fontsize=fz)
ax.set_xlabel('')

# Add coastline and borders
ax.coastlines(resolution="50m", linewidth=1.0)
ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)
   
# Labels and title
ax.set_title('Seasonal cycle amplitude (Jul-Jan): Surface temperature (from ERA5 1991-2020)', 
             fontsize=20,
             fontweight='bold')

#plt.show()
plt.savefig("seasonal_cycle_surftemp.png")
