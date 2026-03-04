import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from pathlib import Path


# Data path
era_path = Path("/home/desan/ESM-data/")

#Annual mean data:
annual_mean = era_path / 'ERA5_AnnualTemp-avg.nc'

#Zonal mean data:
zonal_mean = era_path / 'ERA5zonalTemp.nc'

#Annual mean:
data = xr.open_dataset(annual_mean)
#Variable:
var = data['t2m']

#remove time dimension:
annual=var.squeeze()

#Zonal mean:
data = xr.open_dataset(zonal_mean)
var = data['t2m']
zonal = var.squeeze()
zonal = zonal.rename({'lat':'latitude'}) #i dont know why the name changed to lat

#Difference between annual and zonal:
diff = annual - zonal

# Figure and map projection
fig = plt.figure(figsize=(20, 5))
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
fz= 15

#Colormap for segmented colorbar:
#According to the presentation plots:
nlevels = 7
levels = np.arange(-9, 9, 3)
cmap = plt.get_cmap('turbo', nlevels)
mylinestyles = ['--' if l < 0 else '-' for l in levels]

cs = diff.plot.contour(
        ax=ax, 
        x="longitude", 
        y="latitude", 
        transform=ccrs.PlateCarree(),
        levels=levels,
        cmap= cmap,
        linestyles=mylinestyles,
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
ax.set_title('Annual mean - Averaged zonal mean: Surface temperature (from ERA5 1991-2020)', 
             fontsize=20,
             fontweight='bold')

#plt.show()
plt.savefig("diffannualzonal_surftemp.png")
