import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from pathlib import Path
from netCDF4 import Dataset as NetCDFFile

# Data path
era_path = Path("/home/desan/ESM-data/")

top_sw_down = era_path / 'zonal_avg_top_sw_down.nc'

# Open dataset
data = NetCDFFile(top_sw_down)

#Variable:
var = data.variables['avg_tdswrf'][:]
print(var)

lat = np.arange(-90.0, 90.25, 0.25)
date = np.arange(0, 360, 1)
    
dates, lats = np.meshgrid(date, lat)

# Figure and map projection
fig = plt.figure(figsize=(20, 10))
var = var[:,:,0]
var = var.transpose()
#ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))
plt.contourf(dates, lats, var, 10)
    #Colormap:
    #minval = 0.0
    #maxval = 1.0
    #cmap = plt.get_cmap(cmaps[nn])
    #n=16
    #new_cmap = colors.LinearSegmentedColormap.from_list('trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
    #    cmap(np.linspace(minval, maxval, n)))
    
    # Plot
    #var.plot(
    #ax=ax,
    #x="longitude",
    #y="latitude",
    #transform=ccrs.PlateCarree(),
    #cmap = 'turbo',
    #cbar_kwargs={"label": texts[nn] + " (W/m²)"}
    #)

    #plt.contourf([lons, lats], var2, [16], cmap='turbo')
    # Gridlines
    #gl = ax.gridlines(
    #draw_labels=True,
    #linewidth=0.5,
    #color="black",
    #alpha=0.5,
    #linestyle="-"
    #)

    # Labels and title
#ax.set_title('Annual mean (ERA5 1991-2020): '+ texts[nn])

plt.show()
    #plt.savefig("grafica"+str(nn)+".png")
