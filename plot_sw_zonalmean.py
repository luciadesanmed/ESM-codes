import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import matplotlib.colors as mcolors
from pathlib import Path

# Data path
era_path = Path("/home/desan/ESM-data/")
top_sw_down = era_path / 'zonal_avg_top_sw_down.nc'

data = xr.open_dataset(top_sw_down)

var = data['avg_tdswrf']
var = var.squeeze() #12x721
var = var.transpose()
var = np.flipud(var)
var = np.ma.masked_where(var <= 0, var)
levels = np.arange(0, 650, 50)

cmap_base = plt.cm.jet
colors = cmap_base(np.linspace(0, 1, len(levels)-1))
colors[0] = [1, 1, 1, 1]
cmap = mcolors.ListedColormap(colors)
#cmap.set_under('white')
#cmap.set_bad('white')

lat = np.arange(-90.0, 90.25, 0.25) #721
date = np.arange(0, 12, 1) #12

plt.figure(figsize=(10, 10))
ax = plt.axes()
ax.set_facecolor('white')
ax.set_box_aspect(1)

cs = plt.contour(date, lat, var, 10,
    colors='k',
    linewidths=0.5,
    add_colorbar = False)

cf = plt.contourf(date, lat, var,
             levels = levels,
             cmap=cmap,
             extend='neither')

fz=16
plt.xlabel("Month", fontsize=fz)
plt.ylabel("Latitude", fontsize=fz)
plt.title("Zonal mean based on daily insolation", fontsize=fz, fontweight='bold')
cbar = plt.colorbar(cf, ticks=[0] + list(levels))
cbar.set_label(r"W m$^{-2}$", fontsize=fz)
cbar.ax.tick_params(labelsize=fz)
ax.set_xticks(np.arange(0,12,1))
ax.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'], fontsize=fz)
ax.set_yticks(np.arange(-90,90.25,30))
ax.set_yticklabels(['90S','60S','30S','0','30N','60N','90N'], fontsize=fz)

plt.savefig('zonalmean.png')

