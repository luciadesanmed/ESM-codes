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
surf_sw_net = era_path / 'avg_surf_sw_net.nc'
surf_lw_down = era_path / 'avg_surf_lw_down.nc'
surf_lw_net = era_path / 'avg_surf_lw_net.nc'
surf_sw_down = era_path / 'avg_surf_sw_down.nc'
top_lw_net = era_path / 'avg_top_lw_net.nc'
top_sw_down = era_path / 'avg_top_sw_down.nc'
top_sw_net = era_path / 'avg_top_sw_net.nc'

cases = (surf_sw_net, surf_lw_down, surf_lw_net, surf_sw_down, top_lw_net, top_sw_down, top_sw_net)
variab = ('avg_snswrf','avg_sdlwrf','avg_snlwrf', 'avg_sdswrf', 'avg_tnlwrf', 'avg_tdswrf', 'avg_tnswrf') 
cmaps = ('turbo','turbo','turbo','turbo','turbo','turbo','turbo')

#Tuple with cases:
texts = ('Net SW radiation at the surface','Downward LW radiation at the surface','Net LW radiation at the surface',
         'Downward SW radiation at the surface', 'Net LW radiation at the TOA', 'Downward SW radiation at the TOA',
         'Net SW radiation at the TOA')

nn=0
for i in cases:
    # Open dataset
    data = xr.open_dataset(i)
    #Variable:
    var = data[variab[nn]]

    if var.max()<0:
     var=var*-1.0

    # Figure and map projection
    fig = plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))

    #Colormap for segmented colorbar:
#According to the presentation plots:
    nlevels = 14
    vmin = 60
    vmax = 340
    levels = np.linspace(vmin, vmax, nlevels + 1)
    cmap = plt.get_cmap('turbo', nlevels)
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
    orientation='horizontal',
    pad=0.05,
    fraction=0.05,
    extend='neither')

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

    #plt.show()
    plt.savefig("grafica"+str(nn)+".png")

    nn=nn+1
    print(nn)
