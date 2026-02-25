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

cases = (surf_sw_net, surf_lw_down)#, surf_lw_net, surf_sw_down, top_lw_net, top_sw_down, top_sw_net)
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
    #print(data)
    #Variable:
    var = data[variab[nn]]
    
    lon = np.arange(-180.0,180.0,0.25)
    lat = np.arange(-90.0, 90.0, 0.25)
    
    lons, lats = np.meshgrid(lon, lat)

    # Figure and map projection
    fig = plt.figure(figsize=(20, 10))
    ax = plt.axes(projection=ccrs.Robinson(central_longitude=180))

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

    plt.contourf([lons, lats], var2, [16], cmap='turbo')

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

    # Labels and title
    ax.set_title('Annual mean (ERA5 1991-2020): '+ texts[nn])

    #plt.show()
    plt.savefig("grafica"+str(nn)+".png")

    nn=nn+1
    print(nn)
