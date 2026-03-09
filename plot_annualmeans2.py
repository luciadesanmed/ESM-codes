import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from pathlib import Path


# Data path
era_path = Path("/home/desan/ESM-data/")

#Cases:
surf_net_rad = era_path / 'surface_net_radiation.nc'
surf_lat_heat = era_path / 'surface-latent-heat.nc'
surf_sens_heat = era_path / 'surface-sensible-heat.nc'
surf_heat_stor = era_path / 'surface-heat-storage.nc'

cases = (surf_net_rad, surf_lat_heat, surf_sens_heat, surf_heat_stor)
variab = ('ssr', 'avg_slhtf', 'avg_ishf', 'ssr')
cmaps = ('turbo','turbo','coolwarm', 'coolwarm') #_r to invert the colormap
nlevels1 = (200, 200, 200, 200) 
vmin1 = (50, 0, -60, -200)
vmax1 = (250.1, 200.1, 100.1, 200.1)
cticks = (50, 25, 20, 50)

#Tuple with cases:
texts = ('Net surface radiation', 'Surface latent heat flux', 'Surface sensible heat flux', 'Surface heat storage')

nn=0
for i in cases:
    # Open dataset
    data = xr.open_dataset(i)
    #Variable:
    var = data[variab[nn]]

    if nn==1 or nn==2: 
        var = var*-1
        
    # Figure and map projection
    fig = plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=ccrs.Robinson(central_longitude=0))

    #Colormap for segmented colorbar:
    #According to the presentation plots:
    nlevels = nlevels1[nn]
    vmin = vmin1[nn]
    vmax = vmax1[nn]
    levels = np.linspace(vmin, vmax, nlevels + 1)
    cmap = plt.get_cmap(cmaps[nn], nlevels)
    norm = colors.BoundaryNorm(levels, ncolors=cmap.N, clip=False)

    pcm = var.plot(
    ax=ax,
    x="longitude",
    y="latitude",
    transform=ccrs.PlateCarree(),
    cmap=cmap,
    norm=norm,
    add_colorbar=False)

    cbar = plt.colorbar(
    pcm,
    ax=ax,
    ticks=np.arange(vmin, vmax, cticks[nn]),
    orientation='horizontal',
    pad=0.05,
    fraction=0.05,
    extend='both')

    cbar.set_label(
    texts[nn] + r" W m$^{-2}$",
    fontsize=16)

    cbar.ax.tick_params(labelsize=14)

    # Add coastline and borders
    ax.coastlines(resolution="50m", linewidth=1.0)
    ax.add_feature(cfeature.BORDERS, linestyle=":", linewidth=0.5)

    # Gridlines
    gl = ax.gridlines(
    draw_labels=True,
    linewidth=0.5,
    color="black",
    alpha=0.5,
    linestyle="-"
    )
    
    gl.xlabel_style = {'size': 14}
    gl.ylabel_style = {'size': 14}

    # Labels and title
    ax.set_title('Annual mean (ERA5 1991-2020): '+ texts[nn], fontsize=20)

   # plt.show()
    plt.savefig("grafica"+str(nn)+".png")

    nn=nn+1
    print(nn)
